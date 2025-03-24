import tkinter as tk
from PIL import ImageTk, Image
from threading import Thread
from time import sleep
import subprocess
import importlib
import netifaces
import socket
import os
from djitellopy import Tello
import cv2

def ascii():
    print("""                                      .:-======-:.
                                             .=*##+=-:....:-=+*#*-                 
                                           .*%=.                .=%*.
                                          :@+         =+++:        =@:
                                          =%         @@@@@@-        #=
                                           #-        =@@@@=       :*               .:------:.
                                            :=:        -@@@@=    :-:           :====-::..::-=+#%#+:
                                               .......  +@@@@=              --.                .=%@+.
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
                                                                     :.            
    """)

# Instalar as bibliotecas necessárias
def install_libraries():
    libraries = ["Pillow", "djitellopy", "netifaces", "opencv-python"]
    for library in libraries:
        try:
            importlib.import_module(library)
            print(f"A biblioteca {library} já está instalada.")
        except ImportError:
            print(f"A biblioteca {library} não foi encontrada. Instalando...")
            try:
                subprocess.check_call(["pip", "install", library])
                print(f"A biblioteca {library} foi instalada com sucesso.")
            except Exception as e:
                print(f"Ocorreu um erro durante a instalação da biblioteca {library}: {str(e)}")

# Função para obter o IP local da máquina
def get_local_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue  # Ignorar a interface de loopback
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ip_info = addresses[netifaces.AF_INET][0]
            return ip_info['addr']
    return None

# Função para listar IPs disponíveis na rede local
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

# Função para escolher um IP de drone da lista enumerada
def choose_drone_ip():
    ips = list_available_ips()
    if ips:
        print("IPs disponíveis:")
        for i, ip in enumerate(ips, 1):
            print(f"{i}. {ip}")

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

# Conectar ao drone
def connect_to_drone(drone_ip, drone_port):
    try:
        drone = Tello(drone_ip, drone_port)
        drone.connect()
        drone.streamon()
        ascii()
        print(f"Conectado ao drone com IP {drone_ip} na porta {drone_port}.")
        return drone
    except Exception as e:
        print(f"Ocorreu um erro ao conectar ao drone: {str(e)}")
        return None

# Função para desconectar o drone
def disconnect_drone(drone):
    drone.land()
    drone.streamoff()
    drone.end()
    print("Desconectado do drone.")

# Capturar o feed de vídeo do drone
def capture_video(drone, label, root):
    frame = drone.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
    label.config(image=photo)
    label.image = photo
    root.after(20, capture_video, drone, label, root)  # Atualiza o vídeo a cada 20ms

# Função para exibir a interface gráfica
def display_interface(drone):
    root = tk.Tk()
    root.title("Controle do Drone")
    root.geometry("800x600")

    label = tk.Label(root)
    label.pack()

    takeoff_button = tk.Button(root, text="Decolar", command=drone.takeoff)
    takeoff_button.pack()

    land_button = tk.Button(root, text="Pousar", command=drone.land)
    land_button.pack()

    forward_button = tk.Button(root, text="Avançar", command=lambda: drone.move_forward(20))
    forward_button.pack()

    backward_button = tk.Button(root, text="Recuar", command=lambda: drone.move_back(20))
    backward_button.pack()

    left_button = tk.Button(root, text="Esquerda", command=lambda: drone.move_left(20))
    left_button.pack()

    right_button = tk.Button(root, text="Direita", command=lambda: drone.move_right(20))
    right_button.pack()

    cw_button = tk.Button(root, text="Girar Direita", command=lambda: drone.rotate_clockwise(90))
    cw_button.pack()

    ccw_button = tk.Button(root, text="Girar Esquerda", command=lambda: drone.rotate_counter_clockwise(90))
    ccw_button.pack()

    root.after(20, capture_video, drone, label, root)  # Iniciar a captura de vídeo
    root.mainloop()

# Função principal
def main():
    install_libraries()
    drone_ip = choose_drone_ip()
    drone_port = 8889
    drone = connect_to_drone(drone_ip, drone_port)

    if drone is not None:
        display_interface(drone)
        disconnect_drone(drone)
    else:
        print("Não foi possível conectar ao drone. Verifique a conexão e tente novamente.")

if __name__ == "__main__":
    main()
