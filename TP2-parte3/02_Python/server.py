import socket
import threading
import uuid

HOST = "0.0.0.0"
PORT = 1234

OPTIONS = ["Piedra", "Papel", "Tijera"]
EMPATE = 3
GANA_1 = 1
GANA_2 = 2


# Función para determinar el ganador según las elecciones de los jugadores
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return EMPATE
    elif (
        (choice1 == "Piedra" and choice2 == "Tijera")
        or (choice1 == "Papel" and choice2 == "Piedra")
        or (choice1 == "Tijera" and choice2 == "Papel")
    ):
        return GANA_1
    else:
        return GANA_2


# Clase que maneja la sesión de juego entre dos jugadores
class GameSession:
    def __init__(self):
        self.players = {}
        self.lock = threading.Lock()
        self.ready_choice = (
            threading.Event()
        )  # Evento para indicar que ambos jugadores han hecho su elección
        self.ready_join = (
            threading.Event()
        )  # Evento para indicar que ambos jugadores se han conectado

    # Método para agregar un jugador a la sesión de juego
    def add_player(self, conn):
        with self.lock:
            player_id = len(self.players) + 1
            self.players[player_id] = {"conn": conn, "choice": None}
            return player_id

    # Método para guardar la elección de un jugador
    def set_choice(self, conn, player_id):
        with self.lock:
            choice = conn.recv(1024).decode()
            self.players[player_id]["choice"] = choice
            # Verificar si ambos jugadores han hecho su elección
            if all(player["choice"] is not None for player in self.players.values()):
                self.ready_choice.set()  # Marca el evento como listo cuando ambos jugadores han hecho su elección

    # Método para obtener el resultado del juego
    def get_result(self):
        choice1 = self.players[1]["choice"]
        choice2 = self.players[2]["choice"]
        return determine_winner(choice1, choice2)

    # Método para reiniciar las elecciones de los jugadores para la próxima ronda
    def reset_choices(self):
        with self.lock:
            for player in self.players.values():
                player["choice"] = None
            self.ready_choice.clear()  # Limpia el evento para la próxima ronda


# Clase que maneja el servidor de juego
class GameServer:
    def __init__(self, host=HOST, port=PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.sessions = {}
        print(f"Servidor iniciado en {host}:{port}")

    # Método que maneja cada cliente que se conecta al servidor
    def handle_client(self, conn):
        session_id = None
        try:
            data = conn.recv(1024).decode()
            command, *args = data.split()

            if command == "CREATE":
                # Crear una nueva sesión de juego
                session_id = str(uuid.uuid4())[:8]
                self.sessions[session_id] = GameSession()
                player_id = self.sessions[session_id].add_player(conn)
                conn.sendall(f"CREATED {session_id} {player_id}".encode())

                # Mantener al primer cliente esperando hasta que otro jugador se conecte
                session = self.sessions[session_id]
                session.ready_join.wait()  # Esperar al segundo jugador

                # Iniciar el juego
                threading.Thread(
                    target=self.play_game, args=(session, player_id), daemon=True
                ).start()

            elif command == "JOIN":
                # Unirse a una sesión de juego existente
                session_id = args[0]
                if (
                    session_id in self.sessions
                    and len(self.sessions[session_id].players) < 2
                ):
                    player_id = self.sessions[session_id].add_player(conn)
                    conn.sendall(f"JOINED {session_id} {player_id}".encode())

                    session = self.sessions[session_id]

                    # Liberar el evento para indicar que ambos jugadores están listos
                    session.ready_join.set()

                    # Enviar READY_TO_PLAY a ambos jugadores
                    for _, player in session.players.items():
                        player["conn"].sendall(b"READY_TO_PLAY")

                    # Iniciar el juego (si no se ha iniciado aún)
                    threading.Thread(
                        target=self.play_game, args=(session, player_id), daemon=True
                    ).start()
                else:
                    conn.sendall("SESSION_NOT_FOUND".encode())

        except Exception as e:
            print(f"Error en handle_client: {e}")
        finally:
            if session_id and session_id in self.sessions:
                del self.sessions[session_id]

    # Método que controla el flujo del juego entre dos jugadores
    def play_game(self, session, player_id):
        conn = session.players[player_id]["conn"]
        wins = 0
        loses = 0
        opponent_id = 2 if player_id == 1 else 1
        while True:
            # Esperar hasta que ambos jugadores estén listos (hayan hecho sus elecciones)
            session.set_choice(conn, player_id)
            session.ready_choice.wait()
            result = session.get_result()
            if result == player_id:
                result = "WIN"
                wins += 1
            elif result == EMPATE:
                result = "TIE"
            else:
                result = "LOSE"
                loses += 1

            score = f"Jugador {player_id} [{wins} - {loses}] Jugador {opponent_id}"
            result = result + " " + score

            # Enviar el resultado a ambos jugadores
            conn.sendall(result.encode())
            session.reset_choices()  # Reiniciar las elecciones para la próxima ronda

            data = conn.recv(1024).decode()
            if data == "EXIT":
                break
            elif data == "RESTART":
                continue

    # Iniciar el servidor y esperar conexiones
    def start(self):
        print("Esperando conexiones...")
        while True:
            conn, _ = self.server_socket.accept()
            threading.Thread(
                target=self.handle_client, args=(conn,), daemon=True
            ).start()


if __name__ == "__main__":
    server = GameServer()
    server.start()
