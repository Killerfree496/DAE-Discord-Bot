import discord
import random
import aiohttp
from discord.ext import commands
import asyncio
import os

client = commands.Bot(command_prefix="+")
@client.event
#Einloggen
async def on_ready():
    print('Wir sind eingeloggt als User {}'.format(client.user.name))
    print("--------------------------------")
    print("Der Bot wurde gestartet.")
    print("Version 0.4")
    print("Made by Killerfree99#5403")
    print("--------------------------------")
    client.loop.create_task(status_task())

@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('+hilfe'), status=discord.Status.online)
        await asyncio.sleep(3)
        await client.change_presence(activity=discord.Game(':D'), status=discord.Status.online)
        await asyncio.sleep(3)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')


@client.command()
async def serverstats(ctx):
    embed=discord.Embed(title=f"Serverstats {ctx.guild.name}")
    embed.add_field(name="Users:", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Channels:", value=len(ctx.guild.channels), inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def meme(ctx):
    embedVar = discord.Embed(title="Hier ein Random Meme frisch aus dem World Wide Web", description= f"Angfordert von {ctx.author.name}")
    async with aiohttp.ClientSession() as cs:
     async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
        res = await r.json()
        embedVar.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        await ctx.message.delete()
        await ctx.send(embed=embedVar)



@client.command()
async def voting(ctx, *, suggestion):

    embedVar = discord.Embed (
        title = f"Abstimmung von {ctx.author.name}",
        description = f"Der User <@{ctx.author.id}> hat eine Abstimmung gemacht, stimmt für ihn ab.\n\n**Abstimmung**:\n{suggestion}",
        color = 0xeba834
    )

    embedVar.set_thumbnail(url=f"{ctx.author.avatar_url}")

    await ctx.message.delete()
    suggestion_message = await ctx.send(embed=embedVar)
    await suggestion_message.add_reaction('👍')
    await suggestion_message.add_reaction('👎')


@client.command()
async def say(ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)
        return


@client.command(aliases=['j'])
async def joined(ctx, *, member: discord.Member):
	await ctx.send('{0} joined on {0.joined_at}'.format(member))

@client.command(pass_context=True)
async def nudes(ctx):
    embedVar = discord.Embed(title="Hier ein Random Nacktbild", description= f"Gönn dir! Sry falls die Bilder sich wiederholen!")
    async with aiohttp.ClientSession() as cs:
     async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
        res = await r.json()
        embedVar.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        await ctx.message.delete()
        if ctx.channel.is_nsfw():
         await ctx.send(embed=embedVar)

@client.command(pass_context=True)
async def hilfe(ctx):
	await ctx.message.delete()
	embedVar = discord.Embed(title="**Hilfe zum DaE Bot**", description="Hier sind die Befehle für den Bot", color=0x00ff00)
	embedVar.add_field(name="Sprich mir nach", value="+say [Denk dir was aus]", inline=False)
	embedVar.add_field(name="Bot pingen", value="+ping", inline=False)
	embedVar.add_field(name="Ein Meme bekommen", value="+meme", inline=False)
	embedVar.add_field(name="Voting", value="+voting [Abstimmung]", inline=False)
	embedVar.add_field(name="Random Zahl generieren", value="+RandomZahl", inline=False)
	embedVar.add_field(name="Serverstats", value="+serverstats", inline=False)
	embedVar.add_field(name="Beitritts Datum abfragen", value="+joined [Dein Nickname]", inline=False)
	await ctx.send(embed=embedVar)


client.run('')
