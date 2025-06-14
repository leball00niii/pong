# server.py
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# État initial
game_state = {
    "ball": [400, 300],
    "ball_vel": [5, 5],
    "paddles": {
        0: 250,
        1: 250
    },
    "score": [0, 0]
}

connected_players = 0
lock = threading.Lock()

@app.route("/join", methods=["GET"])
def join():
    global connected_players
    with lock:
        if connected_players >= 2:
            return jsonify({"error": "Game full"}), 403
        player_id = connected_players
        connected_players += 1
    return jsonify({"player_id": player_id})

@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    player_id = data.get("player_id")
    paddle_y = data.get("paddle_y")
    with lock:
        game_state["paddles"][player_id] = paddle_y
    return jsonify(success=True)

@app.route("/state", methods=["GET"])
def state():
    with lock:
        return jsonify(game_state)

def update_game():
    while True:
        time.sleep(0.03)
        with lock:
            game_state["ball"][0] += game_state["ball_vel"][0]
            game_state["ball"][1] += game_state["ball_vel"][1]

            # Bords haut/bas
            if game_state["ball"][1] <= 0 or game_state["ball"][1] >= 600:
                game_state["ball_vel"][1] *= -1

            # Collisions raquettes
            if game_state["ball"][0] <= 60 and game_state["paddles"][0] < game_state["ball"][1] < game_state["paddles"][0] + 100:
                game_state["ball_vel"][0] *= -1
            elif game_state["ball"][0] >= 740 and game_state["paddles"][1] < game_state["ball"][1] < game_state["paddles"][1] + 100:
                game_state["ball_vel"][0] *= -1

            # Points
            if game_state["ball"][0] < 0:
                game_state["score"][1] += 1
                game_state["ball"] = [400, 300]
            elif game_state["ball"][0] > 800:
                game_state["score"][0] += 1
                game_state["ball"] = [400, 300]

# Lancer la boucle de jeu dans un thread
threading.Thread(target=update_game, daemon=True).start()

# Point d'entrée Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
