import discord
import os
import roller
import messageparser
from keep_alive import keep_alive
import user_checker
import traceback
import message_utils


client = discord.Client()
fc = roller.Roller()

no_no_file = open("no_no_words.txt","r")
content = no_no_file.read()
no_no_list = content.split(",")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Placeholder command for fudging functionality
    if message.content.startswith("!fudge"):
      debug_message = "This feature is currently being worked on, this is a placeholder command."
      response = message_utils.format_response(debug_message)
      await message.channel.send(response)
    
    #The help command, displays general info and usage for commands I want people to publicly know.
    if message.content.startswith("!help"):
      help_message = ("Hey! I'm {0.name}, and I'm the bastard child of alcohol consumption and boredom."\
      + "\n\nMy primary function is dice rolling, but I also do...other things. Here's a list of commands I'm willing to share with you publicly:\n"\
      + "\n---------------------------------------------------------------------"\
      + "\n!bully add/list/remove || These add and remove people from the list of users who I'm supposed to bully. /list displays it!"
      + "\n!hello || I'm not very talkative, but you're welcome to say hi!"\
      + "\n!r || My rolling command! You can do things like /r 1d20, /r 1d20 + 2, and even /r 1d20 + 3 #a description"\
      + "\n---------------------------------------------------------------------").format(client.user)
      response = message_utils.format_response(help_message)
      await message.channel.send(response)

    #An old test command I never removed. It's just rude.
    if message.content.startswith('!hello'):
        await message.channel.send('Go fuck yourself.')

    #kicks off roll commands
    #include additional global modifier in the future for the 'fudging part'
    if message.content.startswith("!r"):
      #/r  1d20  +  9
        print("Roll identified, processing.")
        try:
          roll_elements = messageparser.getRollContent(message.content)
          fc.command = roll_elements[0]
          fc.modifier = roll_elements[1]
          result = fc.rollTheFucker()
          if "-" not in roll_elements[1]:
              roll_elements[1] = ("+ " + str(roll_elements[1]))
          response = message_utils.format_response(roll_elements[2] + "\n" + roll_elements[0] + " " + roll_elements[1] + " = " + str(result))
          await message.channel.send(response)
          
        except:
          traceback.print_exc()
          response = message_utils.format_response("Invalid roll syntax, please type `!r XdY` with an optional `+` or `-` `Z` numerical modifier.")
          await message.channel.send(response)
  
    #Bully add, list, remove. Adds or removes an @ person to the list of people to monitor. List displays the people.
    if message.content.startswith("!bully add"):
        if (len(message.mentions) > 0):
          victim=message.mentions[0].id
          print("Adding someone to the bully list.")
          try:
            print("Extracting name from message" + str(victim))
            #victim = messageparser.extractBullyName(message.content)
            member = await client.fetch_user(victim)
            victim_name = member.name
            user_checker.addUserToList(victim)
            response = message_utils.format_response("Added " + victim_name + " to bully list.")
            await message.channel.send(response)
          except:
            traceback.print_exc()
            response = message_utils.format_response("Invalid syntax, please type !bully add @user")
            await message.channel.send(response)
        else:
          response = message_utils.format_response("No users specified.")
          await message.channel.send(response)


    if message.content.startswith("!bully list"):
      print("Returning list of victims.")
      roster = []
      roster_of_ids = user_checker.fetchList()
      for entry in roster_of_ids:
        member = await client.fetch_user(int(entry))
        name = member.name
        roster.append(name)
      print(roster)
      formatted_message = "List of victims: "
      for entry in roster:
        print(entry)
        formatted_message += ("\n"+str(roster.index(entry))+": "+entry)
      response = message_utils.format_response(formatted_message)
      await message.channel.send(response)

    
    if message.content.startswith("!bully remove"):
      print("Removing victim from list.")
      try:
        print("Extracting index from message")
        victim = messageparser.extractBullyName(message.content)
        user_checker.removeUserFromList(victim)
        response = message_utils.format_response("Removed entry: " + victim)
        await message.channel.send(response)
      except:
        traceback.print_exc() 
        response = message_utils.format_response("Invalid removal request. Type !bully list to get a list of users to keep track of, then !bully remove NUMBER to remove an entry from the list.")
        await message.channel.send(response)


    #Checks every message to see if someone needs to be bullied.
    for entry in user_checker.fetchList():
      if str(message.author.id) in str(entry):
        for no_no in no_no_list:
          if no_no in str(message.content).lower():
            response = ("<@"+str(message.author.id)+">" + " shut the fuck up.") 
            await message.channel.send(response)
        
    

#Keeps the bot alive via starting a server that gets external requests every 5 minutes.
keep_alive()
#Runs the bot
client.run(os.getenv('TOKEN'))