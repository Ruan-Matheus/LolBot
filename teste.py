import discord
from discord import app_commands
from discord.ext import commands
import logging
import requests
from pprint import pprint
import os
from getChampionById import get_champions_names_from_id

api_key = os.environ['api_key']

id = 'qpvXGiU4g38cTxL6VKiQlOpi3L2mW32UlgpbyKqJ8syZqdr9oB9oeD78gA'


def get_player_data(summoner_id, api_key):
 data = {}
 try:
  live_game_resquest = requests.get(
      f'https://br1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api_key}'
  )
  if live_game_resquest.status_code == 404:
    print("Not in game")
    return "Not in game"

  if live_game_resquest.status_code // 100 != 2:
   print(f"Error: Unexpected response {live_game_resquest}")

  live_game_json = live_game_resquest.json()

  game_length = live_game_json['gameLength']

  for i, v in enumerate((live_game_json['participants'])):
   if v['summonerId'] == id:
    team_id_pos = i

  teamId = live_game_json['participants'][team_id_pos]['teamId']

  allied_names = []
  allied_champs = []
  enemies_names = []
  enemies_champs = []
  for i, v in enumerate((live_game_json['participants'])):
    
   if v['teamId'] == teamId:
    allied_names.append(v['summonerName'])
    allied_champs.append(get_champions_names_from_id(v['championId']))
   else:
    enemies_names.append(v['summonerName'])
    enemies_champs.append(get_champions_names_from_id(v['championId']))
 
  
  playing_champion = live_game_json['participants'][team_id_pos]['championId']
   
 except requests.exceptions.RequestException as e:
  # A serious problem happened, like an SSLError or InvalidURL
  print("Error: {}".format(e))

  print(f"Game lenght: {game_lenght}")
  print(f"Allied champions: {allied_champs}")
  print(f"Allied champions: {allied_champs}")

 data = {
   'Game_length': game_length,
   'Teammates': allied_names,
   'Enemies': enemies_names,
   'Allied_champions': allied_champs,
   'Enemies_champions': enemies_champs,
   'Playing_champion': get_champions_names_from_id(playing_champion)
 }
  
 return data


def format_game_data(data):
  return f"Game duration: {data['Game_length'] // 60}:{data['Game_length'] % 60} mins\nTeammates: {data['Teammates']}\nEnemies: {data['Enemies']}\nAllied champions: {data['Allied_champions']}"


print(format_game_data(get_player_data(id, api_key)))
