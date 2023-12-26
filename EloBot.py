import discord
from discord import app_commands
from discord.ext import commands
import logging
import requests
from pprint import pprint
import os

api_key = os.environ['api_key']
bot_token = os.environ['bot_token']
server_id = os.environ['server_id']

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')

player_status = {}


def get_player_data(summoner_name, api_key):
 try:
  summomer_request = requests.get(
      f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
  )

  if summomer_request.status_code // 100 != 2:
   print(f"Error: Unexpected response {summomer_request}")

  summoner_json = summomer_request.json()
  summoner_name = summoner_json['name']
  summoner_id = summoner_json['id']
  summoner_account_id = summoner_json['accountId']
  summmoner_puuid = summoner_json['puuid']

  #pprint(summoner_json, indent= 4)

 except requests.exceptions.RequestException as e:
  # A serious problem happened, like an SSLError or InvalidURL
  print("Error: {}".format(e))

 try:
  # Request url for the entries of a summoner --> https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_account_id}?api_key={api_key}
  entries_request = requests.get(
      f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'
  )
  if entries_request.status_code // 100 != 2:

   print(f"Error: Unexpected response {entries_request}")

  entries_json = entries_request.json()
  pprint(entries_json, indent=4)

  for i in range(len(entries_json)):
   if entries_json[i]['queueType'] == 'RANKED_SOLO_5x5':
    n_solo = i
    break

  player_status = {
      'Name':
      summoner_name,
      'Tier':
      entries_json[n_solo]['tier'] if entries_json else 'Unranked',
      'Rank':
      entries_json[n_solo]['rank'] if entries_json else 'Unranked',
      'LP':
      entries_json[n_solo]['leaguePoints'] if entries_json else 0,
      'Wins':
      entries_json[n_solo]['wins'] if entries_json else 0,
      'Losses':
      entries_json[n_solo]['losses'] if entries_json else 0,
      'Win Rate': round(
      entries_json[n_solo]['wins'] /
      (entries_json[n_solo]['wins'] + entries_json[n_solo]['losses']) *
      100, 2) if entries_json else 0
  }

 except Exception as f:
  print(f"Erro {f}")

 return player_status


def format_data(player_data):
 if player_data:
  return f"{player_data['Name']} - {player_data['Tier']} - {player_data['Rank']}\n - Wins: {player_data['Wins']}\n- Losses: {player_data['Losses']}\n- Win Rate: {player_data['Win Rate']}%"


intents = discord.Intents.default()
intents.message_content = True

# Prefixo para os comandos do bot
bot_prefix = "!"

# Criação de um objeto bot com um prefixo
bot = commands.Bot(intents=intents, command_prefix=bot_prefix)


# Evento chamado quando o bot está pronto
@bot.event
async def on_ready():
 print(f'Logged in as {bot.user.name}')


@bot.command(name='elo', help='Shows the elo of the player')
async def elo(ctx, player_name: str):
 print(player_name)
 player_data = get_player_data(player_name, api_key)
 formatted_data = format_data(player_data)
 await ctx.send(f'{formatted_data}!')


# Comando simples: !hello
@bot.command(name='hello', help='Responds with a hello message.')
async def hello(ctx):
 await ctx.send(f'Hello, {ctx.author.mention}!')


# Comando com argumento: !greet <name>
@bot.command(name='greet', help='Greets the specified user.')
async def greet(ctx, name: str):
 await ctx.send(f'Hello, {name}!')


# Comando personalizado: !custom
@bot.command(name='custom', help='A custom command.')
async def custom(ctx):
 await ctx.send('This is a custom command!')

'''
@bot.commnad(name='help', help='Shows the help message.')
async def help(ctx):
 await ctx.send'''

    
# Inicialização do bot
bot.run(bot_token, log_handler=handler)
