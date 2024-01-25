from typing import Optional
import disnake
from disnake.ext import commands

#command_prefix=commands.when_mentioned

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all(), test_guilds=[YOU CLIENT ID])


CENSORED_WORDS = ["бла", "бла"]


@bot.event
async def on_message( message ):
    msg = message.conetent.lower()


@bot.event
async def on_ready():
    print(f"Bot {bot.user} готов к работе")

@bot.event
async def on_member_join(member):
    role = await disnake.utils.get(guild_id=member.guild.id, role_id=1194548395705106474)
    channel= member.guild.system_channel

    embed = disnake.Embed(
        title="Новый member",
        description=f"{member.name}#{member.discriminator}",
        color=0xffffff

    )

    await member.add_roles(role)
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                await message.delete()
                await message.channel.send(f"{message.author.mention} - такие слова запрещены!")


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас нет прав на это действие")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f"Правельное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExaple: {ctx.prefix}{ctx.command.usage}"
        ))


@bot.event
async def ask_ready():
    print(f"Bot {bot.user} забанить")


@bot.command(name="кик", brief="Это команда выгоняет участника из сервера но не банет", usage="кик <@user> <reason=None>")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил"):
    await ctx.send(F"Админ, {ctx.author.mention} пользователь исключен {member.mention}", delate_after=5)
    await member.kick(reason=reason)
    await ctx.message.delete.delete()


@bot.command(name="бан", aliases=["пошел нахуй", "подумай"], brief="Это команда банят участника из сервера но не кикает будь внимателен", usage="бан <@user> <reason=None>")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил"):
    await ctx.send(F"Админ, {ctx.author.mention} пользователь забанин {member.mention}", delate_after=5)
    await member.ban(reason=reason)
    await ctx.message.delete.delete()


@bot.command( pass_context = True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)


token = open( 'token.txt', 'r' ).readline()

bot.run(token)