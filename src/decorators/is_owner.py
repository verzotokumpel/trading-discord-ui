from discord.ext import commands

def is_owner():
    def predicate(ctx):
        owner = ctx.channel.owner_id
        if owner == ctx.author.id:
            return True
        raise commands.CheckFailure("Permission denied")
    return commands.check(predicate)