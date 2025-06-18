from flask import Flask, render_template, request, jsonify
import requests 
from BattlegroundsCard import BattlegroundsCard
import random
from card_comparison_functions import *
import jinja2
import os

# Get API credentials from environment variables (production) or config file (development)
def get_api_credentials():
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    
    if not client_id or not client_secret:
        # Fall back to config file for local development
        try:
            from config import CLIENT_ID, CLIENT_SECRET
            return CLIENT_ID, CLIENT_SECRET
        except ImportError:
            raise ValueError("API credentials not found. Set CLIENT_ID and CLIENT_SECRET environment variables or create a config.py file.")
    
    return client_id, client_secret

# Init - load cards and metadata
# Get access token
token_url = "https://oauth.battle.net/token"
data = {
    'grant_type' : 'client_credentials'
}
client_id, client_secret = get_api_credentials()

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
        # Skip non-minions
        if card_info['cardTypeId'] != 4: 
            continue
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

# Constants
CARDS_DICT = load_cards(token)
MINION_TYPE_DICT = load_minion_types(token)
CARD_NAMES = [card.name for card in CARDS_DICT.values()]
NUM_ATTEMPTS = 5 # not used

# Start game
target_card = random.choice(list(CARDS_DICT.values()))
print(target_card.name, flush=True)

app = Flask(__name__)

# Dynamic data
guesses_and_rows = []
finished = False

def reset_game():
    global target_card
    global guesses_and_rows
    global finished
    target_card = random.choice(list(CARDS_DICT.values()))
    print(target_card.name, flush=True)
    finished = False
    guesses_and_rows.clear()

def get_guesses():
    return [guess.name for guess, _ in guesses_and_rows ]

def get_rows():
    return [row for _, row in guesses_and_rows]

def check_value_to_color(value):
    if abs(value) == 0:
        return "green"
    elif abs(value) == 1:
        return "orange"
    else:
        return "red"

def is_guess_correct(check):
    for val in check.values():
        if val != 0:
            return False
    return True

def get_value_and_arrows_tuple(value, check_value, show_arrows = False):
    if check_value == 0:
        hide_text_color = "green-text"
    elif check_value == 1:
        hide_text_color = "orange-text"
    else:
        hide_text_color = "red-text"
    if not show_arrows or check_value == 0:
        return (hide_text_color, value, hide_text_color)
    if check_value > 0:
        return ("white-text", value, hide_text_color)
    elif check_value < 0:
        return (hide_text_color, value, "white-text")

COLUMNS = ["Card", "Tier", "Attack", "Health", "Minion Type"]
NUMERIC_COLUMNS = ["Tier", "Attack", "Health"]

@app.route('/', methods=['GET'])
def index():
    table_rows = get_rows()    
    return render_template('index.html', table_rows=table_rows, finished=finished)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    input_text = request.form['q']
    suggestions = [] if len(input_text.strip()) == 0 else [name for name in CARD_NAMES if input_text.lower() in name.lower()]
    suggestions.sort()
    return jsonify(suggestions[:10])

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    global guesses_and_rows
    global finished
    
    guess_card_name = request.form['guess']
    
    if guess_card_name not in get_guesses() and not finished:
        if guess_card_name in CARDS_DICT.keys():
            guess_card = CARDS_DICT[guess_card_name]

            # Return property matches
            check = compare_cards(target_card, guess_card, MINION_TYPE_DICT)

            # Create a row
            minionTypesString = ", ".join([MINION_TYPE_DICT[type_id] for type_id in guess_card.minion_types])
            values = [
                get_value_and_arrows_tuple(guess_card.image_url, 0, False), 
                get_value_and_arrows_tuple(guess_card.tier, check['Tier'], True), 
                get_value_and_arrows_tuple(guess_card.attack, check['Attack'], True), 
                get_value_and_arrows_tuple(guess_card.health, check['Health'], True), 
                get_value_and_arrows_tuple(minionTypesString, check['Minion Type'], False)]
            
            colors = []
            for col in COLUMNS:
                if col == "Card":
                    colors.append("blank")
                else:
                    colors.append(check_value_to_color(check[col]))

            # Add the row to the table_rows list
            row = list(zip(values, colors))
            guesses_and_rows.append((guess_card, row))
            finished = is_guess_correct(check)
            
            return jsonify({
                'success': True,
                'row': row,
                'finished': finished,
                'message': 'Congratulations you got it!' if finished else ''
            })
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
    else:
        return jsonify({'success': False, 'error': 'Card already guessed or game finished'})

@app.route('/reset_game', methods=['POST'])
def reset_game_route():
    reset_game()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Use environment variable for port (Render requirement)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)