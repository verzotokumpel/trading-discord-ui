import discord

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.channel.owner.id == interaction.user.id