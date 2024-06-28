from Helpers.TelegramHelper import TelegramHelper
import Helpers.Utils as Utils
import time
from git import Repo
import os
import asyncio
    
class RepoManager():
    def __init__(self, settings):
        self.logger = Utils.GetMeLogger(settings["log_token"])

        self.settings = settings
        self.telegramHelper = TelegramHelper(settings, self.logger)

        self.isTradingOn = False
        self.task = None


    async def StartListeningToMessages(self):
        print("Oh Lord, please bless me with your kind and forgiving words.")
        await self.telegramHelper.send_message("Oh Lord, please bless me with your kind and forgiving words.")
        close = 0

        # Main infinite loop to listen to messages.
        while(close == 0):
            if(self.task != None):
                if(self.task.done()):
                    self.isTradingOn = False
            updates = await self.telegramHelper.get_update_commands()

            if(len(updates) > 0):
                for update in updates:
                    # If not authenticated then skip this message
                    if(not await self.AuthenticateMessage(update)):
                        continue

                    # User is authorized and the command is valid and implemented.
                    await self.telegramHelper.send_message("Oh lord,\nThank you for your command.\nYour command is my wish and I shall fulfill it.\nAmen.")
                    
                    await self.ProcessCommand(update["text"])
                
                await self.telegramHelper.set_latest_update_id()

            time.sleep(1)


    async def AuthenticateMessage(self, update):
        implemented_commands = ["deploylatest@GoingInTradeBot"]

        message = update["text"].split()

        # If it is sent by authorized user and is a command by without password then send shit and continue
        if(message[-1] != self.settings["password"]):
            #print("If it is sent by authorized user and is a command by without password then send shit and continue")
            await self.telegramHelper.send_message("Who the fuck do you think you are, giving me commands!!\nI only listen to my gods commands!")
            return False

        # If the command is created in telegram but not implemented send message and continue
        if(message[0][1:] not in implemented_commands):
            #print("If the command is created in telegram but not implemented send message and continue")
            await self.telegramHelper.send_message("Oh help me god, that I have yet to learn this command.\nForgive me for my sins and protect me from the worldly powers.\nAmen.")
            return False
        
        return True
    

    async def ProcessCommand(self, command_sent):
        command = command_sent.split()
        #print(command)
        if(command[0][1:] == "deploylatest@GoingInTradeBot"):
            if(not self.isTradingOn):
                await self.DeployLatest()
            else:
                await self.telegramHelper.send_message("The trading is already going on. Please close it to deploy latest.")
        
    async def DeployLatest(self):
        self.logger.info("Trying to take latest of AutomatedTrading and starting it.")
        
        repo = Repo(self.settings["repo_location"])
        fetch_info = repo.remotes.origin.pull()
        
        self.logger.info("Took latest of the repo, now turning it on")

        self.task = asyncio.create_task(self.Deploy())

        self.isTradingOn = True

        self.logger.info("Ran the Trading manager")

    async def Deploy(self):
        os.chdir(self.settings["repo_location"])
        os.system("python Main.py")
    




"""
    Example update object:
    {
      "update_id": 627443265,
      "message": {
        "message_id": 1557,
        "from": {
          "id": 123455,
          "is_bot": false,
          "first_name": "SgtBurns",
          "username": "sgtBurns07",
          "language_code": "en"
        },
        "chat": {
          "id": 123455,
          "first_name": "SgtBurns",
          "username": "sgtBurns07",
          "type": "private"
        },
        "date": 123455,
        "text": "/start",
        "entities": [
          {
            "offset": 0,
            "length": 6,
            "type": "bot_command"
          }
        ]
      }
    }"""