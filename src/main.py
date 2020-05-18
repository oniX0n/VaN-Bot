import discord
import asyncio
import sqlhandling
from discord.ext import commands
import token_store
from discord.utils import get
import sys

standard_roles = ['dj']
tracked_channels = []

db = sqlhandling.BotDb(sys.argv[1])
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


@bot.command()
async def penis(ctx):
    penisvariable=random.randint(0,1)
    if (penisvariable==1):
        await ctx.send("Dein Penis ist groß")
    else:
        await ctx.send("Dein Penis ist klein")


# Events################################################################################################################
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    for guild in bot.guilds:
        await update_all(guild=guild)
    bot.loop.create_task(check_tracked_channels_loop())


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await db.insert_message(author=message.author, content=message.content, channel=message.channel,
                            date_send=message.created_at)  # TODO: Not sure


@bot.event
async def on_member_join(member):
    await member.add_roles_check(standard_roles)


@bot.event
async def on_voice_state_update(member, before, after):
    channel = get(member.guild.channels, name='➕ New Channel')  # TODO: Hardcoded
    if (after.channel == channel) & (before.channel != channel):
        new_channel = await member.guild.create_voice_channel('Channel ' + member.name, position=channel.position + 1)
        tracked_channels.append(new_channel)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=str(len(tracked_channels)) + ' Channel(s)'))
        await member.move_to(new_channel)

    if (before.channel in tracked_channels) & (before.channel != after.channel):
        await check_tracked_channels()


# General functions#####################################################################################################
async def update_all(guild):
    for member in guild.members:
        await member.add_roles_check(standard_roles)


async def check_tracked_channels_loop():
    while True:
        await check_tracked_channels()
        await asyncio.sleep(20)


async def check_tracked_channels():
    for channel in tracked_channels:
        if len(channel.members) == 0:
            tracked_channels.remove(channel)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                name=str(len(tracked_channels)) + ' Channel(s)'))
            await channel.delete()


async def add_roles_check(self, role_names):
    for role_name in role_names:
        role = get(self.guild.roles, name=role_name)
        if not (role in self.roles):
            await self.add_roles(role)


discord.Member.add_roles_check = add_roles_check

bot.run(str(token_store.token))
