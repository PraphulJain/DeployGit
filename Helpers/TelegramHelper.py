from telegram import *
from telegram.ext import *
import asyncio
import traceback

class TelegramHelper:   

    def __init__(self, settings, logger):
        self.logger = logger
        self.bot_token = settings["bot_token"]
        self.chat_id = settings["chat_id"]
        self.authorized_users = settings["authorized_users"]
        self.update_id = 0

        # Setting the update_id to the current update
        asyncio.run(self.set_latest_update_id())

        # Getting the commands created in telegram
        bot = Bot(settings["bot_token"])
        response = asyncio.run(bot.getMyCommands()) 
        asyncio.run(self.stopBot(bot))
        self.my_commands = []
        for command in response:
            self.my_commands.append(command.command + "@GoingInTradeBot")


    async def refresh_my_commands(self):
        bot = Bot(self.bot_token)
        response = await bot.getMyCommands()
        await self.stopBot(bot)
        commands = []
        for command in response:
            commands.append(command.command)
    
        self.my_commands = commands


    async def send_trade_message(self, order_type, symbol, strat, lots, current_price):
        message = "{0} order:\n\n{1}\nLot size: {3}\nPrice: {4}\n\n{2}".format(order_type, symbol, strat, lots, current_price)
        await self.send_message(message)


    async def send_message(self, message):
        bot = Bot(self.bot_token)
        try:
            await bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as ex:
            self.logger.error(traceback.format_exc())
        await self.stopBot(bot)
        

    async def get_update_commands(self):
        response = await self.get_updates()
        #print(response)
        commands = []
        for update in response:
            # It will only return the updates from valid senders and chats.
            if(self.valid_sender(update)):
                update_info = {"text": update.message.text, "sender_id": update.message.from_user.id}
                commands.append(update_info)
    
        if(len(commands) == 0):
            await self.set_latest_update_id()

        return commands
    

    async def get_updates(self):
        bot = Bot(self.bot_token)
        updates = []
        try:
            updates = await bot.getUpdates(offset=self.update_id)
        except Exception as ex:
            self.logger.error(traceback.format_exc())
        await self.stopBot(bot)

        return updates


    # This method is basically like a firewall or setting a private network for our services which skips the invalid user messages or invalid commands.
    # Basically either 404/503/405 responses.
    def valid_sender(self, update):
        if(update == None):
            return False

        # If it is sent by bot or someone unauthorized or the chat is not the group chat or the message is not a command then skip
        if(update.message.from_user.is_bot == True 
            or update.message.from_user.id not in self.authorized_users
            or update.message.text == None      # In case of emojis this conditions is true
            or update.message.text[0] != '/'
            or update.message.chat.id != self.chat_id):
            if(update.message.from_user.id not in self.authorized_users):
                self.logger.error(update.message.from_user.id + " is trying to talk to this bot")
            return False
        
        command = update.message.text.split()[0][1:]
        if(command not in self.my_commands):
            return False
        
        return True

            
    async def set_latest_update_id(self):
        while(True):
            updates = await self.get_updates()
            if(len(updates) == 0):
                break
            
            self.update_id = updates[-1].update_id + 1
    
    async def stopBot(self, bot):
        try:
            await bot.shutdown()
        finally:
            return
