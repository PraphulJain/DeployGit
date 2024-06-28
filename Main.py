import json
from RepoManager import RepoManager
import asyncio
import Helpers.Utils as Util

def main():
    Util.set_realtime_priority()

    settings = LoadSettings()

    tradingManager = RepoManager(settings)
    asyncio.run(tradingManager.StartListeningToMessages())

def LoadSettings():
    f = open("settings.json")
    data = json.load(f)
    f.close()
    return data

if __name__ == "__main__":
    main()