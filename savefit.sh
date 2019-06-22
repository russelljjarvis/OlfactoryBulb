git checkout master
git pull

cd prev_ob_models/Birgiolas2020/Mechanisms
nrnivmodl
cd ~/OlfactoryBulb

branch_name=fit-`date +%Y-%m-%d-%H-%M-%S`
git branch $branch_name
git checkout $branch_name

cd notebooks
jupyter nbconvert fitting.ipynb --to python
xvfb-run ipython fitting.py $1 | tee /dev/tty > fitting.txt

git add .
git commit -m 'fit results'

git remote set-url origin https://github.com/JustasB/OlfactoryBulb.git
git push origin $branch_name

git checkout master

#sudo poweroff
