# Build the sphinx docker container (skips if have already)
docker build ../docker/documentation/. -t ob-sphinx-docs:1.0

# Cause a rebuild of all .md files
touch *.md

# the make script assumes 'html' folder instead of 'docs'
# it also expects the .md files to be under /docs/source
# So:
#   we copy the .md files to the source folder
#   then, rename docs to html
#   run the make file to generate the html from .md files
#   clean up by restoring the original folder names e.g. doc
mkdir ../docs/source
cp -a . ../docs/source
mv ../docs ../html
cd ../html # We're now in [repo]/html

# Run docker sphix container to build the docs
docker run \
    -it \
    -v $(readlink -f ../neuronunit):/neuronunit \
    -v $(readlink -f .):/html \
    -v $(readlink -f ../olfactorybulb):/olfactorybulb \
    ob-sphinx-docs:1.0
    /bin/bash

#docker run -it -v $(readlink -f ../neuronunit):/neuronunit -v $(readlink -f .):/html -v $(readlink -f ../olfactorybulb):/olfactorybulb ob-sphinx-docs:1.0 sphinx-apidoc -o source /neuronunit -s md && /bin/bash

#    \
#    sphinx-apidoc -o source /olfactorybulb -s md && \
#    sphinx-apidoc -o source /neuronunit -s md && \
#    make html

# Cleanup
cd ..
mv html docs
rm -rf docs/source
cd docs-source
