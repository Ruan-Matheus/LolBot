import requests
import discord
from discord import app_commands
from pprint import pprint

"Ver o elo da rapaziada com um comando com um bot de discord"

api_key = 'RGAPI-acd6e3fa-c899-455e-80aa-27d22b0d5db3'

players_names = ["Ruansitos", "Dutdudu"]
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

#for p in players_status:
#    pprint(p, sort_dicts = False, compact = True)

id_do_servidor =  1183402576172044309

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=id_do_servidor)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'teste', description='Testando') #Comando específico para seu servidor

async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Estou funcionando!", ephemeral = True) 
  

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'ruansitos', description='Mosta o elo de ruansitos') #Comando específico para seu servidor

async def slash3(interaction: discord.Interaction):
    await interaction.response.send_message(f"{player_status[0]['Tier']} {player_status[0]['Rank']}", ephemeral = False)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'dutdudu', description='Mosta o elo de dutdudu') #Comando específico para seu servidor

async def slash4(interaction: discord.Interaction):
    await interaction.response.send_message(f"{players_status[1]['Tier']} {players_status[1]['Rank']}", ephemeral = False) 




  

aclient.run('MTE4NDYyMDY1NzM4NDg5MDM4OA.G0VJ6W.hgQda5Os3qEQTLolD_sbiQIae8nVue8JmrJji8')
