import dice
import messageparser
import message_utils
import traceback

#TODO: Add additional attributes for fudgeModifier and fudgeCount

class Roller:
    def __init__(self):
        self.command = '1d20'
        self.modifier = 0

    @property
    def getCommand(self):
        return self.command
    
    @property
    def getModifier(self):
        return self.modifier    
    
    @getCommand.setter
    def setCommand(self, com):
        self.command = com
    
    @getModifier.setter
    def seModifier(self, mod):
        self.modifier = mod

    def identifyRoll(self, message):
        try:
            roll_elements = messageparser.getRollContent(message.content)
            self.command = roll_elements[0]
            self.modifier = roll_elements[1]
            result = self.rollTheFucker()
            if "-" not in roll_elements[1]:
                roll_elements[1] = ("+ " + str(roll_elements[1]))
            response = message_utils.format_response(
                roll_elements[2] + "\n" + roll_elements[0] + " " + roll_elements[1] + " = " + str(result))
            return response

        except:
            traceback.print_exc()
            response = message_utils.format_response("Invalid roll syntax, please type `!r XdY` with an optional `+` or `-` `Z` numerical modifier.")
            return response

    def rollTheFucker(self):
      #takes in a list of dice elements (a command and a modifier), rolls them, and 
      #returns the result
      print("This is the command to run: " + self.command)
      print("This is the modifier: " + str(self.modifier))
      base_result = (dice.roll(self.command))
      result_with_modifier = int(base_result) + int(self.modifier)
      return result_with_modifier

    
