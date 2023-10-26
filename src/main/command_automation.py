import os
from datetime import date
import time

def getDate():
    today = date.today()
    # mmddYYYY
    d1 = today.strftime("%m%d%Y")
    # print("d1 =", d1)
    return d1


getDate()

filepath = "data/statsOfGames/2023-2024-Season/Games/" + getDate();
copyFromPath = filepath;
copyToPath = "~/miniProj/dataNbaSim/data/2023-2024-Season/Games/";
copyCommand = "cp -R " + copyFromPath + " " + copyToPath;
changeDirectory = "cd ~/miniProj/dataNbaSim/data/";
gitAdd = "git add .";
gitCommit = "git commit -m \"PROBABILITY-UPDATE\""; 
gitPush = "git push";

os.system(copyCommand)
time.sleep(0.25)
os.system(changeDirectory)
os.system(gitAdd)
time.sleep(0.25)
os.system(gitCommit)
time.sleep(0.25)
os.system(gitPush)
time.sleep(0.25)
print("Complted Process")
