import requests
from pprint import pprint

"Ver o elo da rapaziada com um comando com um bot de discord"

key = 'RGAPI-201ddfd1-407c-43f3-b6e8-8a8eac8a81ee'

players_names = ["Ruansitos", "Dutdudu", "Ferballen"]
player_status = {}
players_status = []

for player_name in players_names:
    try:
        summomer_request = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={key}')
        if not summomer_request.status_code // 100 == 2:
            print(f"Error: Unexpected response {summomer_request}")
        
        summoner_json = summomer_request.json()
        summoner_name = summoner_json['name']
        summoner_id = summoner_json['id']
        summoner_account_id = summoner_json['accountId']
        summmoner_puuid = summoner_json['puuid']

        pprint(summoner_json, indent= 4)
        
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
         print("Error: {}".format(e))
         
    try:
        # Request url for the entries of a summoner --> https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_account_id}?api_key={api_key}
        entries_request = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_xclsid}?api_key={key}')
        if not entries_request.status_code // 100 == 2:
            print(f"Error: Unexpected response {entries_request}")
            
        entries_json = entries_request.json()
        player_status['Name'] = summoner_name
        player_status['Tier'] = entries_json['tier']
        player_status['Rank'] = entries_json['rank']
        
    except:
        pass
    
    print(player_status)
