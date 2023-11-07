from discord.ext import commands
from discord import app_commands
import discord
from db import Strategy, StrategyStatus
from uuid import uuid4
from datetime import datetime
from client import Client

class Init(commands.Cog):
  def __init__(self, client: Client):
    self.client = client

  @app_commands.command(name="init", description="If you are owner use it to initialize strategy")
  async def init(self, interaction: discord.Interaction, amount: str, currency_ticker: str):
    if amount.isnumeric() and int(amount) > 0 and amount.lstrip('0') == amount:
      if self.client.controller.get_strategy_by_discord_id(interaction.channel_id) is None:
        strategy = Strategy(
          uuid4(), datetime.now(), interaction.channel_id, interaction.user.id, currency_ticker, int(amount), StrategyStatus.INITIALIZED
        )
        self.client.controller.add_strategy(strategy)
        embed=discord.Embed(
          title=f"{interaction.channel}",
          description="Status: waiting for owner to run strategy.",
          color=0xe67e22   
          )
        embed.add_field(name="Time to join now", value="Use !join [value]", inline=False)
        embed.add_field(name="Owner:", value=f"{self.client.get_user(interaction.user.id)}", inline=False)
        embed.add_field(name="Owner position: ", value=f"{amount}$", inline=False)
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.pin()
      else: 
        embed=discord.Embed(
          title=f"{interaction.channel}",
          description="Strategy alerady initialized or in progerss",
          color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(Init(client))