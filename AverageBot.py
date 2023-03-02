import discord
import logging

# Logging to make my life not hell, should probably change to log to a text document
logging.basicConfig(level=logging.INFO)
client = discord.Client()


stat_ids = []
stat_types = [[], [], [], [], [], []]


async def update_average(stat, stat_name, channel):
    stat_sum = sum(stat_types[stat])
    stat_average = stat_sum/len(stat_types[stat])
    messages = await channel.pins()
    for x in messages:
        if x.content.startswith(stat_name):
            await x.unpin()
    message = await channel.send(stat_name + ": " + str(stat_average))
    await message.pin()
    msg = await channel.history().get()
    await msg.delete()


# Informs when bot has logged in
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(command):
    global stat_types
    if command.content.startswith("$reset"):
        stat_types = [[], [], [], [], [], []]
        messages = await command.channel.pins()
        for x in messages:
            await x.unpin()
    if command.content.startswith("$save"):
        channel = command.channel
        callremoved = command.content.replace("$save ", "")
        command = callremoved.split(" ")
        stat_index = -1
        command[1] = int(command[1])
        if command[0] == "str":
            stat_types[0].append(command[1])
            stat_index = 0
        if command[0] == "dex":
            stat_types[1].append(command[1])
            stat_index = 1
        if command[0] == "con":
            stat_types[2].append(command[1])
            stat_index = 2
        if command[0] == "int":
            stat_types[3].append(command[1])
            stat_index = 3
        if command[0] == "wis":
            stat_types[4].append(command[1])
            stat_index = 4
        if command[0] == "cha":
            stat_types[5].append(command[1])
            stat_index = 5
        await update_average(stat_index, command[0], channel)
key = input("Enter Bot Key: ")
client.run(key)
