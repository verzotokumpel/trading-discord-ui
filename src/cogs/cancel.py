from discord.ext import commands
from discord import app_commands
import discord
from client import Client
from db import StrategyStatus
from decorators.is_owner import is_owner

class Cancel(commands.Cog):
  def __init__(self, client: Client):
    self.client = client

  @app_commands.command(name="cancel", description="If you are owner use it to cancel strategy")
  @app_commands.check(is_owner)
  async def cancel(self, interaction: discord.Interaction):
    fetched_status = self.client.controller.get_strategy_status(interaction.channel_id)
    if fetched_status[0] == "INITIALIZED": 
      embed=discord.Embed(
        title=f"{interaction.channel}",
        description="Status: CANCELED",
        color=0xe67e22   
      )
      self.client.controller.change_status(interaction.channel_id, StrategyStatus.CANCELLED)
      await interaction.response.send_message(embed=embed)
    else:
      await interaction.response.send_message("You can cancel strategy only after initialize")
  
async def setup(client:commands.Bot) -> None:
  await client.add_cog(Cancel(client))