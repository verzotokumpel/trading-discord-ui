from discord.ext import commands
from discord import app_commands
import discord

class Cancel(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="cancel", description="If you are owner use it to cancel strategy")
  async def hello(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(Cancel(client))