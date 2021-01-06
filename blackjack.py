import discord
import random
from discord.ext import commands

class Blackjack:
    def __init__(self,card,switch):
        self.card=card
        self.switch=switch

p1=Blackjack(0,True)
p2=Blackjack(0,True)  

client =  commands.Bot(command_prefix=">")

@client.event
async def on_ready():
    print("IM ready bitch")
@client.command()
async def hitp2(ctx):
  
    await ctx.send("You have decided to hit")
    rand_count=random.randint(1,10)
    if (p1.switch=True):
        p1.card+=rand_count
    
        if(p1.card>21):
            await ctx.send(f"You have exceeded 21 and have lost \n TAke ThE L \n {ctx.author} loses")
            p1.card=0
            p2.card=0
            p2.switch=True
            p2.switch=False
        else: 
             await ctx.send(f"{p1.card} is the current score")
    else:
        await ctx.send("You decided to stand earlier remember!! \nYou cannot hit after choosing to stand")
@client.command()
@client.command()
async def hitp2(ctx):
  
    await ctx.send("You have decided to hit")
    rand_count=random.randint(1,10)
    if (p2.switch=True):
        p2.card+=rand_count
    
        if(p2.card>21):
            await ctx.send(f"You have exceeded 21 and have lost \n TAke ThE L \n {ctx.author} loses")
            p1.card=0
            p2.card=0
            p2.switch=True
            p2.switch=False
        else: 
             await ctx.send(f"{p2.card} is the current score")
    else:
        await ctx.send("You decided to stand earlier remember!! \nYou cannot hit after choosing to stand")
@client.command()
async def standp1(ctx):

    await ctx.send("You have decided to stand")
    p1.switch=False
    await ctx.send("You can no longer hit.")

@client.command()
async def standp2(ctx):

    await ctx.send("You have decided to stand")
    p2.switch=False
    await ctx.send("You can no longer hit.")
@client.command()
async def doublep1(ctx):

    await ctx.send("Decided to Double down huh , I dig that\n so now you can no longer hit")


client.run('NzgyMTY0NDkyMjc2NTk2NzU3.X8INcg.GQcvOa9f7gh1glBJO88VGfKichc')




