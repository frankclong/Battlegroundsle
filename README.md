# Battlegroundsle

A Hearthstone Battlegrounds card guessing game built with Flask.

## Game Overview

Battlegroundsle is a Wordle-style game where you guess Hearthstone Battlegrounds cards. After each guess, you get feedback on:
- **Tier**: Whether the target card is higher or lower tier
- **Attack**: Whether the target card has more or less attack
- **Health**: Whether the target card has more or less health  
- **Minion Type**: Whether the target card has the same minion types

## Features

## How to Play 🎮

🎯🏆 Start typing the name of a card, select one and click guess! Use the clues provided to deduce what the mystery card is.

## Local Development

### Prerequisites

1. Python 3.9 or higher
2. Blizzard API credentials

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Battlegroundsle
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Blizzard API credentials**
   - Get your credentials from [Blizzard Developer Portal](https://develop.battle.net/access/clients)
   - Create a `config.py` file:
   ```python
   CLIENT_ID = "your_client_id_here"
   CLIENT_SECRET = "your_client_secret_here"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Deployment on Render

### Prerequisites

1. A Render account (free tier available)
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)

### Deployment Steps

1. **Prepare your repository**
   - Ensure all files are committed and pushed to your Git repository
   - Make sure `config.py` is in your `.gitignore` (it should be)

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your Git repository

3. **Configure the service**
   - **Name**: `battlegroundsle` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Add Environment Variables**
   - Go to the "Environment" tab
   - Add these environment variables:
     - `CLIENT_ID`: Your Blizzard API Client ID
     - `CLIENT_SECRET`: Your Blizzard API Client Secret

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your app will be available at `https://your-app-name.onrender.com`

### Environment Variables

The following environment variables are required for production:

| Variable | Description | Example |
|----------|-------------|---------|
| `CLIENT_ID` | Your Blizzard API Client ID | `507d40b0d2b0405a92dabe79423f167c` |
| `CLIENT_SECRET` | Your Blizzard API Client Secret | `P8aIHP1vK2WDV2pJjMPeVms5z50QGl1g` |

### Important Notes

- **API Rate Limits**: Blizzard API has rate limits. Consider implementing caching for production use.
- **Security**: Never commit your `config.py` file to version control.
- **Performance**: The app loads all cards on startup, which may take a few seconds.

## File Structure

```
Battlegroundsle/
├── app.py                 # Main Flask application
├── config.py             # API credentials (not in version control)
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment configuration
├── .gitignore           # Git ignore rules
├── static/
│   ├── styles.css       # All CSS styling
│   ├── game.js          # JavaScript functionality
│   └── Belwe-Bold.otf   # Custom font
├── templates/
│   └── index.html       # Main HTML template
└── README.md            # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **API**: Blizzard Hearthstone API
- **Deployment**: Render
- **Font**: Belwe-Bold (Hearthstone-style font)

## Motivation and Final Thoughts
I started playing Hearthstone quite early on, just before the Curse of Naxxramus was released. Since then, I've been going in and out of playing. The release of Battlegrounds was a refreshing new game mode that incorporated many of the characters from the world I loved. I haven't been playing consistently this whole time, but prior to the start of this project I was getting really into it with my friends and one day we wanted to look for a Wordle version to test our knowledge. We found a Hearthstone version, but that was for the main card game and not Battlegrounds so I decided to make one myself. 

This is my first Flask app and I had a lot of fun working on it, especially adding the little details that I feel make or break the game. I hope someone out there can have fun playing Battlegroundsle and flex their Battlegrounds knowledge to their friends. 

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes. Hearthstone is a trademark of Blizzard Entertainment. 


Currently hosted at http://battlegroundsle.pythonanywhere.com/