import discord
import os 
import responses

async def send_message(message, user_message, is_private):
  try:
    response = responses.handle_response(user_message)
    if isinstance(response, discord.embeds.Embed):
      await message.author.send(embed = response) if is_private else await message.channel.send(embed = response)
    else: 
      await message.author.send(response) if is_private else await message.channel.send(response)
  except Exception as e:
    print(e)

def run_discord_bot(): 
  my_secret = os.environ['Bot_key']
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)
  
  @client.event
  async def on_ready():
   print('We have logged in as {0.user}'.format(client))

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel) 

    if user_message[0] == '?':
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else:
      await send_message(message, user_message, is_private=False)
        
        
  
  client.run(my_secret)