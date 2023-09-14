import random
import discord
import os 
import requests
import json
import re
from datetime import date

def get_weather(city):
  my_secret2 = os.environ['Weather_key']
  
  response = requests.get("http://api.weatherapi.com/v1/current.json?key=" + my_secret2 + "&q=" + city)
  
  json_data = json.loads(response.text)
  
  location = json_data['location']['name']
  temp_c = json_data['current']['temp_c']
  temp_f = json_data['current']['temp_f']
  humidity = json_data['current']['humidity']
  wind_kph = json_data['current']['wind_kph']
  wind_mph = json_data['current']['wind_mph']
  condition = json_data['current']['condition']['text']
  image_url = "http:" + json_data['current']['condition']['icon']
  
  embed = discord.Embed(title=f"Weather for {location}", description=f"The condition in `{location}` is `{condition}`")
  embed.add_field(name="Temperature", value=f"C: {temp_c} | F: {temp_f}")
  embed.add_field(name="Humidity", value=f"{humidity}")
  embed.add_field(name="Wind Speeds", value=f"KPH: {wind_kph} | MPH: {wind_mph}")
  embed.set_thumbnail(url=image_url)
  
  return embed 

def get_dailyStocks(stock, date):
  my_secret3 = os.environ['Stock_key']
  stockS = stock.upper()
  
  response = requests.get("https://api.polygon.io/v1/open-close/" + stockS + "/" + date + "?adjusted=true&apiKey=" + my_secret3) 

  json_data = json.loads(response.text)

  afterhours = json_data['afterHours']
  close = json_data['close']
  fromDate = json_data['from']
  high = json_data['high']
  low = json_data['low']
  open = json_data['open']
  preMarket = json_data['preMarket']
  symbol = json_data['symbol']
  volume = json_data['volume']

  embed = discord.Embed(title="" + fromDate + " " + symbol + " Prices", description="Today's info on the " + symbol + " stock.")
  embed.add_field(name="PreMarket Price", value="" + str(preMarket))
  embed.add_field(name="High and Low Prices", value="High: " + str(high) + " / Low:" + str(low) )
  embed.add_field(name="Open and Close Prices", value="Open: " + str(open) + " / Close:" + str(close))
  embed.add_field(name="Trading Volume", value="" + str(volume))
  embed.add_field(name="After Hours closed Price", value="" + str(afterhours))

  return embed 

def definition(word):
  my_secret4 = os.environ['Def_key']
  
  response = requests.get("https://www.stands4.com/services/v2/defs.php?uid=12018&tokenid=" + my_secret4 + "&word=" + word+ "&format=json") 
  
  json_data = json.loads(response.text)['result']
  
  term = json_data[0]['term']
  definition = json_data[0]['definition']
  partofspeech = json_data[0]['partofspeech']
  example = json_data[0]['example']
  
  embed = discord.Embed(title="Word: " + term + ", " + partofspeech + "", description="" + definition + "") 
  embed.add_field(name="Word example", value="" + example)

  return embed

def handle_response(message) -> str:
  p_message = message.lower() 

  if p_message == 'hello':
    return 'hey there!'

  if p_message == 'roll':
    return str(random.randint(1,6))

  if p_message == '!help':
    return "`Get current weather details: !weather (city/zip/state/country)\nGet daily stock values: !stocks (stock name) (yyyy-mm-dd)\nRandom number between 1 and 6: roll\nGet today's date: !date\nGet a definition of a word w/ example: !definition (word)`"

  if p_message.startswith('!weather'):
    city = re.search('(?<=!weather ).+', p_message).group(0)
    return get_weather(city)

  if p_message.startswith('!stocks'):
    stock = re.search('(!stocks )(\w+)', p_message).group(2)
    date1 = re.search('(?<=!stocks )\w+ (\d+-\d+-\d+)', p_message).group(1)
    return get_dailyStocks(stock, date1)

  if p_message == '!date':
    today = date.today()
    return today 

  if p_message.startswith('!definition'):
    word = re.search('(?<=!definition ).+', p_message).group(0)
    return definition(word)