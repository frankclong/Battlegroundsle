from flask import Flask, render_template, request
import requests 
from BattlegroundsCard import BattlegroundsCard
from config import CLIENT_ID, CLIENT_SECRET
import random
from card_comparison_functions import *
import jinja2

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
target_card = random.choice(list(cards_dict.values()))
print(target_card.name)

app = Flask(__name__)

# Define a list to store the table rows
table_rows = []

def reset_game():
    target_card = random.choice(list(cards_dict.values()))
    table_rows.clear()

def check_value_to_color(value):
    if abs(value) == 0:
        return "green"
    elif abs(value) == 1:
        return "orange"
    else:
        return "red"


COLUMNS = ["Name", "Tier", "Attack", "Health", "Minion Type"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'guess' in request.form:
            # Get the value from the text input field
            guess_card_name = request.form['input_text']
            
            # TODO auto suggest
            # TODO handle invalid name
            # TODO new game
            if guess_card_name in cards_dict.keys():
                guess_card = cards_dict[guess_card_name]

                # Return property matches
                check = compare_cards(target_card, guess_card, minion_type_dict)

                # Create a row
                minionTypesString = ", ".join([minion_type_dict[type_id] for type_id in guess_card.minion_types])
                values = [guess_card_name, guess_card.tier, guess_card.attack, guess_card.health, minionTypesString]
                colors = []
                for col in COLUMNS:
                    if col == "Name":
                        colors.append("blank")
                    else:
                        colors.append(check_value_to_color(check[col]))

                # Add the row to the table_rows list
                table_rows.append(list(zip(values, colors)))
        elif 'reset' in request.form:
            reset_game()

    # Render the index.html template with the table_rows
    
    return render_template('index.html', table_rows=table_rows)


if __name__ == '__main__':
    app.run()