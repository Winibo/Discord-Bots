import discord
import logging


# Logging to make my life not hell, should probably change to log to a text document
logging.basicConfig(level=logging.INFO)
client = discord.Client()


# Informs when bot has logged in
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


hp = 0


@client.event
async def on_message(command):
    global hp
    if command.content.startswith("$hp "):
        callremoved = command.content.replace("$hp ", "")
        hp = hp + int(callremoved)
        await command.channel.send("Dealt " + str(hp) + " Damage")
    if command.content.startswith("$reset"):
        hp = 0


key = input("Enter Bot Key: ")
client.run(key)
