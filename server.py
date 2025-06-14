import socket
import threading
import pickle

HOST = '0.0.0.0'
PORT = 12345

# État initial du jeu
game_state = {
    "ball": [400, 300],
    "ball_vel": [5, 5],
    "paddles": {
        0: 250,
        1: 250
    },
    "score": [0, 0]
}

clients = {}

def handle_client(conn, player_id):
    global game_state
    conn.send(pickle.dumps(player_id))  # Envoie l'ID au client
    while True:
        try:
            paddle_y = pickle.loads(conn.recv(1024))
            game_state["paddles"][player_id] = paddle_y
        except:
            break

def update_game():
    while True:
        game_state["ball"][0] += game_state["ball_vel"][0]
        game_state["ball"][1] += game_state["ball_vel"][1]

        # Collisions avec le haut/bas
        if game_state["ball"][1] <= 0 or game_state["ball"][1] >= 600:
            game_state["ball_vel"][1] *= -1

        # Collisions avec les raquettes
        if game_state["ball"][0] <= 60 and game_state["paddles"][0] < game_state["ball"][1] < game_state["paddles"][0] + 100:
            game_state["ball_vel"][0] *= -1
        elif game_state["ball"][0] >= 740 and game_state["paddles"][1] < game_state["ball"][1] < game_state["paddles"][1] + 100:
            game_state["ball_vel"][0] *= -1

        # Points
        if game_state["ball"][0] < 0:
            game_state["score"][1] += 1
            game_state["ball"] = [400, 300]
        if game_state["ball"][0] > 800:
            game_state["score"][0] += 1
            game_state["ball"] = [400, 300]

        for conn in clients.values():
            try:
                conn.sendall(pickle.dumps(game_state))
            except:
                continue

import time
def start_server():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Serveur en attente de 2 joueurs...")

    player_id = 0
    while player_id < 2:
        conn, addr = server.accept()
        print(f"Connexion du joueur {player_id} depuis {addr}")
        clients[player_id] = conn
        threading.Thread(target=handle_client, args=(conn, player_id)).start()
        player_id += 1

    threading.Thread(target=update_game).start()

start_server()
