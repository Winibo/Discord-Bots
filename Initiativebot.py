import discord
import logging

# Logging to make my life not hell, should probably change to log to a text document
logging.basicConfig(level=logging.INFO)
client = discord.Client()

# These globals should ONLY be affected by initiative based commands
currentPlayer = 0
currentInitiative = []


# Function to write initiative to discord channel
async def write_initiative(channel, initiativeorder):
    initiativeorder[currentPlayer] = "-->" + initiativeorder[currentPlayer]
    await channel.send("```" + "Initiative:\n" + "\n".join(initiativeorder) + "```")


# Informs when bot has logged in
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


# Actual functions for the bot
@client.event
async def on_message(initiative):
    commandrun = False
    global currentPlayer, currentInitiative
    channel = initiative.channel
    # Ensures that the bot can't call itself(Shouldn't ever be triggered, but I'm an idiot...)
    if initiative.author == client.user:
        return
    # Commands that change things about initiative.
    # Sets up new initiative
    if initiative.content.startswith("$init"):
        currentPlayer = 0
        callremoved = initiative.content.replace("$init ", "")
        excessmessage = callremoved.split(", ")
        currentInitiative = list(excessmessage)
        commandrun = True
    # Moves to next player in initiative
    if initiative.content.startswith("$next"):
        currentPlayer += 1
        commandrun = True
    # Edits a player in the current initiative
    if initiative.content.startswith("$edit"):
        callremoved = initiative.content.replace("$edit ", "")
        editsplit = callremoved.split(", ")
        indexvalue = currentInitiative.index(editsplit[0])
        currentInitiative[indexvalue] = editsplit[1]
        commandrun = True
    # Deletes a player from the initiative, moving to next player if necessary
    if initiative.content.startswith("$del"):
        callremoved = initiative.content.replace("$del ", "")
        if currentInitiative.index(callremoved) < currentPlayer:
            currentPlayer -= 1
        currentInitiative.remove(callremoved)
        if len(currentInitiative) == 0:
            await channel.send("No more players in Initiative.")
            return
        commandrun = True
    # Inserts new player into initiative, keeping current turn order
    if initiative.content.startswith("$add"):
        callremoved = initiative.content.replace("$add ", "")
        editsplit = callremoved.split(", ")
        # Appends the current initiative if argument is not passed
        # This defaults a player to end of initiative if a position is not specified
        if len(editsplit) == 1:
            editsplit.append(len(currentInitiative)+1)
        currentInitiative.insert(int(editsplit[1])-1, editsplit[0])
        if int(editsplit[1])-1 <= currentPlayer:
            currentPlayer += 1
        commandrun = True
    # Checks if Initiative is greater than number of players, and resets to start of initiative if true.
    if currentPlayer >= len(currentInitiative):
        currentPlayer = 0
    # Calls function to write Current Initiative to channel ONLY if a command is written
    if commandrun:
        excessmessage = list(currentInitiative)
        await write_initiative(channel, excessmessage)

# Runs bot
key = input("Input Bot Key:")
client.run(key)
