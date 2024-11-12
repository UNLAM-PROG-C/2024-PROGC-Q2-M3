import socket

# Configurar la IP y el puerto del servidor aquí
SERVER_IP = "127.0.0.1"  # Aquí puedes poner la IP del servidor
SERVER_PORT = 12345  # Puerto donde el servidor escucha

# Función para crear una partida
def create_game(server_socket):
    try:
        server_socket.sendall(b"CREATE")
        response = server_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {response}")
        if response.startswith("CREATED"):
            session_id, player_id = response.split()[1], response.split()[2]
            print(f"Partida creada con código {session_id}. Tu ID es {player_id}")

            # Esperar a que otro jugador se una
            print("Esperando a otro jugador...")
            # response = server_socket.recv(1024).decode()
            # if response == "READY_TO_PLAY":
            #     # print("Ambos jugadores están listos. ¡Comienza el juego!")
            #     return session_id
            # else:
            #     print("Error: No se recibió la confirmación de inicio de juego.")
            #     return None
            return session_id
        else:
            print("Error al crear la partida.")
            return None
    except Exception as e:
        print(f"Error al crear la partida: {e}")
        return None

# Función para unirse a una partida existente
def join_game(server_socket):
    try:
        session_id = input("Ingresa el código de la sesión a la que deseas unirte: ")
        server_socket.sendall(f"JOIN {session_id}".encode())

        response = server_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {response}")  # Imprimir respuesta para depurar

        if response.startswith("JOINED"):
            _, session_id, player_id = response.split()
            print(f"Te has unido a la partida {session_id}. Tu ID es {player_id}")
            return session_id
        elif response == "SESSION_NOT_FOUND":
            print("El código de sesión no es válido o la sesión no existe.")
            return None
        else:
            print("No se pudo unir a la partida.")
            return None
    except Exception as e:
        print(f"Error al unirse a la partida: {e}")
        return None

# Función principal del cliente
def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))

        print("Elige una opción:")
        print("1. Crear partida")
        print("2. Unirse a una partida")
        option = input("Opción (1/2): ")

        if option == "1":
            session_id = create_game(server_socket)
        elif option == "2":
            session_id = join_game(server_socket)
        else:
            print("Opción inválida.")
            server_socket.close()
            return

        if session_id:
            # Esperar la respuesta "READY_TO_PLAY"
            response = server_socket.recv(1024).decode()
            print(f"Respuesta del servidor: {response}")

            if response == "READY_TO_PLAY":
                print("Ambos jugadores están listos. ¡Comienza el juego!")
                while True:
                    choice = input("Elige Piedra, Papel o Tijera: ").capitalize()
                    if choice in ["Piedra", "Papel", "Tijera"]:
                        server_socket.sendall(choice.encode())
                        response = server_socket.recv(1024).decode()
                        print(response)
                        # Control de continuación o salida del juego
                        continue_playing = input("¿Deseas seguir jugando? (si/no): ").lower()
                        if continue_playing == 'si':
                            # Enviar solicitud para reiniciar la partida si es necesario
                            server_socket.sendall(b"RESTART")
                            continue
                        else:
                            server_socket.sendall(b"EXIT")
                            print("Saliendo de la partida...")
                            break

    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()