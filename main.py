import discord
from discord.ext import commands
import token_store
from discord.utils import get

standard_roles = ['dj']

bot = commands.Bot(command_prefix='$')


# Commands##############################################################################################################
@bot.command(pass_context=True)
async def check_standard_roles(ctx):
    message = ""
    for member in ctx.guild.members:
        message_end = '\n'
        for role_name in standard_roles:
            role = get(ctx.guild.roles, name=role_name)
            if role in member.roles:
                message_end += (role_name + ' :white_check_mark:     ')
            else:
                message_end += (role_name + ' :x:     ')
        message += '**' + member.name + '**' + message_end + '\n'
    await ctx.send(message)


@bot.command()
async def update(ctx):
    await update_all(ctx.guild)
    await ctx.send('Updated this guild!')


# Events################################################################################################################
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    for guild in bot.guilds:
        await update_all(guild=guild)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.event
async def on_member_join(member):
    await member.add_roles_check(standard_roles)


# General functions#####################################################################################################
async def update_all(guild):
    for member in guild.members:
        await member.add_roles_check(standard_roles)


async def add_roles_check(self, role_names):
    for role_name in role_names:
        role = get(self.guild.roles, name=role_name)
        if not (role in self.roles):
            await self.add_roles(role)


discord.Member.add_roles_check = add_roles_check

bot.run(str(token_store.token))
