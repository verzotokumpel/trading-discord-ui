from discord.ext import commands
from discord import app_commands
import discord
from db import Strategy, StrategyStatus
from uuid import uuid4
from datetime import datetime

class Init(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="init", description="If you are owner use it to initialize strategy")
  async def init(self, interaction: discord.Interaction, amount: str):
    if amount.isnumeric() and int(amount) > 0 and amount.lstrip('0') == amount:
      embed=discord.Embed(
        title=f"{interaction.channel}",
        description="Status: waiting for owner to run strategy.",
        color=0xe67e22   
        )
      embed.add_field(name="Time to join now", value="Use !join [value]", inline=False)
      embed.add_field(name="Owner: ", value=f"owner", inline=False)
      embed.add_field(name="Owner position: ", value=f"{amount}$", inline=False)
      await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(Init(client))