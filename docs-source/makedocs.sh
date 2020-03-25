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
cd ../html
make html
cd ..
mv html docs
rm -rf docs/source
