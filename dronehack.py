import tkinter as tk
from PIL import ImageTk, Image
from threading import Thread
from time import sleep
from djitellopy import Tello
import importlib
import netifaces
import socket
import os
import random

def ascii():
    print("""                                      .:-======-:.                                                                    
                                             .=*##+=-:....:-=+*#*-                                                                
                                           .*%=.                .=%*.                                                             
                                          :@+         =+++:        =@:                                                            
                                          =%         @@@@@@-        #=                                                            
                                           #-        =@@@@=       :*               .:------:.                                    
                                            :=:        -@@@@=    :-:           :====-::..::-=+#%#+:                               
                                               .......  +@@@@%:              --.                .=%@+.                            
                                                         @@@@@@#:           :          .-=:        =@@.                           
                                                         #@@@@@@@%+=-------=======++*#@@@@@@        %@=                           
                                                        :%@- *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+       -@%.                           
                                -+++++=======-     .-+#@@@+ +@@@@@**%@@@@@@@@@@@#+-:.            -##-                             
                             =#*-             .-+#@@@@@@@@= @@@@@#: :@@@@@@@@*:    ...    .:--==+-                                
                           .%#       :====+*%@@@@@@@@@@@@@=.@@@@@@@@@@%+=#@@@*         ....                                       
                           :@:      +@@@@@@@@@@@@@@@@@@@@@=.@@@@@@@@%=     +@@.                                                   
                            =#:     :*%@#+:::..   :@@==@@@=.@@@@@@@#@#      =@+                                                   
                              -=-:           .::. @%   *@@--@@@@@@@@@@:.:::: %%                                                   
                                 .::::.......    -@-    -==@@@#- .#@@@@.    .=@:                                                  
                                                 -@:    :+. .      %@@@@+    :@=                                                  
                                                 -@:  :+:    =     =@+@%=    -@=                                                  
                                                 -%.-+:       :--.  @*   . .+@*                                                   
                                                  :+:            .:.#@====#@+.                                                    
                                                                    =@.-%@=                                                       
                                                                    :@@#-                                                         
                                                                     :.                                       """)


# (Controle do Drone)

# Inicializar o drone
drone = Tello()

# Função para capturar o feed de vídeo do drone
def capture_video():
    while True:
        frame = drone.get_frame_read().frame
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        sleep(0.01)

# Funções para controlar o drone
def takeoff():
    drone.takeoff()

def land():
    drone.land()

def move_forward():
    drone.move_forward(50)

def move_backward():
    drone.move_backward(50)

def move_left():
    drone.move_left(50)

def move_right():
    drone.move_right(50)

# Criar janela
window = tk.Tk()

# Criar rótulo para exibir a imagem do vídeo
label = tk.Label(window)
label.pack()

# Criar botões de controle
takeoff_button = tk.Button(window, text="Decolar", command=takeoff)
takeoff_button.pack()

land_button = tk.Button(window, text="Pousar", command=land)
land_button.pack()

forward_button = tk.Button(window, text="Avançar", command=move_forward)
forward_button.pack()

backward_button = tk.Button(window, text="Recuar", command=move_backward)
backward_button.pack()

left_button = tk.Button(window, text="Esquerda", command=move_left)
left_button.pack()

right_button = tk.Button(window, text="Direita", command=move_right)
right_button.pack()

# Iniciar captura de vídeo em uma thread separada
video_thread = Thread(target=capture_video)
video_thread.daemon = True
video_thread.start()

# (Conexão e controle do drone)

# Verifica se a biblioteca djitellopy está instalada
try:
    importlib.import_module('djitellopy')
    print("Biblioteca djitellopy já está instalada.")
except ImportError:
    print("Biblioteca djitellopy não encontrada. Baixando do repositório...")
    try:
        os.system("git clone https://github.com/damiafuentes/DJITelloPy.git")
        print("Biblioteca djitellopy baixada com sucesso.")
    except Exception as e:
        print("Ocorreu um erro durante o download da biblioteca djitellopy:")
        print(str(e))
        exit()

# Importa a biblioteca djitellopy
from djitellopy import Tello

# Obtém o endereço IP da interface de rede
def get_local_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != 'lo':
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ipv4_addresses = addresses[netifaces.AF_INET]
                if len(ipv4_addresses) > 0:
                    return ipv4_addresses[0]['addr']
    return None

# Lista os IPs disponíveis na rede local
def list_available_ips():
    local_ip = get_local_ip()
    if local_ip:
        prefix = ".".join(local_ip.split(".")[:-1])
        available_ips = []
        for i in range(1, 255):
            ip = f"{prefix}.{i}"
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, 8889))  # Porta do protocolo Tello
            if result == 0:
                available_ips.append(ip)
            sock.close()
        return available_ips
    return []

# Lista os IPs disponíveis e permite selecionar o IP do drone
def choose_drone_ip():
    ips = list_available_ips()
    if ips:
        print("IPs disponíveis:")
        for i, ip in enumerate(ips):
            print(f"{i+1}. {ip}")

        while True:
            try:
                choice = int(input("Selecione o número do IP do drone: "))
                if 1 <= choice <= len(ips):
                    return ips[choice - 1]
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    else:
        print("Nenhum IP de drone encontrado.")
        return None

