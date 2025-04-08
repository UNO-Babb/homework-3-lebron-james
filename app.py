#Example Flask App for a hexaganal tile game
#Logic is in this python file
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

MAX_SPACES = 50  # Total spaces on the board

# Function to simulate a 10-sided die roll
def roll_die():
    return random.randint(1, 10)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Initialize the game if it's the first time
        if 'players' not in session:
            # Get player names from form and initialize the players' positions
            player_names = [request.form.get(f"player{i}") for i in range(1, 5) if request.form.get(f"player{i}")]
            session['players'] = {name: 0 for name in player_names}  # Starting position 0
            session['turn_index'] = 0  # Player 1 starts
            session['game_over'] = False
            session['winner'] = None
            session['rolls'] = {name: 0 for name in player_names}  # Store each player's roll history

        # Proceed with the game if it is not over
        if not session['game_over']:
            # Get the current player based on turn index
            current_player = list(session['players'].keys())[session['turn_index']]
            roll = roll_die()
            new_position = session['players'][current_player] + roll

            # Store the roll for the current player
            session['rolls'][current_player] = roll

            # Ensure the player does not move past the 50th space
            if new_position <= MAX_SPACES:
                session['players'][current_player] = new_position

            # Check if the player has reached space 50
            if session['players'][current_player] == MAX_SPACES:
                session['game_over'] = True
                session['winner'] = current_player
            else:
                # Move to the next player (turn cycle)
                session['turn_index'] = (session['turn_index'] + 1) % len(session['players'])

        return redirect(url_for('index'))

    return render_template("index.html", players=session.get('players', {}),
                           rolls=session.get('rolls', {}),
                           player_names=list(session.get('players', {}).keys()),
                           game_over=session.get('game_over', False),
                           winner=session.get('winner', None))


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()  # Clear the session to reset the game state
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
