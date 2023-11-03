from discord.ext import commands
from discord import app_commands
import discord

class useStrategy(discord.ui.View):
    def __init__(self, amount, cur, user):
        super().__init__(timeout=None)
        self.amount = amount
        self.cur = cur
        self.user = user

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.success)
    async def join(self, interaction, button):
        if interaction.user.id == self.user.id:
            user=interaction.user
            strategyName = interaction.message.channel.name
            strategyId = interaction.message.channel.id
            await user.send(f"Your position is open now! \nuser:{user} \nname: {strategyName} \nid: {strategyId} \nvalue: {self.amount}")
            #here you can send message to trading platform

class Join(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="join", description="If strategy is initialized by owner, use it to contribute.")
  async def join(self, interaction: discord.Interaction, amount: str):
    await interaction.response.send_message("Hello!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(Join(client))