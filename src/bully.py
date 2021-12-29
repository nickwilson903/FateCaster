from . import message_utils,  user_checker, messageparser
import traceback


no_no_file = open("./resources/no_no_words.txt", "r")
content = no_no_file.read()
no_no_list = content.split(",")

# Checks a given message to see if a user on the bully list said a no-no word.
def checkForNoNo(message):
    for entry in user_checker.fetchList():
        if str(message.author.id) in str(entry):
            for no_no in no_no_list:
                if no_no in str(message.content).lower():
                    response = ("<@" + str(message.author.id) + ">" + " shut the fuck up.")
                    return response
                else:
                    return None
        else:
            return None

# Adds someone to the bully list based on an @ extracted from the message
async def addBully(client, message):
      if "daddies" in [role.name.lower() for role in message.author.roles]:
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
            return response
          except:
            traceback.print_exc()
            response = message_utils.format_response("Invalid syntax, please type !bully add @user")
            return response
        else:
          response = message_utils.format_response("No users specified.")
          return response

# Fetches the list of people to bully
async def getBullyList(client):
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
        formatted_message += ("\n" + str(roster.index(entry)) + ": " + entry)
    response = message_utils.format_response(formatted_message)
    return response

# Removes someone from the bully list based on an index value retrieved from the message.
async def removeBully(client, message):
    if "daddies" in [role.name.lower() for role in message.author.roles]:
        print("Removing victim from list.")
        try:
            print("Extracting index from message")
            victim_index = messageparser.extractBullyName(message.content)
            victim_id = user_checker.getUserFromList(victim_index)
            member = await client.fetch_user(victim_id)
            victim_name = member.name
            user_checker.removeUserFromList(victim_index)
            response = message_utils.format_response("Removed entry: " + str(victim_name))
            return response
        except:
            traceback.print_exc()
            response = message_utils.format_response(
                "Invalid removal request. Type !bully list to get a list of users to keep track of, then !bully remove NUMBER to remove an entry from the list.")
            return response
    else:
        response = message_utils.format_response("No, cry about it.")
        return response

