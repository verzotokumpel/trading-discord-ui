
def is_owner():
    def predicate(ctx):
        owner = ctx.channel.owner_id
        if owner == ctx.author.id:
            return True
        return predicate