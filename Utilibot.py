import discord
import logging
import re
import random
import collections

logging.basicConfig(level=logging.INFO)
client = discord.Client()

numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
dietest = re.compile("\A[\dd]")
additivematch = re.compile("([-+])")
damage_done = {}
current_initiative = {}


async def charactersheet(content, userid, channel):
    if content.startswith("-c"):
        content = content.replace("-c ", "")
        if content.startswith("stats"):
            content = content.replace("stats ", "")


async def initiative(content, guild, channel):
    toprint = []
    if content.startswith("-i"):
        content = content.replace("-i ", "")
        if content.startswith("init"):
            callremoved = content.replace("init ", "")
            current_initiative[guild] = []
            current_initiative[guild].append(0)
            excessmessage = callremoved.split(", ")
            current_initiative[guild].append(list(excessmessage))
            toprint = list(current_initiative[guild][1])
            toprint[current_initiative[guild][0]] = "-->" + toprint[current_initiative[guild][0]]
        if content.startswith("next"):
            current_initiative[guild][0] += 1
            if current_initiative[guild][0] >= len(current_initiative[guild][1]):
                current_initiative[guild][0] = 0
            toprint = list(current_initiative[guild][1])
            toprint[current_initiative[guild][0]] = "-->" + toprint[current_initiative[guild][0]]
        if content.startswith("del"):
            callremoved = content.replace("del ", "")
            if current_initiative[guild][1].index(callremoved) < current_initiative[guild][0]:
                current_initiative[guild][0] -= 1
            current_initiative[guild][1].remove(callremoved)
            if current_initiative[guild][0] >= len(current_initiative[guild][1]):
                current_initiative[guild][0] = 0
            if len(current_initiative[guild][1]) == 0:
                current_initiative[guild][1] = []
            else:
                toprint = list(current_initiative[guild][1])
                toprint[current_initiative[guild][0]] = "-->" + toprint[
                    current_initiative[guild][0]]
        if content.startswith("add"):
            callremoved = content.replace("add ", "")
            editsplit = callremoved.split(", ")
            if len(editsplit) == 1:
                editsplit.append(len(current_initiative[guild][1]) + 1)
            current_initiative[guild][1].insert(int(editsplit[1]) - 1, editsplit[0])
            if int(editsplit[1]) - 1 <= current_initiative[guild][0]:
                current_initiative[guild][0] += 1
            toprint = list(current_initiative[guild][1])
            toprint[current_initiative[guild][0]] = "-->" + toprint[current_initiative[guild][0]]
        if content.startswith("edit"):
            callremoved = content.replace("edit ", "")
            editsplit = callremoved.split(", ")
            indexvalue = current_initiative[guild][1].index(editsplit[0])
            current_initiative[guild][1][indexvalue] = editsplit[1]
            toprint = list(current_initiative[guild][1])
            toprint[current_initiative[guild][0]] = "-->" + toprint[current_initiative[guild][0]]
        await channel.send("```" + "Initiative:\n" + "\n".join(toprint) + "```")


async def roll(content, channel):
    total = 0
    addsub = 0
    batchedrolls = []
    batch = False
    if content.startswith("-r"):
        content = content.replace("-r ", "")
        if content.startswith("statroll"):
            stats = [[], [], [], [], [], []]
            minkept = [[], [], [], [], [], []]
            total = []
            for x in range(6):
                stats[x] = [random.randint(1, 6) for y in range(4)]
                stats[x].remove(min(stats[x]))
            for x in stats:
                total.append(sum(x))
        if content.startswith("-b"):
            content = content.replace("-b ", "")
            batch = True
        if re.match(dietest, content):
            num, maximum, = content.split("d")
            if num == "":
                num = 1
            if len(re.split(additivematch, maximum)) > 1:
                maximum, addsub, additive = re.split(additivematch, maximum)
                addsub = addsub + additive
            else:
                addsub = 0
            rolls = [random.randint(1, int(maximum)) for x in range(int(num))]
            if not batch:
                batchedrolls = rolls
            else:
                batchedrolls = dict(collections.Counter(rolls))
            total = sum(rolls)
        await channel.send("```" + "Result: " + str(total + int(addsub))
                           + " " + "Rolls: " + str(batchedrolls) + "```")


# Informs when bot has logged in
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(command):
    # Run any command related to Generating a random number
    await roll(command.content, command.channel)
    # Run any command related to creating and maintaining initiative
    await initiative(command.content, command.guild, command.channel)
    # Adds Damage Dealt to boss
    # Guaranteed to work

    if command.content.startswith("-hp"):
        callremoved = command.content.replace("-hp ", "")
        damage_done[command.guild.id] = damage_done.get(command.guild.id, 0) + int(callremoved)
        await command.channel.send("```Dealt: " + str(damage_done[command.guild.id]) + " Damage```")
    if command.content.startswith("-resethp"):
        damage_done[command.guild.id] = 0
        await command.channel.send("```Dealt: " + str(damage_done[command.guild.id]) + " Damage```")

    # Rolls xdx dice in form of emojis and returns result as emojis
    # Should work

    if command.content.startswith("\U0001fB30"):
        callremoved = command.content.replace("\U0001fB30", "")
        num, maximum = callremoved.split("🅱")
        num = [x for x in num]
        decodednum = []
        maximum = [x for x in maximum]
        for x in num:
            try:
                decodednum.append(int(x))
            except:
                pass
        decodedmax = []
        for x in maximum:
            try:
                decodedmax.append(int(x))
            except:
                pass
        maxdice = 0
        for x in decodednum:
            maxdice = int(str(maxdice) + str(x))
        maxsides = 0
        for x in decodedmax:
            maxsides = int(str(maxsides) + str(x))
        rolls = [random.randint(1, int(maxsides)) for x in range(int(maxdice))]
        total = str(sum(rolls))
        total = [int(x) for x in str(total)]
        output = []
        for x in total:
            output.append(numbers[int(x)])
        await command.channel.send("".join(output))


client.run()
