import importlib
import netifaces
import socket
import os
from threading import Thread
from time import sleep


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


ascii()

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
from DJITelloPy.djitellopy import Tello

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
print("Comandos disponíveis:")
for i, command in enumerate(command_list, 1):
    print(f"{i}. {command}")

# Função para processar os comandos digitados pelo usuário
def process_user_commands():
    while True:
        user_input = input("Digite o número do comando para o drone (ou 'sair' para encerrar): ")
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

# Parar o stream de vídeo
drone.streamoff()

# Desconectar do drone
drone.disconnect()

