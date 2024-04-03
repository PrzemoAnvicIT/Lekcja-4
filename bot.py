# Podstawowy kod do uruchomienia bota na Discord, wykorzystuje klasę Bot

import discord
from discord.ext import commands
import random
from settings import settings
from bot_logic import *
import asyncio

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def haslo(ctx, dlugosc_hasla=8):
    losowe_haslo = gen_pass(dlugosc_hasla)
    await ctx.send(f'Twoje losowe hasło to:\n{losowe_haslo}')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def game(ctx):
    number = random.randint(0, 100)   # Dla celów testowych ustaw wartość; możesz chcieć użyć random.randint(0, 100) dla rzeczywistych gier.
    await ctx.send('Zgadnij numer od 0 do 100. Masz 5 prób!')

    def check(message):
        # Sprawdź, czy wiadomość pochodzi od użytkownika, który wywołał komendę i czy jest to liczba całkowita.
        return message.author == ctx.author and message.content.isdigit()

    for i in range(5):
        if i == 4:  # Dostosowane sprawdzanie dla wiadomości z ostatnią szansą.
            await ctx.send('Ostatnia szansa!')
        await ctx.send('Zgadnij numer...')
        
        try:
            response = await bot.wait_for('message', check=check, timeout=30.0)  # Dodaj limit czasu według potrzeb.
        except asyncio.TimeoutError:
            await ctx.send('Przekroczono limit czasu!')
            return

        guess = int(response.content)
        if guess > number:
            await ctx.send('mniej')
        elif guess < number:
            await ctx.send('więcej')
        else:
            await ctx.send(f'Tak! To {number}! Brawo!')
            return

    # Jeśli pętla zakończy się bez poprawnej odpowiedzi:
    await ctx.send(f'Niestety, nie udało się. Prawidłowy numer to: {number}.')



bot.run(settings['TOKEN'])
