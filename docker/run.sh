xhost +local:root

docker run \
    -it \
    -p 8888:8888 \
    -v $(readlink -f ../):/OlfactoryBulb \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    neuron:7.7

xhost -local:root
