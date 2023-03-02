import discord
import logging
import re
import random

# Regex to find if maximum contains an additive/negative
additivematch = re.compile("([-+])")
# Logging to make my life not hell, should probably change to log to a text document
logging.basicConfig(level=logging.INFO)
client = discord.Client()


# Informs when bot has logged in
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(roll):
    if roll.content.startswith("-roll"):
        callremoved = roll.content.replace("-roll ", "")
        num, maximum = callremoved.split("d")
        if len(re.split(additivematch, maximum)) > 1:
            maximum, addsub, additive = re.split(additivematch, maximum)
            addsub = addsub + additive
        else:
            addsub = 0
        if num == "":
            num = 1
        rolls = [random.randint(1, int(maximum)) for x in range(int(num))]
        await roll.channel.send("```" + "Total: " + str(sum(rolls)+int(addsub)) + " " + "Rolls: " + str(rolls) + "```")


# Runs bot
key = input("Input Bot Key:")
client.run(key)
