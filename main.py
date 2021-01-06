import random
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('./ServiceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


custom = commands.Bot(command_prefix='!')

c = ['h', 't']
grid = ['1', '2', '3']


@custom.command()
async def h(ctx):
    await ctx.send('The Kasino welcomes you\n!p to register\n!b "your id" /shows you your balance\n!f "number of coins" "h/t" "id" /creates a coinflip\n!g "number of coins" "column" "row" "id"/grid guess\n!i  /shows player names and their ids\nRules:Everyone starts with a balance of 300 and first to 1000 coins wins\nif you get addicted to gambling and lose your shit visit https://www.begambleaware.org')


@custom.command()
async def p(ctx):
    doc_ref = db.collection('users').document(f'{ctx.author.id}')

    doc = doc_ref.get()
    if doc.exists:
        await ctx.send(f'You are already a registered gambler, {doc.to_dict()["username"]}.')
    else:
        init_money = 500 if random.randint(1, 20) == 1 else 300
        doc_ref.set({
            'username': f'{ctx.author.name}',
            'name': f'{ctx.author.display_name}',
            'money': init_money,
            'loan': 0
        })
        await ctx.send(f'You have officially registered as a gambler.\n{"Oh seems like you are lucky" if init_money == 500 else ""}')


@custom.command()
async def f(ctx, arg1, arg2):  # arg1=coins to be flipped
    temp3 = random.choice(c)
    docref=db.collection('users').document(f'{ctx.author.id}')
    doc=docref.get();
    moneyflip = int(doc.to_dict()['money'])
    if (moneyflip - int(arg1)) >= 0:

        if (temp3 == arg2):
            temp4 = 'you won the flip, coins are added to your balance'
            outcome = int(arg1)

        else:
            temp4 = 'scammed'
            outcome = -int(arg1)
        temp5 = moneyflip
        temp6 = (temp5) + int(outcome)  # temp 6 is updated coin values
        if temp6 >= 1000:
            await ctx.send(f'{ctx.author.display_name} wins the session')
        elif temp6 == 0:
            await ctx.send(f'{ctx.author.display_name} is out')
        else:
            await ctx.send(f'{ctx.author.display_name} your balance has been updated')

        docref.update({ 'money': temp6})
        await ctx.send(temp4)

    else:
        await ctx.send('you really thought that would work?')


@custom.command()
async def game(ctx):
    emoji = '<:python3:788673802300686347>'
    e = [':one:', ':two:', ':three:', ':four:', ':five:',
         ':six:', ':seven:', ':eight:', ':nine:']
    await ctx.send(f'there is a coin hidden in these squares chose one \n {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')


@custom.command()
async def choose(ctx, arg11, arg22, arg44):  # arg1=coins arg2=no. on the grid arg4=id
    hiddenc = random.randint(1, 9)
    a = int(arg22)
    e = [':one:', ':two:', ':three:', ':four:', ':five:',
         ':six:', ':seven:', ':eight:', ':nine:']

    emoji = '<:python3:788673802300686347>'
    b = hiddenc
    tempvaluuu = e[b-1]
    e[b-1] = ':coin:'
    if a >= 1 and a <= 9:
        if a == b:
            await ctx.send(f' {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')
            await ctx.send(f'{emoji} JACKPOT YOU FOUND THE COIN {emoji}')

            outcome = 9*int(arg11)
        else:

            await ctx.send(f' {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')
            e[b-1] = tempvaluuu
            await ctx.send(f'coin was in {e[b-1]}')
            outcome = -int(arg11)
        e[b-1] = tempvaluuu

        temp55 = int(coins[int(arg44)])
        temp66 = (temp55) + int(outcome)  # temp 5 is updated coin values
        if temp66 >= 1000:
            await ctx.send(t[int(arg44)] + ' wins the session')
        elif temp66 == 0:
            await ctx.send(t[int(arg44)] + ' is out')
        else:
            await ctx.send(t[int(arg44)] + ' your balance has been updated')

        coins[int(arg44)] = int(temp66)

    else:
        await ctx.send('you really thought that would work?')


@custom.command()
async def b(ctx, arg):
    await ctx.send(coins[int(arg)])



custom.run('token here')
