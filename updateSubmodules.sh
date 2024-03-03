git submodule update --init --recursive --remote
git pull && git submodule foreach git pull origin automated-updates
cd database
git pull origin automated-updates
cd ..
git add database
git commit -m "Updating submodule to latest commit"
git push origin main

