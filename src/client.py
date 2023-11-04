import discord
from discord.ext import commands
from db import DatabaseController


class Client(commands.Bot):
    def __init__(self, controller: DatabaseController):
        super().__init__(command_prefix="/", intents=discord.Intents().all())
        self.cogslist = ["init", "start", "stop", "cancel", "join"]

        self.controller = controller

    async def on_ready(self):
        print(" Logged in as " + self.user.name)
        synced = await self.tree.sync()
        print(" Slash CMDs Synced " + str(len(synced)) + " Commands")
    
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension("cogs." + ext)

    async def example_usage(self):
        return self.controller.get_strategy_by_discord_id(1)
