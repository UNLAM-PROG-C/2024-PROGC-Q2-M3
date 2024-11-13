from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, simpledialog
import socket


# Configuración del servidor
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
ROUNDS = 5
ROUNDS_TO_WIN = (ROUNDS // 2) + 1


class GameClientApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.root.resizable(width=False, height=False)
        self.root.title("Piedra, Papel o Tijeras")
        self.root.configure(background="black")

        # Configuración del socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Variables del juego
        self.session_id = None
        self.player_id = None
        self.wins = 0
        self.loses = 0
        self.choice_var = None  # Variable para la opción seleccionada

        # Cargar y redimensionar la imagen de fondo
        self.bg_image = Image.open("background.jpg").resize((800, 600))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Crear un Canvas para la imagen de fondo y colocarlo en la ventana
        self.background_canvas = Canvas(self.root, width=800, height=600)
        self.background_canvas.pack(fill="both", expand=True)
        self.background_canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")

        # Colores y estilo de los botones y etiquetas
        self.color1 = '#0a0b0c'
        self.color2 = '#f5267b'
        self.color3 = '#ff3d8d'
        self.color4 = 'BLACK'

        # Imágenes de botones
        self.imag_join_game = ImageTk.PhotoImage(Image.open('join.png').resize((20, 20)))
        self.imag_create_game = ImageTk.PhotoImage(Image.open('new_game.png').resize((20, 20)))
        self.imag_piedra_option = ImageTk.PhotoImage(Image.open('piedraOption.png').resize((20, 20)))
        self.imag_papel_option = ImageTk.PhotoImage(Image.open('papelOption.png').resize((20, 20)))
        self.imag_tijera_option = ImageTk.PhotoImage(Image.open('tijeraOption.png').resize((20, 20)))

        # Interfaz de bienvenida
        self.setup_welcome_screen()

    def setup_welcome_screen(self):
        """Configura la pantalla de bienvenida con opciones para unirse o crear partida."""
        self.clear_screen()

        # Conectar al servidor
        self.server_socket.connect((SERVER_IP, SERVER_PORT))

        # Etiqueta de bienvenida
        self.welcome_label = Label(self.root, text="¡Bienvenido a Piedra, Papel o Tijeras!", fg="white", bg="black", font=("Helvetica", 24))
        self.welcome_label.place(x=200, y=100)

        # Botón "Crear Partida"
        self.create_button = Button(
            self.root, text='Crear Partida', background=self.color2, foreground=self.color4,
            width=200, height=50, highlightthickness=0, activebackground=self.color3, activeforeground=self.color4,
            cursor='hand1', border=0, image=self.imag_create_game, compound=LEFT,
            command=self.create_game, font=('Arial', 15, 'bold')
        )
        self.create_button.place(x=300, y=250)

        # Botón "Unirse a Partida"
        self.join_button = Button(
            self.root, text='Unirse a Partida', background=self.color2, foreground=self.color4,
            width=200, height=50, highlightthickness=0, activebackground=self.color3, activeforeground=self.color4,
            cursor='hand1', border=0, image=self.imag_join_game, compound=LEFT,
            command=self.join_game, font=('Arial', 15, 'bold')
        )
        self.join_button.place(x=300, y=350)

    def create_game(self):
        """Crea una nueva partida."""
        self.server_socket.sendall(b"CREATE")
        response = self.server_socket.recv(1024).decode()
        if response.startswith("CREATED"):
            self.session_id, self.player_id = response.split()[1], response.split()[2]
            messagebox.showinfo("Partida Creada", f"Código de sesión: {self.session_id}\nID de jugador: {self.player_id}")
            self.wait_for_player()
        else:
            messagebox.showerror("Error", "No se pudo crear la partida.")

    def join_game(self):
        """Solicita unirse a una partida existente."""
        session_id = simpledialog.askstring("Unirse a partida", "Ingrese el código de sesión:")
        if session_id:
            self.server_socket.sendall(f"JOIN {session_id}".encode())
            response = self.server_socket.recv(1024).decode()
            if response.startswith("JOINED"):
                _, self.session_id, self.player_id = response.split()
                messagebox.showinfo("Unido a Partida", f"Te uniste a la partida {self.session_id} con ID {self.player_id}")
                self.wait_for_player()
            else:
                messagebox.showerror("Error", "Código de sesión inválido o sesión no encontrada.")

    def wait_for_player(self):
        """Espera a que otro jugador se una para comenzar el juego."""
        response = self.server_socket.recv(1024).decode()
        if response == "READY_TO_PLAY":
            messagebox.showinfo("Listo", "¡Ambos jugadores están listos! Comienza el juego.")
            self.start_game()
        else:
            messagebox.showerror("Error", "Error al iniciar la partida.")

    def start_game(self):
        """Configura la interfaz del juego con estilo y botones con imágenes."""
        self.clear_screen()

        # Frame de opciones de juego
        self.game_frame = Frame(self.root, bg=self.color1, pady=20)
        self.game_frame.place(x=0, y=0, width=800, height=600)

        # Crear un Frame adicional para alinear los botones verticalmente
        buttons_frame = Frame(self.game_frame, bg=self.color1)
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Botones de elección (Piedra, Papel, Tijera)
        Button(
            buttons_frame, text='Piedra', background='#8B4513', foreground='white', width=200, height=50, highlightthickness=0,
            activebackground='#A0522D', activeforeground='white', cursor='hand1', border=0,
            image=self.imag_piedra_option, compound=LEFT, command=lambda: self.play_round("Piedra"), font=('Arial', 15, 'bold')
        ).pack(pady=10)

        Button(
            buttons_frame, text='Papel', background='white', foreground='black', width=200, height=50, highlightthickness=0,
            activebackground='#D3D3D3', activeforeground='black', cursor='hand1', border=0,
            image=self.imag_papel_option, compound=LEFT, command=lambda: self.play_round("Papel"), font=('Arial', 15, 'bold')
        ).pack(pady=10)

        Button(
            buttons_frame, text='Tijera', background='#87CEEB', foreground='black', width=200, height=50, highlightthickness=0,
            activebackground='#00BFFF', activeforeground='black', cursor='hand1', border=0,
            image=self.imag_tijera_option, compound=LEFT, command=lambda: self.play_round("Tijera"), font=('Arial', 15, 'bold')
        ).pack(pady=10)

    def play_round(self, choice):
        """Envía la elección del jugador al servidor y muestra el resultado de la ronda."""
        self.server_socket.sendall(choice.encode())
        response = self.server_socket.recv(1024).decode()

        result_text = "Error al determinar ganador"
        if response.startswith("TIE"):
            result_text = "EMPATE"
        elif response.startswith("WIN"):
            result_text = "VICTORIA"
        elif response.startswith("LOSE"):
            result_text = "DERROTA"

        messagebox.showinfo("Resultado de la Ronda", result_text)

        # Obtener el puntaje y mostrar
        score = response.split()
        self.wins = int(score[3][1])
        self.loses = int(score[5][0])
        score = " ".join(score[1:])
        messagebox.showinfo("Puntaje", f"{score}")

        if self.wins == ROUNDS_TO_WIN:
            messagebox.showinfo("Ganador", "¡HAS GANADO LA PARTIDA!")
            self.server_socket.sendall(b"EXIT")
            self.root.quit()
        elif self.loses == ROUNDS_TO_WIN:
            messagebox.showinfo("Perdedor", "¡HAS PERDIDO LA PARTIDA!")
            self.server_socket.sendall(b"EXIT")
            self.root.quit()
        else:
            self.server_socket.sendall(b"NEXT")

    def clear_screen(self):
        """Elimina todos los widgets de la pantalla."""
        for widget in self.root.winfo_children():
            widget.destroy()


# Ejecución de la interfaz gráfica
if __name__ == "__main__":
    root = Tk()
    app = GameClientApp(root)
    root.mainloop()
