import discord
from discord.ext import commands

client =  commands.Bot(command_prefix=">")

player1_count=0
dealer_count=0
rand_count=0;
@client.event
async def on_ready():
    print("IM ready bitch")
@client.commant()
async def hit(ctx)
    await ctx.send("You have decided to hit")
    rand_count=random.randint(1,10)
    player1_count+=rand_count
    if(player1_count>21):
        player1_count=0
        await.ctx.send("You have exceeded 21 and have lost \n TAke ThE L")
    

