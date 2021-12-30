import discord
import os
from src import message_utils, roller, bully
from src.keep_alive import keep_alive

client = discord.Client()
fc = roller.Roller()

#TODO make actual commands instead of parsing every message for a given pattern.
#TODO create a json configuration that holds server command prefixes, bullied users, no no words, roles needed for changing bullied list, and fudged value.
#TODO refactor uses of the traceback library to use logging instead. Use logger with discord client integration.


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Placeholder command for fudging functionality
    if message.content.startswith("!fudge"):
        debug_message = "This feature is currently being worked on, this is a placeholder command."
        response = message_utils.format_response(debug_message)
        await message.channel.send(response)

    # The help command, displays general info and usage for commands I want people to publicly know.
    if message.content.startswith("!help"):
        help_message = ("Hey! I'm {0.name}, and I'm the bastard child of alcohol consumption and boredom." \
                        + "\n\nMy primary function is dice rolling, but I also do...other things. Here's a list of commands I'm willing to share with you publicly:\n" \
                        + "\n---------------------------------------------------------------------" \
                        + "\n!bully add/remove || These add and remove people from the list of users who I'm supposed to bully. To remove someone, specify their location in the bully list. !bully list can show you."
                        + "\n!hello || I'm not very talkative, but you're welcome to say hi!" \
                        + "\n!r || My rolling command! You can do things like !r 1d20, !r 1d20 + 2, and even !r 1d20 + 3 #now with a description" \
                        + "\n---------------------------------------------------------------------").format(client.user)
        response = message_utils.format_response(help_message)
        await message.channel.send(response)

    # An old test command I never removed. It's just rude.
    if message.content.startswith('!hello'):
        await message.channel.send('Go fuck yourself.')

    # kicks off roll commands
    # include additional global modifier in the future for the 'fudging part'
    if message.content.startswith("!r"):
        # /r  1d20  +  9
        print("Roll identified, processing.")
        await message.channel.send(fc.identifyRoll(message))

    # Bully add, list, remove.
    #TODO make a generic bully command, add functionality for displaying, adding, and removing no-no words.
    if message.content.startswith("!bully add"):
        await message.channel.send(await bully.addBully(client,message))

    if message.content.startswith("!bully list"):
        await message.channel.send(await bully.getBullyList(client))

    if message.content.startswith("!bully remove"):
        await message.channel.send(await bully.removeBully(client, message))

    # Checks every message to see if someone needs to be bullied.
    has_no_no = bully.checkForNoNo(message)
    if has_no_no is not None:
      await message.channel.send(has_no_no)


# Keeps the bot alive via starting a server that gets external requests every 5 minutes.
# Only used for hosting on replit because I don't wanna pay for this every month.
keep_alive()
# Runs the bot

client.run(os.getenv('TOKEN'))
