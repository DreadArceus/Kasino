import random
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
load_dotenv()
import discord

cred = credentials.Certificate('./ServiceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
bank = db.collection('users').document('bank')


def money_transfer(doc_ref, change):
    old = doc_ref.get().to_dict()['money']
    reserve = bank.get().to_dict()['money']
    doc_ref.update({'money': old + change})
    bank.update({'money': reserve - change})


class Blackjack:
    def __init__(self, card, chance, stand, author, wage):
        self.card = card
        self.chance = chance
        self.stand = stand
        self.author = author
        self.wage = wage


p1 = Blackjack(0, True, False, None, 0)
p2 = Blackjack(0, True, False, None, 0)

custom = commands.Bot(command_prefix='!')


@custom.command()
async def h(ctx):
    await ctx.send('The Kasino welcomes you\n!p to register\n!b shows you your balance\n!f "number of coins" "h/T" /creates a coinflip\n!game /shows the grid for pot \n !choose "number of coins" "no. on the grid"/grid guess\n!slot "bid amt" to try the slot machine\nRules:Everyone starts with a balance of 300\nif you get addicted to gambling and lose your shit visit https://www.begambleaware.org')


@custom.command()
async def bankc(ctx):
    await ctx.send(f'Bank has: {bank.get().to_dict()["money"]}')


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

        money_transfer(docref,outcome)
        await ctx.send(temp4)

    else:
        await ctx.send('you really thought that would work?')

@custom.command()
async def loanplayer(ctx, amt,playername : discord.User):
    amt=int(amt)
    print(playername.display_name)
    print(playername.id)
    doc_ref = db.collection('users').document(f'{playername.id}')
    doc_ref2 = db.collection('users').document(f'{ctx.author.id}')
    
    doc = doc_ref.get()
    doc2 = doc_ref2.get()
    bal1 = int(doc.to_dict()['money'])
    bal2 = int(doc2.to_dict()['money'])
    if doc.exists and amt<=bal2:
        doc_ref.update({ 'money' : bal1+amt  })
        doc_ref2.update({'money' : bal2-amt })
        await ctx.send(f'updating blanace of {playername.display_name} and {ctx.author.display_name}')
    elif doc.exists :
        await ctx.send(f'insufficient balance')
    else :
        await ctx.send(f'user doesnt exist')
        
        


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

            money_transfer(docref,outcome)

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
async def d(ctx):
    s=[random.randint(-1000,1000),random.randint(-1000,1000),random.randint(-1000,1000),random.randint(-1000,1000),random.randint(-1000,1000),random.randint(-1000,1000)]
    i = random.randint(0,5)
    m=s[i]
    docref=db.collection('users').document(f'{ctx.author.id}')
    doc=docref.get()
    balance=int(doc.to_dict()['money'])
    await ctx.send('The dice rools:-')
    await ctx.send(file=discord.File('tenor.gif'))
    await ctx.send(i+1)
    if (m>=0 and m<=100):
        await ctx.send('Heres your little penny <:peepoHappy:791557963679793164>')
        await ctx.send(m)
        balance=balance+m
    elif (m>100 and m<500):
        await ctx.send('WOO looks like u r lucky day <:EZ:>')
        await ctx.send(m)
        balance=balance+m
    elif m>500:
        await ctx.send('Damnn boi RICHH :POGGIES:')
        await ctx.send(m)
        balance=balance+m
    elif (m<0 and m>-100):
        await ctx.send('Hehe U got robbed :KEKW:')
        await ctx.send(m)
        balance=balance+m
    elif (m<-100 and m>-500):
        await ctx.send('Fuk off bitch u dead fam :PepeLaugh:')
        await ctx.send(m)
        balance=balance+m
    elif m<-500:
        await ctx.send('Someone call Logan, Dead body reported :DORIME:791557963282120765')
        await ctx.send(m)
        balance=balance+m
    docref.update({ 'money': balance })    

                       
@custom.command()
async def slot(ctx, bid):
    bet = int(bid)
    outcome=0
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
                await ctx.send("congrats,you get 2 times ur bet amount")  #if win outcome positive
                outcome= (bet * 2)

            elif(l[0] == "<:peepoHappy:791557963679793164>"):
                await ctx.send("congrats,you get 5 times ur bet amount")
                outcome= (bet * 5)

            elif(l[0] == "<:FeelsGeniusMan:788674683687010305>"):
                outcome= (bet * 15)
                await ctx.send("congrats,you get 15 times ur bet amount")

            elif(l[0] == "<:POGGIES:791557965005324340>"):
                outcome= (bet * 50)
                await ctx.send("congrats,you get 50 times ur bet amount")

            else:
                outcome= (bet * 100)
                await ctx.send("FIND A REAL LOTTERY,you get 100 TIMES ur bet amount")

        elif(l[0] == l[1] or l[1] == l[2] or l[0] == l[2]):
            await ctx.send("U get to keep ur money")         #if draw outcome 0
            outcome =0
        else:
            outcome=-bet                    # if lose outcome negative
            await ctx.send("Hehehe,Better Luck Next Time!")

        await ctx.send(f'{ctx.author.display_name} your balance has been updated')
        money_transfer(docref,outcome)   

    else:
        await ctx.send("u poor being,ask boss for more coins ")


@custom.command()
async def blackjack(ctx):
    await ctx.send("Welcome to BlackJack")
    if(p1.author == None):
        p1.author = ctx.author
        await ctx.send("You are Player One")
    elif(p2.author == None):
        if(ctx.author == p1.author):
            await ctx.send("Wait for second player")
        else:
            p2.author = ctx.author
            await ctx.send("You are Player Two")
            await ctx.send("If you wanna wager this game type !wager amount")
    else:
        await ctx.send("A Game is goin on wait for it to get over")


@custom.command()
async def wager(ctx, amt):
    amt = int(amt)
    docrefp1 = db.collection('users').document(f'{p1.author.id}')
    docp1 = docrefp1.get()
    balp1 = int(docp1.to_dict()['money'])
    docrefp2 = db.collection('users').document(f'{p2.author.id}')
    docp2 = docrefp2.get()
    balp2 = int(docp2.to_dict()['money'])
    if(balp1 >= amt and balp2 >= amt):
        p1.wage = amt
        p2.wage = amt
        balp1 -= amt
        balp2 -= amt
        docrefp1.update({'money': balp1})
        docrefp2.update({'money': balp2})
        await ctx.send("Both have enough money to wager and amount has been deducted")
    else:
        if(balp1 < amt):
            await ctx.send(f"{p1.author.name}, you're broke man :(")
        else:
            await ctx.send(f"{p2.author.name}, you're broke man :(")


@custom.command()
async def hit(ctx):
    if(ctx.author == p1.author):
        await ctx.send(f"{p1.author.name} decided to hit")
        rand_count = random.randint(1, 10)
        if (p1.chance == True and p1.stand == False):
            p1.card += rand_count
            await ctx.send(f"You have picked {rand_count}")
            if(p2.stand == False):
                p1.chance = False
            if(p1.card > 21):
                await ctx.send(f"You have exceeded 21 and have lost \n TAke ThE L ")
                if(p1.wage != 0):
                    await ctx.send(f"{ctx.author.name} loses his wager of {p1.wage}")
                docrefp1 = db.collection('users').document(f'{p1.author.id}')
                docp1 = docrefp1.get()
                balp1 = int(docp1.to_dict()['money'])
                docrefp2 = db.collection('users').document(f'{p2.author.id}')
                docp2 = docrefp2.get()
                balp2 = int(docp2.to_dict()['money'])
                balp2 += 2*p2.wage
                docrefp1.update({'money': balp1})
                docrefp2.update({'money': balp2})
                if(p1.wage != 0):
                    await ctx.send(f"Wager amount has been added to {p2.author.name}'s account ")
                p1.card = 0
                p1.stand = False
                p1.chance = True
                p1.author = None
                p1.card = 0
                p1.wage = 0
                p1.stand = False
                p1.chance = True
                p2.author = None
                p2.wage = 0
            else:
                p2.chance = True
                await ctx.send(f"{p1.card} is the current score")
        else:
            if(p1.stand == True):
                await ctx.send("You can no longer hit as you decided to stand")
            else:
                await ctx.send("Its not your turn")
    elif(ctx.author == p2.author):
        await ctx.send(f"{p2.author.name} decided to hit")
        rand_count = random.randint(1, 10)
        if (p2.chance == True and p2.stand == False):
            p2.card += rand_count
            await ctx.send(f"You have picked {rand_count}")
            if(p1.stand == False):
                p2.chance = False
            if(p2.card > 21):
                await ctx.send(f"You have exceeded 21 and have lost \n TAke ThE L ")
                if(p1.wage != 0):
                    await ctx.send(f"{ctx.author.name} loses his wager of {p1.wage}")
                docrefp1 = db.collection('users').document(f'{p1.author.id}')
                docp1 = docrefp1.get()
                balp1 = int(docp1.to_dict()['money'])
                docrefp2 = db.collection('users').document(f'{p2.author.id}')
                docp2 = docrefp2.get()
                balp2 = int(docp2.to_dict()['money'])
                balp1 += 2*p2.wage
                docrefp1.update({'money': balp1})
                docrefp2.update({'money': balp2})
                if(p1.wage != 0):
                    await ctx.send(f"Wager amount has been added to {p1.author.name}'s account ")
                p1.card = 0
                p1.stand = False
                p1.chance = True
                p1.author = None
                p1.wage = 0
                p2.card = 0
                p2.stand = False
                p2.chance = True
                p2.author = None
                p2.wage = 0
            else:
                p1.chance = True
                await ctx.send(f"{p2.card} is the current score")
        else:
            if(p1.stand == True):
                await ctx.send("You can no longer hit as you decided to stand")
            else:
                await ctx.send("Its not your turn")


@custom.command()
async def stand(ctx):

    if(ctx.author == p1.author):
        await ctx.send("You have decided to stand")
        p1.stand = True
        p2.chance = True
        if(p2.stand == True):
            await ctx.send("Both have decided to stand")
        else:
            await ctx.send("You can no longer hit.")
    elif(ctx.author == p2.author):
        await ctx.send("You have decided to stand")
        p2.stand = True
        p1.chance = True
        if(p1.stand == True):
            await ctx.send("Both have decided to stand")
        else:
            await ctx.send("You can no longer hit.")
    if(p1.stand == True and p2.stand == True):
        docrefp1 = db.collection('users').document(f'{p1.author.id}')
        docp1 = docrefp1.get()
        balp1 = int(docp1.to_dict()['money'])
        docrefp2 = db.collection('users').document(f'{p2.author.id}')
        docp2 = docrefp2.get()
        balp2 = int(docp2.to_dict()['money'])
        if(p1.card > p2.card):
            await ctx.send(f"{p2.author.name} lost  to {p1.author.name}")
            balp1 += 2*p2.wage
            docrefp1.update({'money': balp1})
            docrefp2.update({'money': balp2})
            if(p1.wage != 0):
                await ctx.send(f"Wager amount has been added to {p1.author.name}'s account ")
        elif(p2.card > p1.card):
            await ctx.send(f"{p1.author.name} lost  to {p2.author.name}")
            balp2 += 2*p2.wage
            docrefp1.update({'money': balp1})
            docrefp2.update({'money': balp2})
            if(p1.wage != 0):
                await ctx.send(f"Wager amount has been added to {p2.author.name}'s account ")
        else:
            await ctx.send("Match ends in a draw")
            balp1 += p1.wage
            balp2 += p2.wage
            docrefp1.update({'money': balp1})
            docrefp2.update({'money': balp2})
            if(p1.wage != 0):
                await ctx.send("Wager amount has been returned")
        p1.card = 0
        p1.stand = False
        p1.chance = True
        p1.author = None
        p1.wage = 0
        p2.card = 0
        p2.stand = False
        p2.chance = True
        p2.author = None
        p2.wage = 0


custom.run(os.getenv("TOKEN"))
