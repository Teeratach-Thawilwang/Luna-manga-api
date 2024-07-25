import os

configfiles = []
configsPath = "app/Settings"
if os.path.exists(configsPath) and os.path.isdir(configsPath):
    for fileName in os.listdir(configsPath):
        if fileName == "settings.py":
            continue
        if fileName.endswith(".py"):
            configfiles.append(fileName[0:-3])

    with open(configsPath + "/settings.py", "w") as fp:
        for configFile in configfiles:
            fp.write("from app.Settings.%s import *\n" % configFile)

from app.Settings.settings import *
