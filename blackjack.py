import discord
import random
from discord.ext import commands

class Blackjack:
    def __init__(self,player1,player2,rand_count):
        self.player1=player1
        self.player2=player2
        self.rand_count=rand_count
    

client =  commands.Bot(command_prefix=">")
switch = True
@client.event
async def on_ready():
    print("IM ready bitch")
@client.command()
async def hitp1(ctx):
    player1_count = 0
    await ctx.send("You have decided to hit")
    await ctx.send(f"{player1_count} is the amt")
    rand_count=random.randint(1,10)
    player1_count+=rand_count
    if(player1_count>21):
        await ctx.send("You have exceeded 21 and have lost \n TAke ThE L")
        switch=False
    else: 
        await ctx.send(f"{player1_count} is the current number")
        switch = True
@client.command()
async def hitp2(ctx):
    player2_count = 0
    await ctx.send("You have decided to hit")
    rand_count=random.randint(1,10)
    player2_count+=rand_count
    if(player2_count>21):
        await ctx.send("You have exceeded 21 and have lost \n TAke ThE L")

client.run('NzgyMTY0NDkyMjc2NTk2NzU3.X8INcg.fZrEL4I3_FiWBGjz_v-VtLH9mQg')




