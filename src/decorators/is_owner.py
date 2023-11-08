import discord

def is_owner(interaction: discord.Interaction) -> bool:
    interaction.response.send_message("Hello")
    return interaction.channel.owner.id == interaction.user.id