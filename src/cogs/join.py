from discord.ext import commands
from discord import app_commands
import discord
from client import Client
from db import Contribution, StrategyStatus
from uuid import uuid4
from datetime import datetime

class useStrategy(discord.ui.View):
    def __init__(self, amount, user, client):
      super().__init__(timeout=None)
      self.amount = amount
      self.user = user
      self.client = client

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.success)
    async def join(self, interaction, button):
        if interaction.user.id == self.user.id:
          user=interaction.user
          strategyName = interaction.message.channel.name
          strategyId = interaction.message.channel.id
          fetched_positon_value = self.client.controller.get_user_positon_value(interaction.channel_id, interaction.user.id)
          fetched_status = self.client.controller.get_strategy_status(interaction.channel_id)
          if fetched_status == StrategyStatus.INITIALIZED:
            if fetched_positon_value:
              self.client.controller.change_contribution_value(self.amount, interaction.user.id, interaction.channel_id,)
            else:
              contribution = Contribution(
              uuid4(), datetime.now(), interaction.channel_id, interaction.user.id, int(self.amount),
              )
              self.client.controller.add_contribution(contribution)

            await interaction.response.send_message("Submited")
            await user.send(f"Your position is open now! \nuser:{user} \nname: {strategyName} \nid: {strategyId} \nvalue: {self.amount}")
          else:
             await interaction.response.send_message("You can't join strategy now. It's cancelled or already started.")

class Join(commands.Cog):
  def __init__(self, client: Client):
    self.client = client

  @app_commands.command(name="join", description="If strategy is initialized by owner, use it to contribute.")
  async def join(self, interaction: discord.Interaction, amount: str):
    if amount.isnumeric() and int(amount) > 0 and amount.lstrip('0') == amount: 
      fetched_status = self.client.controller.get_strategy_status(interaction.channel_id)
      if fetched_status is None or fetched_status != StrategyStatus.INITIALIZED: 
        embed = discord.Embed(
        title="Error",
        description="It's to late for join or owner didn't initialized strategy yet",
        color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)     
      else:  
          fetched_positon_value = self.client.controller.get_user_positon_value(interaction.channel_id, interaction.user.id)
          embed = discord.Embed(
              title="Your Position Details",
              description="Check if all is correct!",
              color=0x00FF00
          )
          if fetched_positon_value:
              embed.add_field(name="Your position was: ", value=f"{fetched_positon_value[0]} USDC", inline=False)
              embed.add_field(name="Your position is going to be: ", value=f"{int(amount) + fetched_positon_value[0]} USDC", inline=False)
          else:
              embed.add_field(name="Total Value: ", value=f"{amount} USDC", inline=False)
          embed.add_field(name="Strategy Name:  ", value=f"{interaction.channel}", inline=False)
          await interaction.response.send_message(embed=embed, view=useStrategy(amount, interaction.user, self.client)) 
    else:
      embed = discord.Embed(
          title="Error",
          description="Provide positive number to join strategy. For example use !join 500",
          color=0xFF0000
      )
      await interaction.response.send_message(embed=embed) 


async def setup(client:commands.Bot) -> None:
  await client.add_cog(Join(client))