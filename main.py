import os
import discord
import requests
import json
import random
from replit import db
from keepalive import keep_alive

# function to update encouragements
def update_encourage(args):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(args)
        db['encouragements'] = encouragements
    else:
        global encourage_starter
        encourage_starter.append(args)
        db['encouragements'] = encourage_starter

# to delete encouragements
def delete_encourage(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

# function to update sad words
def update_sadwords(args):
    if 'sadwords' in db.keys():
        sadwords = db['sadwords']
        sadwords.append(args)
        db['sadwords'] = sadwords
    else:
        global starter_sadwords
        starter_sadwords.append(args)
        db['sadwords'] = starter_sadwords

# to delete sadwords
def delete_sadword(index):
  sadwords = db['sadwords']
  if len(sadwords) > index:
    del sadwords[index]
    db['sadwords'] = sadwords

client = discord.Client()

sad_words = ["sad", "depressing","depressed","angry","unhappy","miserable"]

starter_encouragments = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot !"
  ]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

@client.event
async def on_ready():
  print('We are logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db["responding"]:
    options = starter_encouragments
    if "encouragements" in db.keys():
      options += db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$newEnco"):
    encouraging_message = msg.split("$newEnco ",1)[1]
    update_encourage(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$delEnco"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$delEnco",1)[1])
      delete_encourage(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

# to list encouragements 
  if msg.startswith('$listEnco'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
      if len(encouragements) == 0:
        await message.channel.send('The list is empty please add new encouragements by command "$newEnco"')
      else:
        list1 = '\n'.join(encouragements)
    await message.channel.send(list1)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on!")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off!")

# if msg starts with '!newSad' means user want to add new sad word
  if msg.startswith('$newSad'):
    new = msg.split('$newSad ', 1)[1]
    update_sadwords(new)
    await message.channel.send(f'new sad "{new}"word added')

  if msg.startswith('$listSad'):
    sadwords = []
    if 'sadwords' in db.keys():
      sadwords = db['sadwords']
      if len(sadwords) == 0:
        await message.channel.send('the list is empty')
      else:
        lost = '\n'.join(sadwords)
        await message.channel.send(lost)

  if msg.startswith('$deleteSad'):
    sadwords = []
    if 'sadwords' in db.keys():
      sadwords = db['sadwords']
      index = int(msg.split('$deleteSad ',1)[1])
      index = index - 1
      delete_sadword(index)
      await message.channel.send('sadowrd is deleted')  

my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)