# Função para obter a porta para conexão
def get_drone_port():
    default_port = 8889
    user_input = input(f"Digite a porta do drone (padrão {default_port}) ou deixe em branco para descoberta automática: ")
    if user_input == "":
        return default_port
    try:
        port = int(user_input)
        return port
    except ValueError:
        print("Entrada inválida. Usando a porta padrão.")
        return default_port

# Função para receber os dados do estado do drone
def state_handler(event, sender, data):
    print(f"[Estado do Drone] {data}")

# Função para receber os dados de vídeo do drone
def video_handler(event, sender, data):
    # Processar o feed de vídeo aqui
    pass

# Função para enviar comandos ao drone
def send_command(command):
    drone.send_command(command)

# Função para tirar uma foto e salvá-la em arquivo local
photo_counter = 1  # Contador para nomear as imagens capturadas

def take_photo():
    global photo_counter  # Acessar a variável global do contador

    photo = drone.take_picture()
    photo_path = f"photo{photo_counter}.jpg"  # Nome do arquivo único
    photo.save(photo_path)
    print(f"Foto tirada e salva em '{photo_path}'")

    photo_counter += 1  # Incrementar o contador para a próxima imagem

recording = False  # Variável para controlar o estado da gravação
video_counter = 1  # Contador para nomear os vídeos gravados

# Função para iniciar a gravação de vídeo
def start_recording():
    global recording, video_counter  # Acessar as variáveis globais

    if not recording:
        video_path = f"video{video_counter}.mp4"  # Nome do arquivo único
        drone.start_video_recording(video_path)
        print(f"Iniciando gravação em '{video_path}'")
        recording = True

# Função para parar a gravação de vídeo
def stop_recording():
    global recording, video_counter  # Acessar as variáveis globais

    if recording:
        drone.stop_video_recording()
        print("Gravação encerrada")
        recording = False
        video_counter += 1  # Incrementar o contador para o próximo vídeo

# Desconectar o drone
def disconnect_drone(drone):
    drone.disconnect()

# Desconectar todos os drones
def disconnect_all_drones(drones):
    for drone in drones:
        drone.disconnect()

# Conectar ao drone
drone_ip = choose_drone_ip()
drone_port = get_drone_port()
drone = Tello(drone_ip, drone_port)
drone.connect()

# Configurar manipuladores de eventos
drone.subscribe(drone.EVENT_FLIGHT_DATA, state_handler)
drone.subscribe(drone.EVENT_VIDEO_FRAME, video_handler)

# Iniciar stream de vídeo
drone.streamon()

# Menu de controle ou derrubada
while True:
    ascii()
    print("\n1. Controlar o drone")
    print("2. Derrubar um drone")
    print("3. Derrubar todos os drones")
    print("0. Sair\n")

    choice = input("Digite o número da opção desejada: ")

    if choice == "1":
        # Lista de comandos disponíveis
        command_list = [
            "takeoff",
            "land",
            "up {distance}",
            "down {distance}",
            "left {distance}",
            "right {distance}",
            "forward {distance}",
            "back {distance}",
            "flip {direction}",
            "cw {angle}",
            "ccw {angle}",
            "battery?",
            "capture",
            "record {time}"
        ]

        # Imprimir a lista de comandos disponíveis
        print("\nComandos disponíveis:")
        for i, command in enumerate(command_list, 1):
            print(f"{i}. {command}")

        # Função para processar os comandos digitados pelo usuário
        def process_user_commands():
            while True:
                user_input = input("\nDigite o número do comando para o drone (ou 'sair' para encerrar): ")
                if user_input.lower() == "sair":
                    break
                try:
                    command_index = int(user_input) - 1
                    if 0 <= command_index < len(command_list):
                        command = command_list[command_index]
                        if "{distance}" in command or "{angle}" in command:
                            value = input("Digite a distância ou ângulo: ")
                            command = command.replace("{distance}", value).replace("{angle}", value)
                        send_command(command)
                    else:
                        print("Comando inválido. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Digite um número ou 'sair' para encerrar.")

        # Iniciar o processamento de comandos do usuário em uma thread separada
        thread = Thread(target=process_user_commands)
        thread.start()

        # Aguardar o encerramento da thread de processamento de comandos
        thread.join()

    elif choice == "2":
        drone_ip = input("Digite o IP do drone que deseja derrubar: ")
        drone_port = get_drone_port()
        drone_to_drop = Tello(drone_ip, drone_port)
        drone_to_drop.connect()
        drone_to_drop.land()
        disconnect_drone(drone_to_drop)
        print("Drone derrubado.")

    elif choice == "3":
        available_ips = list_available_ips()
        if available_ips:
            for ip in available_ips:
                drone_to_drop = Tello(ip, get_drone_port())
                drone_to_drop.connect()
                drone_to_drop.land()
                disconnect_drone(drone_to_drop)
            print("Todos os drones foram derrubados.")
        else:
            print("Nenhum drone encontrado.")

    elif choice == "0":
        disconnect_all_drones([drone])
        print("Programa encerrado.")
        break

    else:
        print("Escolha inválida. Tente novamente.")
