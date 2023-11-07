import discord
from discord.ext import commands, tasks
from db import DatabaseController
import random

class Client(commands.Bot):
    def __init__(self, controller: DatabaseController):
        super().__init__(command_prefix="/", intents=discord.Intents().all())
        self.cogslist = ["init", "start", "stop", "cancel", "join"]

        self.controller = controller

    @tasks.loop(seconds=10)
    async def follow_profits(self):
        messages = self.controller.get_messages_to_follow_profit()
        for message in messages:
            profit = random.randint(-100, 300)
            if profit >= 0:
                    embed = discord.Embed(
                    title=f"{message.strategy_name}",
                    description=f"Profit: {profit}%",
                    color=0x00FF00
                )
            else:
                embed = discord.Embed(
                    title=f"{message.strategy_name}",
                    description=f"Profit: {profit}%",
                    color=0xFF0000
                )
            message_to_edit = await self.get_channel(message.channel_id).fetch_message(message.message_id)
            await message_to_edit.edit(embed=embed)
        
    async def on_ready(self):
        print(" Logged in as " + self.user.name)
        synced = await self.tree.sync()
        print(" Slash CMDs Synced " + str(len(synced)) + " Commands")
        await self.follow_profits.start()
        
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension("cogs." + ext)

    async def example_usage(self):
        return self.controller.get_strategy_by_discord_id(1)
    
    
