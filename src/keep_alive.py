from flask import Flask
from threading import Thread


#Exists solely so I don't have to pay for this thing. Is hit every 5 minutes from
#an external app to keep this one alive.
app= Flask('')

@app.route('/')

def home():
    return "Still alive."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t=Thread(target=run)
    t.start()