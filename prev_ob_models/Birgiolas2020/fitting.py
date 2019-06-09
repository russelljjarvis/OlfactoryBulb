from exceptions import Exception

from olfactorybulb.database import *
import os,sys
from neuronunit.tests.olfactory_bulb.publications import *
from neuronunit.tests.olfactory_bulb.tests import *
from neuronunit.models.neuron_cell import NeuronCellModel
from sciunit.suites import TestSuite
from pandas import DataFrame
import quantities as pq
from neuronunit.tests.olfactory_bulb.utilities import cache
from linetimer import CodeTimer
import string, math
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import linetimer
import multiprocessing
from multiprocessing import Pool, TimeoutError
from sciunit.scores import ZScore
from deap import base, creator
import math
import random
from deap import tools
from time import sleep, time

SHOW_ERRORS = True
FAST_EVAL = False

class CellFitter(object):
    def __init__(self, cell_type, fitting_model_class):
        print("Starting FITTER for", fitting_model_class)

        self.fitting_model_class = fitting_model_class
        self.cell_type = cell_type

        self.load_measurements()

        # GA classes
        creator.create("FitnessMin", base.Fitness, weights=(-1,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

    def pretty_pop(self):
        import pandas
        df = pandas.DataFrame([list(i) for i in self.pop], [i.fitness.values[0] for i in self.pop])
        df.columns = [p['attr'] for p in self.params]
        df = df.sort_index()
        return df

    def load_measurements(self):
        # Load ephyz measurments for the cell from DB
        self.measurements = Measurement \
            .select(Measurement) \
            .join(Property) \
            .switch(Measurement) \
            .join(Source) \
            .where((Measurement.property.type == "Electrophysiology") &
                   (Measurement.property.id.startswith(self.cell_type + '_'))) \
            .order_by(Measurement.property.id)

        # Aggregate measurments into NeuronUnit tests of properties
        self.properties = {}

        for m in self.measurements:
            # Create specific measurement test classes
            test_generic = str(m.property.test_class_generic)
            pub = str(m.source.publication_class).strip()
            class_name = test_generic + pub

            if FAST_EVAL and test_generic != "RestingVoltageTest":
                continue

            if test_generic not in self.properties:
                self.properties[test_generic] = []

            # Make the created classes available globaly
            globals()[class_name] = type(class_name, (eval(pub), eval(test_generic)), {})

            # Create instances of those classes with the specific
            # measurments (against which the model will be compared)
            test_instance = eval(class_name)(observation={
                "mean": m.mean * eval(m.property.units),
                "std": m.std * eval(m.property.units),
                "n": m.n
            })

            self.properties[test_generic].append(test_instance)

        return self.properties

    def load_previous_models_as_workitems(self):
        # Load model class names from the DB
        self.model_classes = list(CellModel \
                             .select(CellModel) \
                             .where(CellModel.cell_type == self.cell_type.upper())
                             )

        # Make the model classes loadable with 'module.module.ModelClass()'
        for i, m in enumerate(model_classes):
            nmsp = string.join(m.isolated_model_class.split('.')[:-1], '.')
            cls = m.isolated_model_class.split('.')[-1]

            import_cmd = 'from ' + nmsp + ' import ' + cls + ' as Model' + str(i)
            print(import_cmd)
            exec (import_cmd)

        # Create work item list
        self.work_items = []

        for model in self.model_classes:
            self.work_items.append({"model_class": model.isolated_model_class})

        return self.work_items

    def evaluate(self, param_set, raw_scores=False):

        try:
            score = self.get_workitem_score({
                "model_class": self.fitting_model_class,
                "param_values": param_set
            })

            return score["model_score"],

        except:
            if SHOW_ERRORS:
                import traceback
                print(traceback.format_exc())

            raise

    def get_workitem_score(self, item):
        results = item
        results["properties"] = {}
        results["model_score"] = 0

        model_class = str(item["model_class"])

        # This line takes input like: 'prev_ob_models.BhallaBower1993.isolated_cells.MC' and converts it to:
        #                         from prev_ob_models.BhallaBower1993.isolated_cells import MC
        exec('from ' + '.'.join(model_class.split('.')[0:-1]) + " import " + model_class.split('.')[-1])

        # Import the root module
        exec("import " + model_class.split('.')[0])

        # Instantiate the model class
        exec ('cell = ' + model_class + '()')

        if "param_values" in item:
            param_values = item["param_values"]
            self.set_model_params(param_values, cell.cell)
        else:
            param_values = []

        model = NeuronCellModel(cell.soma(0.5),
                                name=cell.__class__.__module__ + '.' +
                                     cell.__class__.__name__ + '|' +
                                     str(param_values))

        if FAST_EVAL:
            print("FAST_EVAL: ON. Evaluating only: ", self.properties.keys())

        # Compute the Root Mean Square error score of the model
        for prop in self.properties.keys():

            if prop not in results["properties"]:
                results["properties"][prop] = {"tests": {}, "total_n": 0, "z_score_combined": None}

            prop_tests = self.properties[prop]

            for prop_test in prop_tests:

                prop_test_result = {}
                results["properties"][prop]["tests"][prop_test.__class__.__name__] = prop_test_result

                try:
                    prediction = prop_test.generate_prediction(model)

                except:
                    import traceback
                    prediction = traceback.format_exc()

                    if SHOW_ERRORS:
                        print(prediction)

                prop_test_result["observation"] = prop_test.observation
                prop_test_result["prediction"] = prediction

                if type(prediction) != str:
                    z_score = (prediction - prop_test.observation["mean"]) / prop_test.observation["std"]
                    z_score = z_score.simplified
                else:
                    z_score = 6.0*pq.dimensionless  # errors are treated as 6 std deviation

                # Weigh each publication z-score by the pub sample size
                z_weighed = z_score * prop_test.observation["n"]

                prop_test_result["z_score"] = z_score
                prop_test_result["z_score_weighed"] = z_weighed

                results["properties"][prop]["total_n"] += prop_test.observation["n"]

            results["properties"][prop]["z_score_combined"] = sum([i["z_score_weighed"] for i in results["properties"][prop]["tests"].values()])
            results["properties"][prop]["z_score_combined"] /= results["properties"][prop]["total_n"]

            results["model_score"] += results["properties"][prop]["z_score_combined"].magnitude ** 2

        import math
        results["model_score"] = math.sqrt(results["model_score"])

        return results

    def set_model_params(self, param_values, hoc_cell):
        from neuron import h
        for pi, pv in enumerate(param_values):
            attr = self.params[pi]["attr"]
            if attr == "tau_CaPool":
                setattr(h, attr, pv)
            else:
                for param_list in self.params[pi]["lists"]:
                    for sec in getattr(hoc_cell, param_list):
                        if attr == "diam":
                            for i3d in range(int(h.n3d(sec=sec))):
                                h.pt3dchange(i3d, h.diam3d(i3d, sec=sec) * pv, sec=sec)
                        else:
                            setattr(sec, attr, pv)

    def get_best_score(self):

        score = self.get_workitem_score({
            "model_class": self.fitting_model_class,
            "param_values": self.best
        })

        df = []
        model = score
        row = {"model": model["model_class"]}
        for t, test in enumerate(model["properties"].keys()):
            row[test] = model["properties"][test]["z_score_combined"]
        df.append(row)

        df = DataFrame(df, [model["model_class"]])
        return df, score

    def random_parameters(self):
        # Initial param values are uniformly distributed between the low-high bounds
        result = [random.random()] * len(self.params)

        for i, pv in enumerate(result):
            result[i] = (self.params[i]["high"] - self.params[i]["low"]) * pv + self.params[i]["low"]

        return creator.Individual(result)

    def get_fitnesses(self, pop, label):
        max_wait = round(2.5 * 60) # seconds
        processes = max(1, multiprocessing.cpu_count() - 1)

        from multiprocess import Pool, TimeoutError

        pool = Pool(processes=processes, maxtasksperchild=1)
        processes = [pool.apply_async(self.evaluate, (list(ind),)) for ind in pop]

        wait_until = time() + max_wait

        fitnesses = []

        print("STARTED GEN", label)

        for pi, process in enumerate(processes):
            timeout = max(0, wait_until - time())

            try:
                result = process.get(timeout)

            except TimeoutError:
                result = 9 * 10.0,

                if SHOW_ERRORS:
                    print('Simulation timed out')

            except:
                result = 9 * 10.999,

                if SHOW_ERRORS:
                    print('Error in simulation')

            fitnesses.append(result)

            print("DONE with", pi+1, "of", len(processes), "of GEN", label, "with Fitness","%.2f" % result[0])

        pool.terminate()

        return fitnesses


    def fit(self, generation_size, number_of_generations):

        if generation_size < 5:
            raise Exception("Generation size must be 5 or more")

        if number_of_generations < 0:
            raise Exception("Number of generations must be 0 or more")

        self.pop = self.GA(self.top if hasattr(self, "top") else None, generation_size, number_of_generations)

    def GA(self, suggested_pop=None, n=30, NGEN=30):
        lows = [p["low"] for p in self.params]
        highs = [p["high"] for p in self.params]

        toolbox = base.Toolbox()
        toolbox.register("individual", self.random_parameters)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta=0.1, low=lows, up=highs)
        toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.1, low=lows, up=highs, indpb=0.1)
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("select", tools.selNSGA2, k=int(n * 0.2))

        if suggested_pop is None:
            self.pop = toolbox.population(n=n)
        else:
            self.pop = [creator.Individual(i) for i in suggested_pop]

        CXPB, MUTPB = 1, 1
        F_DIVERSITY = 0.5

        # Evaluate the entire population - each in a separate process
        fitnesses = self.get_fitnesses(self.pop, label="ZERO")

        for ind, fit in zip(self.pop, fitnesses):
            ind.fitness.values = fit

        for g in range(NGEN):
            # Select the parents
            elite = toolbox.select(self.pop)

            random_offspring = toolbox.population(n=int(n * F_DIVERSITY / 2.0))
            diversity_offspring = random_offspring + tools.selRandom(self.pop, int(n * F_DIVERSITY / 2.0))
            elite_offspring = tools.selRandom(elite, n - len(elite) - len(diversity_offspring))

            offspring = random_offspring + diversity_offspring + elite_offspring

            # Clone the selected individuals
            offspring = map(toolbox.clone, offspring)

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for child in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(child)
                    del child.fitness.values

            # Evaluate the individuals without fitness value - again in separate processes
            offspring_nofitness = [ind for ind in offspring if not ind.fitness.valid]

            fitnesses = self.get_fitnesses(offspring_nofitness, label=str(g+1))

            for ind, fit in zip(offspring_nofitness, fitnesses):
                ind.fitness.values = fit

            # The population is entirely replaced by the parents + offspring
            self.pop[:] = elite + offspring

            self.top = toolbox.select(self.pop)
            self.best = self.top[0]
            print("Generation", g+1, "out of", NGEN, "COMPLETE")
            print('Best fitness:', self.best.fitness.values[0])
            print('Best individual', self.best)


        return self.pop

    def clear_cache(self):
        cache.clear()

