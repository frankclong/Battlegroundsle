import requests 
from BattlegroundsCard import BattlegroundsCard
from config import CLIENT_ID, CLIENT_SECRET
import random

# Init - load cards and metadata
# Get access token
token_url = "https://oauth.battle.net/token"
data = {
    'grant_type' : 'client_credentials'
}
client_id = CLIENT_ID
client_secret = CLIENT_SECRET

token_response = requests.post(token_url, data=data, auth=(client_id, client_secret))
token = token_response.json()['access_token'] 


def load_cards(token):
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
        'pageSize' : 500, # hard coded
    }

    cards_response = requests.get(url, headers=headers, params=params)
    # print(cards_response.json())
    cards = cards_response.json()['cards']
    cards_dict = {}
    for card_info in cards:
        card = BattlegroundsCard(card_info)
        cards_dict[card.name] = card
    
    return cards_dict

def load_minion_types(token):
    url = "https://us.api.blizzard.com/hearthstone/metadata/"
    full_token = 'Bearer ' + token
    headers = {
        'Authorization' : full_token
    }
    params = {
        'namespace' : 'dynamic-us',
        'region' : 'us',
        'locale' : 'en_US',
    }
    metadata_response = requests.get(url, headers=headers, params=params)
    type_infos = metadata_response.json()['minionTypes']
    type_dict = {}
    for type_info in type_infos:
        type_dict[type_info['id']] = type_info['name']

    return type_dict

cards_dict = load_cards(token)
minion_type_dict = load_minion_types(token)

# Play
def play():
    # Get random card
    target_card = random.choice(list(cards_dict.keys()))

    # Get guess

    # Return property matches

    # Check if correct
    print(target_card)

play()