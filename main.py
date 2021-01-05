import random
from discord.ext import commands


custom = commands.Bot(command_prefix='!')

coins = ['ez']  # here are the coins
c = ['h', 't']
t = ['following blocks contain player names and their ids is the index ']
grid = ['1', '2', '3']


@custom.command()
async def h(ctx):
    await ctx.send('my commands are,  ')
    await ctx.send('!p "name" /to play  ')
    await ctx.send('!b "your id" /shows you your balance  ')
    await ctx.send('!f "number of coins" "h/t" "id" /creates a coinflip  ')
    await ctx.send('!g "number of coins" "column" "row" "id"/grid guess  ')
    await ctx.send('!i  /shows player names and their ids  ')
    await ctx.send('Rules:Everyone starts with a balance of 300 and first to 1000 coins wins')
    await ctx.send('if you get addicted to gambling and lose your shit contact @DreadArceus')


@custom.command()
async def p(ctx, arg1):
    temp1 = str(arg1)
    temprich = 'rich'
    if temprich in arg1:
        temp2 = 500  # coins rich mode
    else:
        temp2 = 300  # coins

    coins.append(temp2)
    t.append(temp1)
    i = t.index(temp1)
    await ctx.send(arg1 + '  has been added with ' + str(temp2) + ' coins, your id is ' + str(i))


@custom.command()
async def f(ctx, arg1, arg2, arg3):  # arg1=coins arg3=id
    temp3 = random.choice(c)
    if (int(coins[int(arg3)]) - int(arg1)) >= 0:

        if (temp3 == arg2):
            temp4 = 'you won the flip, coins are added to your balance'
            outcome = int(arg1)

        else:
            temp4 = 'scammed'
            outcome = -int(arg1)
        temp5 = int(coins[int(arg3)])
        temp6 = (temp5) + int(outcome)  # temp 5 is updated coin values
        if temp6 >= 1000:
            await ctx.send(t[int(arg3)] + ' wins the session')
        elif temp6 == 0:
            await ctx.send(t[int(arg3)] + ' is out')
        else:
            await ctx.send(t[int(arg3)] + ' your balance has been updated')

        coins[int(arg3)] = int(temp6)
        await ctx.send(temp4)

    else:
        await ctx.send('you really thought that would work?')
@custom.command()
async def game(ctx):
    emoji='<:python3:788673802300686347>'
    e=[':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:']
    await ctx.send( f'there is a coin hidden in these squares chose one \n {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')

@custom.command()
async def choose(ctx,arg11, arg22, arg44):  # arg1=coins arg2=no. on the grid arg4=id
    hiddenc=random.randint(1,9)
    a=int(arg22)
    e=[':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:']
    
    b=random.randint(1,9)
    tempvaluuu=e[b-1]
    e[b-1]=':coin:'
    if a>=1 and a<=9:
        if a==b:
            await ctx.send(f' {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')
            await ctx.send(f'{emoji} JACKPOT YOU FOUND THE COIN {emoji}' )
        
            outcome=9*int(arg11)
        else:
            
            await ctx.send(f' {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')
            e[b-1]=tempvaluuu
            await ctx.send(f'coin was in {e[b-1]}')
            outcome=-int(arg11)
        e[b-1]=tempvaluuu

    
        temp55 = int(coins[int(arg44)])
        temp66 = (temp55) + int(outcome)  # temp 5 is updated coin values
        if temp66 >= 1000:
            await ctx.send(t[int(arg44)] + ' wins the session')
        elif temp66 == 0:
            await ctx.send(t[int(arg44)] + ' is out')
        else:
            await ctx.send(t[int(arg44)] + ' your balance has been updated')

            coins[int(arg44)] = int(temp66)
            await ctx.send(temp44)

    else:
        await ctx.send('you really thought that would work?')


@custom.command()
async def b(ctx, arg):
    await ctx.send(coins[int(arg)])


@custom.command()
async def i(ctx):
    await ctx.send(t)

custom.run('tokenhere')
