#Strips the '/r' from the message, leaving just the body
def getRollContent(message):
    print("This is the message I'm evaluating: " + message)
    extracted_message=message.split('!r',1)
    validroll = extractValidRoll(extracted_message[1])
    #Should return strings like 1d20 or 1d20+2
    #Technically returns everything just without the /r, but we'll deal with that later
    return validroll

def extractValidRoll(extracted_message):

    print("This is what I extracted: " + extracted_message)

    #GOAL: get number of dice, get sides of dice, and an optional + or - & number
    modifier = 0
    #Extracts the items needed to perform a roll: a dice expression (XdY) and an #optional modifier
    validroll = extracted_message
    mod1 = "+"
    mod2 = "-"
    mod3 = "#"
    descriptor=''

    if mod3 in extracted_message:
      #should return the message attached to a roll, if present.
      descriptor = ("#" + validroll.split(mod3)[1])
      validroll = validroll.split(mod3)[0]

    validroll = validroll.replace(" ","")  

    if mod1 in extracted_message:
        #should return an extracted number, to be made positive
        modifier = int(validroll.split(mod1)[1])
        #should only keep the XdY expression
        validroll = validroll.split(mod1)[0]
        
    if mod2 in extracted_message:
        modifier = (int(validroll.split(mod2)[1]) * -1)
        validroll = validroll.split(mod2)[0]

    print("This is what I got for a valid roll: " + validroll + " and this is the modifier: " + str(modifier))

    roll_elements = [validroll, str(modifier), descriptor]

    return roll_elements

def extractBullyName(message):
    print("Trying to extract from: " + message)
    bully_command = message.split('!bully')[1]
    bully_command =bully_command.replace(" ","")
    comm1 = "add"
    comm2 = "remove"
    print(bully_command)
    if comm1 in bully_command:
      print("Bully Add Command")
      bully_name = bully_command.split(comm1)[1]
    elif comm2 in bully_command:
      bully_name = bully_command.split(comm2)[1]
    else:
      raise Exception
    
    print("Returning " +  bully_name)
    return bully_name


    


