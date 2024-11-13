# Piedra, Papel o Tijeras

Este repositorio contiene la implementación de un cliente y servidor para un juego de "Piedra, Papel o Tijeras" usando Python y la librería `tkinter` para la interfaz gráfica del cliente.

## Descripción
El proyecto consiste en un juego de "Piedra, Papel o Tijeras" donde los jugadores pueden crear o unirse a partidas en un entorno cliente-servidor. El cliente se conecta al servidor y permite a los jugadores realizar elecciones que son evaluadas por el servidor para determinar el ganador de cada ronda. El primer jugador en ganar la mayoría de rondas es declarado vencedor.

## Archivos principales
- **interfaz.py**: Archivo que contiene la implementación del cliente con una interfaz gráfica construida con `tkinter`.
- **server.py**: Archivo que contiene la implementación del servidor que gestiona las sesiones de juego y las interacciones entre los jugadores.

## Requisitos

Para ejecutar el proyecto, se necesita:
- Python 3.x
- Librerías:
  - `tkinter` (incluida en Python por defecto)
  - `PIL` (de la librería `Pillow`)

Puedes instalar los requerimientos usando:
```bash
pip install -r requirements.txt
```

## Instrucciones de uso

### Ejecución del Servidor
Para iniciar el servidor, ejecuta el archivo `server.py`:
```bash
python server.py
```
Esto iniciará el servidor en la dirección IP y puerto especificados (por defecto, `0.0.0.0:12345`).

### Ejecución del Cliente
Para iniciar el cliente, ejecuta el archivo `interfaz.py`:
```bash
python interfaz.py
```
Esto abrirá la interfaz gráfica donde podrás:
- Crear una partida.
- Unirte a una partida existente ingresando un código de sesión.

## Estructura del Proyecto

### interfaz.py
El archivo `interfaz.py` incluye:
- Una clase `GameClientApp` que maneja la lógica y la interfaz del cliente.
- Funciones para conectarse al servidor, enviar y recibir datos, y gestionar las diferentes etapas del juego (crear partida, unirse, jugar rondas, mostrar resultados).

### server.py
El archivo `server.py` incluye:
- Una clase `GameServer` que gestiona las conexiones de los clientes y las sesiones de juego.
- Una clase `GameSession` que controla las interacciones entre dos jugadores y determina el resultado de cada ronda.
- Funciones de utilidad para determinar el ganador de cada ronda según las elecciones de los jugadores.
