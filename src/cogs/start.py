from discord.ext import commands
from discord import app_commands
import discord

class Start(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="start", description="If you are owner use it to start strategy")
  async def hello(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(Start(client))