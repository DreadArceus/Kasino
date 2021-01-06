import random
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate('./ServiceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


custom = commands.Bot(command_prefix='!')


@custom.command()
async def h(ctx):
    await ctx.send('The Kasino welcomes you\n!p to register\n!b shows you your balance\n!f "number of coins" "h/T" /creates a coinflip\n!game /shows the grid for pot \n !choose "number of coins" "no. on the grid"/grid guess\n!slot "bid amt" to try the slot machine\nRules:Everyone starts with a balance of 300\nif you get addicted to gambling and lose your shit visit https://www.begambleaware.org')


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
    c = ['h', 't']
    temp3 = random.choice(c)
    docref = db.collection('users').document(f'{ctx.author.id}')
    doc = docref.get()
    moneyflip = int(doc.to_dict()['money'])
    if (moneyflip - int(arg1)) >= 0 and int(arg1) > 0:

        if (temp3 == arg2):
            temp4 = 'you won the flip, coins are added to your balance'
            outcome = int(arg1)

        else:
            temp4 = 'scammed'
            outcome = -int(arg1)
        temp5 = moneyflip
        temp6 = (temp5) + int(outcome)  # temp 6 is updated coin values
        if temp6 == 0:
            await ctx.send(f'{ctx.author.display_name} is out')
        else:
            await ctx.send(f'{ctx.author.display_name} your balance has been updated')

        docref.update({'money': temp6})
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
async def choose(ctx, arg11, arg22):  # arg1=coins arg2=no. on the grid arg4=id
    hiddenc = random.randint(1, 9)
    a = int(arg22)
    e = [':one:', ':two:', ':three:', ':four:', ':five:',
         ':six:', ':seven:', ':eight:', ':nine:']
    t = int(arg11)
    emoji = '<:python3:788673802300686347>'
    b = hiddenc
    tempvaluuu = e[b-1]
    docref = db.collection('users').document(f'{ctx.author.id}')
    doc = docref.get()
    temp55 = int(doc.to_dict()['money'])
    e[b-1] = ':coin:'

    if t <= temp55:
        if a >= 1 and a <= 9:
            if a == b:
                await ctx.send(f' {e[0]}{e[1]}{e[2]} \n{e[3]}{e[4]}{e[5]} \n{e[6]}{e[7]}{e[8]}')
                await ctx.send(f'{emoji} JACKPOT YOU FOUND THE COIN {emoji}')

                outcome = 9*int(arg11)
            else:

                await ctx.send(f' {e[0]}{e[1]}{e[2]} \n {e[3]}{e[4]}{e[5]} \n {e[6]}{e[7]}{e[8]}')
                e[b-1] = tempvaluuu
                await ctx.send(f'coin was in {e[b-1]}')
                outcome = -int(arg11)
            e[b-1] = tempvaluuu
            docref = db.collection('users').document(f'{ctx.author.id}')
            doc = docref.get()

            temp66 = (temp55) + int(outcome)  # temp 5 is updated coin values
            if temp66 == 0:
                await ctx.send(f'{ctx.author.display_name} is out')
            else:
                await ctx.send(f'{ctx.author.display_name} your balance has been updated')

            docref.update({'money': temp66})

        else:
            await ctx.send('you really thought that would work?')
    else:
        await ctx.send('you broke lmao')


@custom.command()
async def b(ctx):
    docref = db.collection('users').document(f'{ctx.author.id}')
    doc = docref.get()
    c = int(doc.to_dict()['money'])
    await ctx.send(c)


@custom.command()
async def slot(ctx, bid):
    bet = int(bid)
    list = ["<:DORIME:791557963282120765>", "<:peepoHappy:791557963679793164>",
            "<:FeelsGeniusMan:788674683687010305>", "<:POGGIES:791557965005324340>", "<:EZ:791557965441138720>"]
    l = []
    docref = db.collection('users').document(f'{ctx.author.id}')
    doc = docref.get()
    balance = int(doc.to_dict()['money'])

    if(balance >= bet and bet > 0):
        balance = balance-bet
        for i in range(3):
            a = random.randint(1, 100)
            if(a >= 1 and a <= 30):
                l.append(list[0])
            elif(a > 30 and a <= 55):
                l.append(list[1])
            elif(a > 55 and a <= 75):
                l.append(list[2])
            elif(a > 75 and a <= 90):
                l.append(list[3])
            elif(a > 90 and a <= 100):
                l.append(list[4])

        s = l[0]+l[1]+l[2]
        await ctx.send("u rolled--")
        await ctx.send(s)

        if(l[0] == l[1] and l[1] == l[2] and l[0] == l[2]):
            if(l[0] == "<:DORIME:791557963282120765>"):
                await ctx.send("congrats,you get 2 times ur bet amount")
                balance += (bet * 2)

            elif(l[0] == "<:peepoHappy:791557963679793164>"):
                await ctx.send("congrats,you get 5 times ur bet amount")
                balance += (bet * 5)

            elif(l[0] == "<:FeelsGeniusMan:788674683687010305>"):
                balance += (bet * 15)
                await ctx.send("congrats,you get 15 times ur bet amount")

            elif(l[0] == "<:POGGIES:791557965005324340>"):
                balance += (bet * 50)
                await ctx.send("congrats,you get 50 times ur bet amount")

            else:
                balance += (bet * 100)
                await ctx.send("FIND A REAL LOTTERY,you get 100 TIMES ur bet amount")

        elif(l[0] == l[1] or l[1] == l[2] or l[0] == l[2]):
            await ctx.send("U get to keep ur money")
            balance = balance+bet
        else:
            await ctx.send("Hehehe,Better Luck Next Time!")

        await ctx.send(f'{ctx.author.display_name} your balance has been updated')
        docref.update({'money': balance})

    else:
        await ctx.send("u poor being,ask boss for more coins ")


custom.run(os.getenv(TOKEN))
