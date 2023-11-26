# A simple program to view your League of legends status

import requests
import json

name = input("Your game name: ")

# Get a summoner by game name -> /lol/summoner/v4/summoners/by-name/{summonerName}
summoner = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key=RGAPI-600e4868-1c0f-4409-84a8-bb43d18f7f5c')
response_code = summoner.status_code
summoner_json = summoner.json()

summoner_name = summoner_json["name"]
summoner_id = summoner_json["id"]
summoner_puuid = summoner_json["puuid"]
summoner_level = summoner_json["summonerLevel"]

print(f"Response code: {response_code}")
print(f"Your summoner name: {summoner_name}")
print(f"Your summoner id: {summoner_id}")
print(f"Your summoner puuid: {summoner_puuid}")
print(f"Your summoner level: {summoner_level}")


# Get a champion mastery by puuid
mastery = requests.get(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_puuid}?api_key={api_key}")