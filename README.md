# Battlegroundsle

Currently hosted at http://battlegroundsle.pythonanywhere.com/

## Set-up
1. Ensure you have Python 3 installed
2. Clone a copy of this repo. 
3. You can set up the required libraries by running `pip install -r requirements.txt` from the Battlegroundsle directory. If preferred, you can create a virtual environment first.
4. Visit https://develop.battle.net/ to set up a client.
5. Create a `config.py` file in the same directory as `app.py` and add two constants to it - `CLIENT_ID` and `CLIENT_SECRET` which can be found under a client's credentials
6. Run `app.py` locally to see if it works!

## How to play
Start typing the name of a card, select one and click guess! Use the clues provided to deduce what the mystery card is.

## Motivation and Final Thoughts
I started playing Hearthstone quite early on, just before the Curse of Naxxramus was released. Since then, I've been going in and out of playing. The release of Battlegrounds was a refreshing new game mode that incorporated many of the characters from the world I loved. I haven't been playing consistently this whole time, but prior to the start of this project I was getting really into it with my friends and one day we wanted to look for a Wordle version to test our knowledge. We found a Hearthstone version, but that was for the main card game and not Battlegrounds so I decided to make one myself. 

This is my first Flask app and I had a lot of fun working on it, especially adding the little details that I feel make or break the game. I hope someone out there can have fun playing Battlegroundsle and flex their Battlegrounds knowledge to their friends. 