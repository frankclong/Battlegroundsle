import requests 
from BattlegroundsCard import BattlegroundsCard
from config import CLIENT_ID, CLIENT_SECRET
import random
from card_comparison_functions import *

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
    type_dict[-1] = 'None'

    return type_dict

cards_dict = load_cards(token)
minion_type_dict = load_minion_types(token)
NUM_ATTEMPTS = 5

# Play
def play():
    # Get random card
    target_card = random.choice(list(cards_dict.values()))

    # Get guesses
    for i in range(NUM_ATTEMPTS): 
        guess_card = None
        while True:
            guess_card_name = input('Enter guess: ')
            if guess_card_name in cards_dict.keys():
                guess_card = cards_dict[guess_card_name]
                break
            else:
                print("Invalid choice! Please enter a valid card name")

        # Return property matches
        check = compare_cards(target_card, guess_card, minion_type_dict)
        print(check)

        # Check if correct
        correct = True
        for category in check.keys():
            if check[category] != 0:
                correct = False
        if guess_card.name != target_card.name:
            correct = False

        if correct:
            print("Congrats! You got it!")
            break
    print(target_card.name)

play()