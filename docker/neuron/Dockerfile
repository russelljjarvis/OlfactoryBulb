# Start with a base Ubuntu image
FROM ubuntu:18.04

# Install packages required for NEURON and IV compilation
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libx11-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libxt-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install gnome-devel 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mpich 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libncurses-dev 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install xfonts-100dpi
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install make

# Install miniconda with python 3.7
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh
RUN bash miniconda.sh -p /miniconda -b
RUN rm miniconda.sh
ENV PATH=/miniconda/bin:${PATH}

# Create Python environment named 'p3'
RUN conda create -n p3 -c anaconda python=3.5.3
ENV PATH /opt/conda/envs/p3/bin:$PATH
RUN /bin/bash -c "source activate p3"

# Install libraries required for NEURON compilation
RUN pip install --upgrade pip
RUN pip install scipy numpy matplotlib cython mpi4py

# Download NEURON and IV tarballs
RUN curl -o nrn.tar.gz https://neuron.yale.edu/ftp/neuron/versions/v7.7/nrn-7.7.tar.gz
RUN curl -o iv.tar.gz https://neuron.yale.edu/ftp/neuron/versions/v7.7/iv-19.tar.gz

# Extract tarballs into known locations
RUN tar -xvzf nrn.tar.gz
RUN tar -xvzf iv.tar.gz
RUN rm *.tar.gz
RUN mkdir ~/neuron
RUN mv nrn-7.7 ~/neuron/nrn
RUN mv iv-19 ~/neuron/iv

# Compile IV and NEURON with Python and MPI
RUN cd ~/neuron/iv && \
    ./configure --prefix=`pwd` && \
    make && \
    make install && \
    cd ~/neuron/nrn && \
    python_loc=$(which python) && \
    ./configure --prefix=`pwd` --with-iv=$HOME/neuron/iv --with-paranrn --with-nrnpython=$python_loc && \
    make && \
    make install

# Set up NEURON env variables
ENV HOME=/root
ENV IV=$HOME/neuron/iv
ENV N=$HOME/neuron/nrn
ENV CPU=x86_64
ENV PATH="$IV/$CPU/bin:$N/$CPU/bin:$PATH"

# Install NEURON library
RUN cd ~/neuron/nrn/src/nrnpython/ && \
    python setup.py install

# Install packages required for the model
RUN pip install jupyter
EXPOSE 8888 8888

# Remove packages that are not needed to run NEURON
RUN apt-get -y remove libxt-dev gnome-devel libncurses-dev 
RUN apt -y autoremove --purge
RUN conda clean --all -y
