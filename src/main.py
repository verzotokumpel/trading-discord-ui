import asyncio
from db import DatabaseController, Strategy, StrategyStatus
from uuid import uuid4
from datetime import datetime
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

TOKEN = os.getenv("DISCORD_TOKEN")

async def main():
    controller = DatabaseController()

    example_strategy = Strategy(
        uuid4(), datetime.now(), 1, 1, "BTCUSDT", 100, StrategyStatus.INITIALIZED
    )
    controller.add_strategy(example_strategy)

    fetched_strategy = controller.get_strategy_by_discord_id(1)
    print(fetched_strategy)

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='/', intents=discord.Intents().all())
    self.cogslist = ["init", "start", "stop", "cancel", "join"]
    load_dotenv()

  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    synced = await self.tree.sync()
    print(" Slash CMDs Synced "+ str(len(synced)) + " Commands")

  async def setup_hook(self):
    for ext in self.cogslist:
      await self.load_extension("cogs."+ext)

client = Client()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    client.run(TOKEN)
    