class FitterMC(CellFitter):
    def __init__(self, fitting_model_class = "prev_ob_models.Birgiolas2020.isolated_cells.MC"):

        super(FitterMC, self).__init__(
            cell_type="mc",
            fitting_model_class=fitting_model_class
        )

        self.params = [
            { "start": 1.0,       "attr": "diam",      "low": 0.1,   "high": 2.0,     "lists": ["apical","basal","axonal"] },
            { "start": 34.77,     "attr": "Ra",        "low": 5.0,   "high": 100.0,   "lists": ["all"] },
            { "start": 2.706,     "attr": "cm",        "low": 0.1,   "high": 4.0,     "lists": ["all"] },
            { "start": 49.95,     "attr": "ena",       "low": 40.0,  "high": 50.0,    "lists": ["all"] },
            { "start": -70.03,    "attr": "ek",        "low": -100.0,"high": -70.0,   "lists": ["all"] },
            { "start": -64.42,    "attr": "e_pas",     "low": -70.0, "high": -50.0,   "lists": ["all"] },
            { "start": 0.0005955, "attr": "g_pas",     "low": 0,     "high": 0.00003, "lists": ["all"] },
            { "start": 0.5955,    "attr": "sh_Na",     "low": 0,     "high": 10,      "lists": ["all"] },
            { "start": 10,        "attr": "tau_CaPool","low": 1,     "high": 20,     "lists": ["all"] },

            { "start":  0.87485,  "attr": "gbar_Na",     "low": 0, "high": 0.05,  "lists": ["all"] },
            { "start": 0.0297,    "attr": "gbar_Kd",     "low": 0, "high": 0.04,  "lists": ["all"] },
            { "start": 0.000264,  "attr": "gbar_Kslow",  "low": 0, "high": 0.004, "lists": ["all"] },
            { "start": 0.07215,   "attr": "gbar_KA",     "low": 0, "high": 0.005, "lists": ["all"] },
            { "start": 0.001,     "attr": "gbar_KCa",    "low": 0, "high": 0.004, "lists": ["all"] },
            { "start": 0.00081441,"attr": "gbar_LCa",    "low": 0, "high": 0.001, "lists": ["all"] },

            { "start": -30.805,  "attr": "eh",        "low": -40.0, "high": -25.0,   "lists": ["apical"] },
            { "start": 0.00335,  "attr": "gbar_Ih",   "low": 0,     "high": 0.000006, "lists": ["apical"] },
            { "start": 0.000107, "attr": "gbar_CaT",  "low": 0,     "high": 18e-3,   "lists": ["apical"] },
        ]

        self.top = [
            [1.825548648056325,
             54.13085715757424,
             1.450513328526805,
             43.46285468853027,
             -79.11578796172239,
             -51.23433621786335,
             2.9304959431139075e-05,
             2.7877089993733044,
             7.579423908207511,
             0.017314273442651348,
             0.013851418754121077,
             0.003492982004433873,
             0.0027512416572638607,
             0.0028399162014080535,
             0.0005158999034465254,
             -34.80571796720459,
             2.0777128131181613e-06,
             0.013341839235068506],

            [1.705342506779839, 57.09925288588258, 1.0480872753459018, 46.92740617824292, -72.62711581494455,
             -63.366346152577506, 2.9914568225261235e-05, 1.562956194462862, 14.20637343187267, 0.01214827511477937,
             0.0218850395961089, 0.0027193856629376834, 0.0035351916435461123, 0.0034455698227170047,
             0.00022010267881156947, -32.888237647601514, 2.4331763915413932e-06, 0.01217015480225392],

            [1.6326325740341017, 34.177396997364056, 0.794699716025574, 41.78273762900968, -78.93519835072384,
             -50.08361215379143, 1.8396477462947385e-05, 4.848903066311322, 3.00304851331697, 0.0098190845816793,
             0.019793837590846183, 0.0016599394725783164, 0.002257500120349872, 0.0020460839439385443,
             0.0009409229621420443, -38.26700986258791, 1.161083055427734e-06, 0.017756177795447206]

        ]



