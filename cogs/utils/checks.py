from discord.ext import commands


# Checks
async def check_guild_permissions(ctx, perms, *, check=all):
    if ctx.guild is None:
        return False
    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def is_admin():
    """Checks if the author has administrator permission"""
    async def predicate(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})
    return commands.check(predicate)


def is_owner():
    """Checks if the author is the bot's owner"""
    async def predicate(ctx):
        return await ctx.bot.is_owner(ctx.author)
    return commands.check(predicate)
