# This file features silly commands, do not judge!
from discord.ext import commands
import random


@commands.command()
async def penis(ctx):
    penis_variable = random.randint(0, 1)
    if penis_variable == 1:
        await ctx.send('Your penis is big')
    else:
        await ctx.send('Your penis is small')


@commands.command()
async def penis_l(ctx):
    rand_var = random.randint(1, 10)
    string_middle = ''
    for i in range(rand_var):
        string_middle += '='
    await ctx.send('8'+string_middle+'>')

commands = [penis, penis_l]

@bot.command()
async def buildjhin(ctx): # TODO: Hardcoded
    await ctx.send("Jhin 10.10 Core Build:")
    await ctx.send("Stormrazor")
    await ctx.send("Infinity Edge")
    await ctx.send("Rapid Firecannon")
    await ctx.send("----------------------------------------")
    await ctx.send("Boots: Swiftness")
    await ctx.send("Keystone: Fleet Footwork")
