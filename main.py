import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()
categories = ['Misc','Programming','Dark','Pun','Spooky','Christmas']


def create_random_jokes():
  joke = ""
  response = requests.get("https://v2.jokeapi.dev/joke/Any?format=json?lang=en?type=single")
  json_data = json.loads(response.text)
  joke_type = json_data['type']
  if(joke_type == "single"):
    joke = json_data['joke']
  else:
    joke += "-" + json_data['setup'] + "\n-" + json_data['delivery']
  return joke
  
def create_categorical_jokes(category):
  joke = ""
  response = requests.get("https://v2.jokeapi.dev/joke/"+category+"?format=json?lang=en?type=single")
  json_data = json.loads(response.text)
  joke_type = json_data['type']
  if(joke_type == "single"):
    joke = json_data['joke']
  else:
    joke += "-" + json_data['setup'] + "\n-" + json_data['delivery']
  return joke

def show_categories():
  index = 1
  tmp = ""
  for category in categories:
    tmp += str(index) + " -> " + category +"\n"
    index+=1
  return tmp

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content.lower()

  if(msg.startswith("$joke")):
    try:
      rest = msg.split("$joke ", 1)[1]
      if rest == "categories":
        await message.channel.send(show_categories())
      elif rest.isnumeric():
        await message.channel.send(create_categorical_jokes(categories[int(rest)-1]))
    except:
      await message.channel.send(create_random_jokes())
  
keep_alive()

client.run(os.getenv('TOKEN'))