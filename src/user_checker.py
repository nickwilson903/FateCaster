from replit import db
import discord


def isUserInList(user_id):
  if "bully" not in db.keys():
    db["bully"] = ''
  bully_list = list(db["bully"])
  user_id_exists = any(user_id in entry for entries in bully_list)
  return user_id_exists

def addUserToList(user_id):
    if "bully" in db.keys():
      if str(user_id) in db["bully"]:
        return
      else:  
        bully_list = list(db["bully"])
        bully_list.append(user_id)
        db["bully"] = bully_list
    else:
      db["bully"] = [user_id]

def getUserFromList(index):
  bully_list = list(db["bully"])
  return bully_list[int(index)] 

def removeUserFromList(index):
    bully_list =list(db["bully"])
    bully_list.pop(int(index))
    db["bully"] = bully_list

def fetchList():
  if "bully" not in db.keys():
    db["bully"] = ''
  bully_list = list(db["bully"])
  return bully_list