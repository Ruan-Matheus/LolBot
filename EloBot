import requests
import discord
from discord import app_commands
from pprint import pprint

"Ver o elo da rapaziada com um comando com um bot de discord"

api_key = 'RGAPI-acd6e3fa-c899-455e-80aa-27d22b0d5db3'

players_names = ["Ruansitos", "Dutdudu", "Ferballen", "n digitarei", "Mânoel Gomes"]
player_status = {}
players_status = []

for player_name in players_names:
    try:
        summomer_request = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={api_key}')
        if not summomer_request.status_code // 100 == 2:
            print(f"Error: Unexpected response {summomer_request}")
        
        summoner_json = summomer_request.json()
        summoner_name = summoner_json['name']
        summoner_id = summoner_json['id']
        summoner_account_id = summoner_json['accountId']
        summmoner_puuid = summoner_json['puuid']

#         pprint(summoner_json, indent= 4)
        
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
         print("Error: {}".format(e))
         
    try:
        # Request url for the entries of a summoner --> https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_account_id}?api_key={api_key}
        entries_request = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
        if not entries_request.status_code // 100 == 2:
            print(f"Error: Unexpected response {entries_request}")

        entries_json = entries_request.json()
#         pprint(entries_json, indent= 4)
            
        n_solo = 1 if len(entries_json) > 1 and entries_json[1]['queueType'] == 'RANKED_SOLO_5x5' else 0
        
        player_status = {
            'Name': summoner_name,
            'Tier': entries_json[n_solo]['tier'] if entries_json else 'Unranked',
            'Rank': entries_json[n_solo]['rank'] if entries_json else 'Unranked',
            'Wins': entries_json[n_solo]['wins'] if entries_json else 0,
            'Losses': entries_json[n_solo]['losses'] if entries_json else 0,
            'Win Rate': entries_json[n_solo]['wins'] / (entries_json[n_solo]['wins'] + entries_json[n_solo]['losses']) * 100 if entries_json else 0
        }

              
    except Exception as f:
        print(f"Erro {f}")
    
    players_status.append(player_status.copy())
    
for p in players_status:
    pprint(p, sort_dicts = False, compact = True)
