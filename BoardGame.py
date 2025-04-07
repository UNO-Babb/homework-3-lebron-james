#Example Flask App for a hexaganal tile game
#Logic is in this python file
from flask import Flask, render_template, redirect, url_for, session, request
import random

app = Flask(__name__)
app.secret_key = 'lebron_james_game'

# Initialize the board size
BOARD_SIZE = 50

# Function to roll a 10-sided die
def roll_die():
    return random.randint(1, 10)

# Initialize the players and board
def initialize_game(num_players):
    session['players'] = [{'position': 0, 'name': f'Player {i+1}'} for i in range(num_players)]
    session['current_player'] = 0
    session['game_over'] = False
    session['roll_value'] = None  # Store the roll value for display

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    num_players = int(request.form.get('num_players'))
    if 1 <= num_players <= 4:
        initialize_game(num_players)
        return redirect(url_for('game'))
    else:
        return "Please select between 1 to 4 players", 400

@app.route('/game')
def game():
    if 'players' not in session or session.get('game_over'):
        return redirect(url_for('home'))
    
    players = session['players']
    current_player = session['current_player']
    roll_value = session['roll_value']
    return render_template('game.html', players=players, current_player=current_player, roll_value=roll_value)

@app.route('/roll')
def roll():
    if 'players' not in session or session.get('game_over'):
        return redirect(url_for('home'))
    
    current_player_idx = session['current_player']
    player = session['players'][current_player_idx]

    # Roll the die
    roll_value = roll_die()
    session['roll_value'] = roll_value

    # Move player, but check if the move exceeds the 50th space
    new_position = player['position'] + roll_value
    if new_position <= BOARD_SIZE:
        player['position'] = new_position

    # Check if game is over
    if player['position'] == BOARD_SIZE:
        session['game_over'] = True
        winner = player['name']
        return render_template('game_over.html', winner=winner)

    # Move to the next player
    next_player_idx = (current_player_idx + 1) % len(session['players'])
    session['current_player'] = next_player_idx

    return redirect(url_for('game'))

@app.route('/reset')
def reset_game():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
