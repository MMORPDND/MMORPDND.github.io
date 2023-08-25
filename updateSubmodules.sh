git submodule update --recursive --remote
git pull && git submodule foreach git pull origin main
cd database
git pull origin main
cd ..
git add database
git commit -m "Updating submodule to latest commit"
git push origin main

