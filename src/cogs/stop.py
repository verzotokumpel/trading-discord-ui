from discord.ext import commands
from discord import app_commands
import discord
from client import Client
from db import StrategyStatus
import random


class Stop(commands.Cog):
  def __init__(self, client: Client):
    self.client = client

  @app_commands.command(name="stop", description="If you are owner use it to stop strategy")
  async def stop(self, interaction: discord.Interaction, method: str):
    fetched_status = self.client.controller.get_strategy_status(interaction.channel_id)
    if fetched_status[0] == "OPENED":
      self.client.controller.change_status(interaction.channel_id, StrategyStatus.CLOSED)
      embed = discord.Embed(
        title=f"{interaction.channel} stopped",
        description=f"Total profit: {random.randint(-100, 300)}%",
        color=0x00FF00
      )
      await interaction.response.send_message(embed=embed)
      message = await interaction.original_response()
      await message.pin()
      self.client.controller.remove_message_to_follow_profit(str(interaction.channel))
    else:
      embed = discord.Embed(
        title="ERROR",
        description="Strategy not initialized or already stopped.",
        color=0x00FF00
      )
      await interaction.response.send_message(embed=embed)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(Stop(client))