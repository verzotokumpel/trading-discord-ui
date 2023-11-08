from discord.ext import commands
from discord import app_commands
import discord
from client import Client
from db import StrategyStatus
from decorators.is_owner import is_owner


class Start(commands.Cog):
  def __init__(self, client: Client):
    self.client = client

  @app_commands.command(name="start", description="If you are owner use it to start strategy")
  @app_commands.check(is_owner)
  async def start(self, interaction: discord.Interaction, method: str):
    fetched_status = self.client.controller.get_strategy_status(interaction.channel_id)
    if fetched_status[0] == "INITIALIZED":
      self.client.controller.change_status(interaction.channel_id, StrategyStatus.OPENED)
      embed = discord.Embed(
        title=f"{interaction.channel}",
        description="Profit: 0",
        color=0x00FF00
      )
      embed.add_field(name="Command used by owner:", value=f"{method}", inline=False)
      await interaction.response.send_message(embed=embed)
      message = await interaction.original_response()
      await message.pin()
      self.client.controller.add_message_to_follow_profit(message.id, str(interaction.channel), interaction.channel_id, method)
    else:
      embed = discord.Embed(
        title="ERROR",
        description="Strategy not initialized or already started.",
        color=0x00FF00
      )
      await interaction.response.send_message(embed=embed)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(Start(client))