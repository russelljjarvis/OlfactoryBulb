
from neuron import h

class TransformGC2:
    def __init__(self):

        # Create a section lookup by section name
        # Note: this assumes each section has a unique name
        self.name2section = { sec.name(): sec for sec in h.allsec() }

        # This will store the new section coordinates
        self.section_coords = { }

    def set_coords(self, sec_name):
        # Lookup the section
        nrn_section = self.name2section[sec_name]

        # Lookup its new coords
        new_coords = self.section_coords[sec_name]

        # Use 3D points as section L and diam sources
        h.pt3dconst(1, sec=nrn_section)

        # Clear the existing points - and allocate room for the incoming points
        h.pt3dclear(len(new_coords["diam"]), sec=nrn_section)

        # Use vectorization to add the points to section
        xvec = h.Vector(new_coords["x"])
        yvec = h.Vector(new_coords["y"])
        zvec = h.Vector(new_coords["z"])
        dvec = h.Vector(new_coords["diam"])

        h.pt3dadd(xvec, yvec, zvec, dvec, sec=nrn_section)

    def set_all(self):
        for sec_name in self.section_coords.keys():
            self.set_coords(sec_name)

    @staticmethod
    def apply_on(prefix):
        t = TransformGC2()
        t.define_coords(prefix)
        t.set_all()

    @staticmethod
    def apply():
        t = TransformGC2()
        t.define_coords()
        t.set_all()

    def define_coords(self, prefix = 'GC2[0]'):
        if prefix != '':
            prefix += '.'

        self.section_coords = {
          prefix + 'apic[5]': {
              'x':[-36.016,-37.106,-37.271,-36.622,-35.876,-34.937,-33.827,-32.159,-31.031,-30.005,-28.972,-27.852,-26.616,-25.759,-24.639,-23.524,-22.515,-21.589,-20.106,-18.861,-17.997,-16.764,-15.833,-14.918,-13.695,-12.504,-10.784,-9.245,-8.064,-6.758,-5.362,-4.167,-3.188,-2.262,-1.068,0.100,0.998,1.966,3.186,4.217,5.584,6.714,7.591,8.572,9.462,10.594,12.284,13.381,15.884,17.442,18.745,20.008,21.366,22.714,23.868,24.463,25.004,25.398,25.667,26.234,27.030,27.854,28.888,30.130,31.037,32.218,33.106,34.018,34.874,35.811,36.968,38.203,39.094,40.063,40.943,41.860,42.853,43.848,45.193,46.185,47.403,48.516,50.008,51.200,52.472,53.422,54.263,55.385,57.018,58.206,59.493,60.519,61.495,62.675,63.627,64.862,66.461],
              'y':[804.321,804.114,803.928,803.782,803.734,803.458,803.532,803.775,804.039,804.130,804.056,803.934,804.247,804.563,804.820,804.935,805.088,805.318,805.484,805.642,805.782,805.858,805.928,806.114,806.343,806.603,806.672,806.800,807.029,807.476,807.972,808.405,808.665,808.897,809.309,809.452,809.357,809.346,809.761,810.327,810.772,811.188,811.583,811.800,812.040,812.215,812.366,812.337,812.578,812.840,813.113,813.398,814.095,814.869,815.523,816.633,817.177,816.849,816.161,816.000,816.495,817.033,816.914,816.464,816.331,816.203,816.276,816.606,816.922,817.157,817.578,817.496,817.464,817.749,818.266,818.841,819.410,819.878,820.341,820.869,821.369,821.555,821.795,822.147,822.182,822.417,822.819,823.502,823.984,824.164,824.475,824.450,824.264,823.820,823.480,823.117,822.642],
              'z':[-1597.293,-1595.752,-1594.570,-1593.435,-1592.374,-1591.443,-1590.580,-1590.652,-1590.360,-1589.459,-1588.559,-1587.719,-1586.975,-1586.528,-1586.236,-1586.498,-1586.657,-1586.234,-1586.146,-1585.895,-1585.409,-1584.625,-1584.160,-1583.697,-1582.920,-1582.111,-1581.672,-1582.244,-1582.566,-1582.439,-1582.414,-1582.234,-1581.837,-1581.392,-1580.643,-1579.825,-1579.354,-1578.906,-1578.182,-1577.398,-1576.768,-1576.535,-1576.117,-1575.712,-1575.238,-1574.937,-1574.968,-1574.609,-1575.351,-1576.002,-1576.448,-1576.857,-1577.051,-1577.336,-1577.314,-1576.823,-1575.813,-1574.630,-1573.495,-1572.340,-1571.410,-1570.501,-1569.651,-1568.969,-1568.513,-1567.691,-1567.209,-1566.792,-1566.345,-1565.909,-1565.145,-1564.368,-1563.895,-1563.516,-1563.190,-1562.935,-1562.717,-1562.425,-1562.360,-1562.110,-1561.440,-1560.570,-1560.560,-1560.354,-1559.583,-1559.163,-1558.752,-1558.092,-1557.660,-1557.969,-1557.821,-1556.936,-1556.021,-1555.320,-1554.972,-1554.835,-1555.058],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'soma': {
              'x':[-100.099,-100.006,-99.913],
              'y':[789.764,790.057,790.349],
              'z':[-1572.953,-1572.599,-1572.245],
              'diam':[0.938,0.938,0.938]
          },

          prefix + 'apic[3]': {
              'x':[-37.420,-37.652,-36.842,-36.016],
              'y':[803.394,803.542,803.960,804.321],
              'z':[-1599.589,-1598.487,-1598.062,-1597.293],
              'diam':[0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[4]': {
              'x':[-36.016,-34.844,-34.025,-33.395,-31.221,-29.694,-28.675,-27.467,-25.916,-24.916,-24.136,-22.951,-21.226,-20.135,-19.087,-17.901,-16.909,-15.942,-14.966,-13.105,-11.905,-11.042,-9.918,-8.659,-7.144,-6.069,-4.901,-3.969,-3.050,-1.983,-0.867,0.221,1.503,2.878,4.185,5.009,5.918,6.862,7.781,8.542,9.518,10.321,11.376,12.183,12.973,14.061,15.275,16.292,17.239,18.396,19.045,21.063,22.377,23.520,24.566,25.565,27.168,28.135,29.137,29.475,30.045,31.614,32.593,33.411,34.518,35.543,37.023,38.992],
              'y':[804.321,804.995,806.126,806.965,807.594,807.722,807.893,808.298,808.650,809.223,809.758,810.290,810.588,810.659,810.786,811.227,811.755,812.336,812.920,813.556,814.138,814.488,814.642,814.790,815.108,815.524,816.272,816.790,817.169,817.835,818.496,819.023,819.218,819.390,819.779,820.296,820.755,821.192,821.793,822.536,823.475,823.957,824.484,824.935,825.374,825.923,826.608,827.327,827.680,828.303,829.060,829.846,830.598,831.274,831.458,831.581,831.935,832.292,833.147,834.410,835.253,835.918,836.458,837.010,837.266,837.324,837.463,837.558],
              'z':[-1597.293,-1597.011,-1596.707,-1596.846,-1597.667,-1598.207,-1598.394,-1598.205,-1598.212,-1598.016,-1597.635,-1596.947,-1597.079,-1597.270,-1597.483,-1597.321,-1597.071,-1596.846,-1596.629,-1597.005,-1596.929,-1596.508,-1596.201,-1596.606,-1597.314,-1597.832,-1598.002,-1597.714,-1597.342,-1596.637,-1595.957,-1595.795,-1596.213,-1596.627,-1596.508,-1596.158,-1595.817,-1595.484,-1595.242,-1595.111,-1594.600,-1594.208,-1593.420,-1593.010,-1592.580,-1591.822,-1591.241,-1591.310,-1591.626,-1591.623,-1591.465,-1592.332,-1592.621,-1592.673,-1592.914,-1593.039,-1593.084,-1592.716,-1592.212,-1591.954,-1592.001,-1592.281,-1592.041,-1591.700,-1591.414,-1591.009,-1590.968,-1591.849],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[1]': {
              'x':[-44.883,-43.567,-41.386,-39.090,-37.420],
              'y':[802.670,802.882,803.029,803.216,803.394],
              'z':[-1595.676,-1596.241,-1597.209,-1598.540,-1599.589],
              'diam':[0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[8]': {
              'x':[-34.164,-35.937,-36.384,-36.924,-37.509,-37.915,-38.213,-38.562,-39.083,-39.572,-39.924,-40.398,-40.862,-41.345,-41.825,-42.134,-42.385,-42.780,-43.183,-43.282,-43.416,-43.635,-44.173,-44.792,-45.213,-45.774,-46.356,-46.811,-47.104,-47.546,-48.128,-48.558,-48.914,-49.143,-49.210,-49.356,-49.762,-50.192,-50.518,-50.650,-50.842,-51.097,-51.229,-51.534,-52.208,-52.880,-53.480,-53.990,-54.439,-54.689,-54.769,-54.859,-55.218,-55.746,-56.425,-57.038,-57.824,-58.518,-58.966,-59.012,-58.575,-58.518,-58.685,-59.040,-59.536,-60.130,-60.550,-60.799,-60.872,-60.775,-60.154,-59.381,-58.776,-58.232,-57.964,-57.883,-57.902,-57.755,-57.701,-57.554,-57.355,-56.960,-55.136,-53.927,-52.762,-51.810,-50.841,-50.143,-49.483,-48.817,-48.246,-47.489,-46.736,-45.585],
              'y':[818.260,821.601,822.344,823.338,824.518,825.729,826.941,828.119,829.180,830.254,831.435,832.506,833.533,834.568,835.601,836.777,837.877,838.801,839.750,840.969,842.183,843.413,844.375,845.290,846.456,847.517,848.539,849.619,850.659,851.605,852.629,853.820,855.070,856.366,857.652,858.945,860.209,861.452,862.712,864.011,865.278,866.506,867.805,869.075,870.313,871.549,872.780,874.000,875.262,876.537,877.847,879.104,880.293,881.538,882.806,884.038,885.232,886.428,887.623,888.874,890.016,891.292,892.565,893.838,894.937,895.765,896.730,897.824,899.081,900.376,901.670,902.834,904.106,905.418,906.710,907.975,909.214,910.518,911.820,913.121,914.427,915.660,916.198,916.644,917.378,918.436,919.299,919.969,920.717,921.838,923.012,924.205,924.900,925.428],
              'z':[-1612.502,-1615.456,-1616.443,-1617.091,-1617.431,-1617.732,-1618.153,-1618.591,-1619.168,-1619.749,-1620.179,-1620.799,-1621.477,-1622.144,-1622.797,-1623.300,-1623.968,-1624.817,-1625.611,-1626.187,-1626.657,-1627.146,-1627.814,-1628.495,-1628.923,-1629.493,-1630.101,-1630.694,-1631.399,-1632.208,-1632.794,-1633.166,-1633.369,-1633.479,-1633.300,-1633.134,-1633.175,-1633.359,-1633.623,-1633.706,-1633.964,-1634.302,-1634.406,-1634.609,-1634.599,-1634.598,-1634.719,-1634.951,-1635.092,-1635.201,-1635.110,-1635.141,-1635.554,-1635.591,-1635.323,-1635.391,-1635.419,-1635.600,-1635.947,-1636.123,-1635.644,-1635.408,-1635.205,-1635.145,-1635.597,-1636.440,-1637.236,-1637.949,-1638.329,-1638.784,-1639.155,-1638.875,-1638.719,-1638.764,-1639.263,-1639.807,-1640.322,-1640.712,-1641.000,-1641.079,-1641.152,-1641.247,-1641.782,-1641.660,-1641.101,-1640.729,-1640.125,-1639.856,-1639.664,-1639.220,-1638.818,-1638.581,-1638.420,-1637.697],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[2]': {
              'x':[-37.420,-36.014,-35.913,-36.096,-35.984,-35.405,-34.057,-32.956,-32.030,-31.593,-30.390,-29.945,-29.606,-28.757,-27.663,-26.746,-26.277,-26.192,-25.211,-24.869,-24.580,-23.767,-23.746,-22.931,-22.168,-21.508,-20.195,-19.236,-18.504,-17.222,-15.713,-14.183,-13.491,-13.424,-13.356,-12.432,-11.969,-10.894,-10.190,-9.156,-8.441,-8.167,-7.672,-6.899,-6.032,-5.062,-4.075,-3.326,-2.698,-2.254,-2.155,-2.211,-1.431,-0.390,0.499,1.057,1.794,3.685,5.716,6.935],
              'y':[803.394,803.648,803.894,803.657,803.310,803.133,803.206,803.322,803.540,803.352,803.214,803.431,803.744,803.862,803.998,804.102,804.265,804.540,804.831,804.657,804.123,804.088,804.287,804.550,804.495,804.394,804.420,804.495,804.372,804.098,804.078,804.164,804.215,804.180,804.287,804.406,804.719,805.201,805.164,804.901,804.656,804.436,804.260,804.322,804.373,804.420,804.451,804.529,804.899,805.305,805.350,805.196,805.081,805.000,804.905,804.678,804.553,804.584,804.519,804.294],
              'z':[-1599.589,-1600.801,-1601.791,-1603.161,-1604.125,-1605.347,-1606.451,-1607.457,-1608.931,-1610.103,-1611.680,-1612.901,-1614.008,-1614.897,-1615.927,-1616.852,-1618.082,-1619.080,-1620.518,-1621.643,-1623.154,-1624.558,-1625.548,-1626.925,-1628.293,-1629.064,-1630.161,-1631.126,-1632.498,-1634.036,-1635.180,-1636.378,-1637.220,-1638.257,-1639.290,-1640.778,-1641.986,-1643.415,-1644.734,-1646.206,-1647.528,-1648.625,-1649.849,-1651.268,-1652.712,-1653.718,-1654.708,-1655.586,-1656.858,-1658.001,-1659.062,-1660.535,-1661.914,-1662.899,-1663.825,-1665.081,-1666.367,-1667.620,-1668.838,-1669.606],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[6]': {
              'x':[-44.883,-45.184,-44.677,-44.325,-43.103,-42.581,-42.379,-42.058,-41.859,-41.582,-41.302,-40.052,-39.329,-38.808,-38.052,-37.378,-36.889,-36.686,-36.505,-36.119,-35.223,-34.164],
              'y':[802.670,803.972,805.314,806.619,807.435,808.154,808.861,809.605,810.344,811.074,811.772,812.465,813.189,813.893,814.254,814.987,815.742,816.417,817.073,817.614,817.900,818.260],
              'z':[-1595.676,-1595.701,-1595.966,-1596.471,-1597.531,-1598.456,-1599.205,-1599.991,-1600.720,-1601.471,-1602.300,-1603.635,-1604.666,-1605.607,-1606.332,-1607.317,-1608.166,-1608.970,-1609.787,-1610.793,-1611.624,-1612.502],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[7]': {
              'x':[-34.164,-33.227,-33.025,-32.832,-33.075,-32.089,-31.155,-30.379,-29.809,-28.965,-28.871,-28.591,-28.320,-28.189,-27.933,-27.695,-27.606,-27.470,-26.198,-25.554,-25.481,-24.275,-23.376,-22.778,-21.974,-21.742,-21.438,-21.359,-20.980,-20.240,-19.447,-18.990,-19.035,-18.662,-17.671,-16.564,-15.843,-15.565,-15.402,-15.231,-15.095,-15.139,-14.198,-13.722,-13.706,-13.870,-13.911,-13.857,-13.786,-13.753,-13.629,-13.565,-13.496,-13.526,-13.595,-13.486,-13.355,-13.294,-13.160,-12.897],
              'y':[818.260,819.022,819.744,820.419,821.368,821.635,821.765,822.112,822.604,822.950,823.360,823.736,824.251,824.858,825.551,826.205,826.692,827.074,827.580,828.182,828.988,829.405,829.630,830.164,830.786,831.298,831.941,832.558,833.016,833.174,833.279,833.582,834.148,834.338,834.437,834.559,834.708,835.128,835.686,836.382,836.925,837.014,837.193,837.799,838.621,839.240,839.614,839.850,839.796,839.570,839.322,839.246,839.554,840.205,841.060,842.107,842.880,843.340,843.885,844.408],
              'z':[-1612.502,-1613.600,-1614.332,-1615.069,-1616.114,-1616.920,-1617.851,-1619.131,-1620.283,-1621.676,-1622.627,-1623.695,-1624.656,-1625.471,-1626.297,-1627.124,-1628.043,-1629.035,-1630.544,-1631.657,-1632.913,-1634.409,-1635.292,-1636.429,-1637.626,-1638.601,-1639.478,-1640.261,-1641.349,-1642.222,-1643.118,-1644.312,-1645.661,-1646.850,-1647.824,-1648.865,-1649.705,-1650.760,-1651.645,-1652.390,-1653.245,-1654.709,-1656.076,-1657.037,-1658.267,-1659.501,-1660.934,-1661.939,-1662.964,-1663.949,-1664.967,-1666.009,-1666.970,-1668.281,-1669.419,-1670.453,-1671.752,-1672.670,-1673.538,-1674.517],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },

          prefix + 'apic[0]': {
              'x':[-99.632,-98.136,-96.886,-95.160,-93.798,-92.148,-90.845,-90.049,-88.213,-87.070,-85.821,-84.335,-83.123,-82.223,-81.100,-79.519,-77.779,-76.354,-75.186,-73.941,-72.611,-71.399,-70.276,-68.829,-67.946,-66.305,-65.124,-63.655,-62.052,-60.570,-59.320,-58.233,-57.104,-55.825,-54.180,-52.574,-51.540,-50.502,-48.216,-47.148,-44.883],
              'y':[790.115,790.387,790.884,791.737,792.104,792.309,792.429,792.665,793.170,793.583,793.988,794.359,794.754,795.158,795.520,795.801,796.046,796.293,796.579,796.870,797.128,797.381,797.627,798.139,798.399,798.685,798.943,799.197,799.457,799.730,800.017,800.272,800.474,800.631,800.846,801.116,801.411,801.949,802.245,802.352,802.670],
              'z':[-1572.739,-1573.659,-1574.507,-1575.736,-1576.664,-1577.867,-1579.000,-1580.421,-1581.947,-1582.564,-1583.250,-1584.092,-1584.860,-1585.494,-1586.108,-1586.817,-1587.559,-1588.059,-1588.378,-1588.762,-1589.237,-1589.605,-1589.937,-1589.969,-1589.520,-1589.588,-1589.936,-1590.515,-1591.181,-1591.715,-1592.071,-1592.316,-1592.554,-1592.918,-1593.604,-1594.298,-1594.572,-1594.343,-1594.932,-1595.115,-1595.676],
              'diam':[0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592,0.592]
          },


        }