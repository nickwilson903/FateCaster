import dice

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

    def rollTheFucker(self):
      #takes in a list of dice elements (a command and a modifier), rolls them, and 
      #returns the result
      print("This is the command to run: " + self.command)
      print("This is the modifier: " + str(self.modifier))
      base_result = (dice.roll(self.command))
      result_with_modifier = int(base_result) + int(self.modifier)
      return result_with_modifier

    
