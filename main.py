import requests 
from BattlegroundsCard import BattlegroundsCard
from config import CLIENT_ID, CLIENT_SECRET

# Get access token
token_url = "https://oauth.battle.net/token"
data = {
    'grant_type' : 'client_credentials'
}
client_id = CLIENT_ID
client_secret = CLIENT_SECRET

token_response = requests.post(token_url, data=data, auth=(client_id, client_secret))
token = token_response.json()['access_token'] 
print(token)

url = "https://us.api.blizzard.com/hearthstone/cards/"
full_token = 'Bearer ' + token
headers = {
    'Authorization' : full_token
}
params = {
    'namespace' : 'dynamic-us',
    'region' : 'us',
    'locale' : 'en_US',
    'gameMode' : 'battlegrounds',
    'tier' : '1,2,3,4,5,6',
}

cards_response = requests.get(url, headers=headers, params=params)
# print(cards_response.json())
cards = cards_response.json()['cards']

# nned to paginate
# need to look at minionTypeId and multiTypeId
print(cards[0])
cards_list = []
for card in cards:
    new_card = BattlegroundsCard(card)
    cards_list.append(new_card)

print(len(cards_list))
my_card = cards_list[17]
print(my_card.name)
print(my_card.minionTypes)
print(my_card.tier)
print(my_card.health)
print(my_card.attack)
