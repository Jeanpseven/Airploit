
# Airploit
                                                  .:-======-:.                                                                    
                                             .=*##+=-:....:-=+*#*-                                                                
                                           .*%=.                .=%*.                                                             
                                          :@+         =+++:        =@:                                                            
                                          =%         @@@@@@-        #=                                                            
                                           #-        =@@@@@+       :*               .:------:.                                    
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
                                 .::::.......    -@-    -==@@@#- .#@@@@.    .=@:           **Airploit - Controle Absoluto dos Céus**                                     
                                                 -@:    :+. .      %@@@@+    :@=                                                  
                                                 -@:  :+:    =     =@+@%=    -@=                                                  
                                                 -%.-+:       :--.  @*   . .+@*                                                   
                                                  :+:            .:.#@====#@+.                                                    
                                                                    =@.-%@=                                                       
                                                                    :@@#-                                                         
                                                                     :.                                       
script que hackeia drones usando biblioteca Tello


Domine os céus e assuma o controle total do seu drone com o poderoso script Airploit. Desenvolvido para entusiastas de drones que desejam explorar todo o potencial de suas aeronaves, o Airploit oferece uma interface avançada e intuitiva para controlar e comandar seu drone com facilidade e precisão.

Recursos do Airploit:

Descoberta Automática de Dispositivos: O script permite detectar automaticamente os drones disponíveis na rede local, facilitando a conexão com o seu drone sem esforço.

Seleção Personalizada de Dispositivos: Apresenta uma lista de drones disponíveis, permitindo que você escolha o drone específico com o qual deseja se conectar e controlar.

Comandos Avançados: O Airploit oferece uma ampla gama de comandos para controlar seu drone. Desde comandos básicos de decolagem e pouso até manobras avançadas, como voar para cima, para baixo, para os lados, fazer flips e giros no ar.

Controle de Voo Preciso: Com o Airploit, você pode enviar comandos de voo precisos para seu drone, permitindo que você o posicione exatamente onde deseja no espaço tridimensional.

Feedback de Estado do Drone: Receba informações em tempo real sobre o estado do drone, como a duração da bateria, altitude, velocidade, temperatura e muito mais. Tenha total conhecimento do seu drone durante o voo.

Lista de Comandos Disponíveis:

takeoff: Decolar o drone.

land: Pousar o drone.

up {distância}: Mover o drone para cima a uma distância específica.

down {distância}: Mover o drone para baixo a uma distância específica.

left {distância}: Mover o drone para a esquerda a uma distância específica.

right {distância}: Mover o drone para a direita a uma distância específica.

forward {distância}: Mover o drone para frente a uma distância específica.

back {distância}: Mover o drone para trás a uma distância específica.

flip {direção}: Realizar um flip na direção especificada.

cw {ângulo}: Girar o drone no sentido horário por um ângulo específico.

ccw {ângulo}: Girar o drone no sentido anti-horário por um ângulo específico.

battery?: Obter o nível atual da bateria do drone.

Exemplos de Comandos:

Digite "takeoff" para decolar o drone.
Use o comando "up 1" para mover o drone para cima em 1 metro.
Experimente "flip front" para realizar um flip para a frente.
Envie o comando "ccw 90" para girar o drone 90 graus no sentido anti-horário.
Digite "battery?" para verificar o nível atual da bateria do drone.

![camera](img.jpg)

Os comandos "record" e "capture" são usados para gravar vídeos e capturar fotos, respectivamente, utilizando o drone Tello.

Comando "record":

Sintaxe: record {time}
Descrição: Este comando instrui o drone a começar a gravar um vídeo com a duração especificada em segundos.
Exemplo: Para gravar um vídeo de 10 segundos, você pode digitar record 10.
Comando "capture":

Sintaxe: capture
Descrição: Este comando instrui o drone a capturar uma foto.
Exemplo: Digite capture para capturar uma foto com o drone.
No script atualizado, você pode selecionar esses comandos digitando o número correspondente na lista de comandos disponíveis. Por exemplo, se "record" estiver na posição 13 e "capture" na posição 14, você pode digitar 13 para gravar um vídeo ou 14 para capturar uma foto.

Certifique-se de que o drone Tello esteja conectado e pronto para receber os comandos antes de executar os comandos de gravação de vídeo ou captura de foto.

# Script de Controle de Drone

Este é um script Python que utiliza a biblioteca djitellopy para controlar um drone DJI Tello. Ele oferece as seguintes funcionalidades:

Decolar o drone
Pousar o drone
Mover o drone para frente
Mover o drone para trás
Mover o drone para a esquerda
Mover o drone para a direita
Capturar o feed de vídeo do drone
Exibir o feed de vídeo em uma janela usando tkinter
Controlar o drone usando botões interativos na interface
Iniciar a captura de vídeo em uma thread separada
Receber e exibir os dados do estado do drone (bateria, altitude, velocidade, etc.)
Receber e exibir os dados de vídeo do drone
Requisitos
Python 3.7 ou superior
Biblioteca djitellopy
Biblioteca tkinter
Biblioteca PIL (Pillow)
Biblioteca threading
Biblioteca time
Configuração
Certifique-se de ter todas as bibliotecas necessárias instaladas.
Conecte o drone DJI Tello à rede Wi-Fi correta.
Execute o script drone_control.py.
Utilização
Execute o script e aguarde até que a interface do drone seja exibida.
Clique nos botões para controlar o drone: decolar, pousar, mover para frente, mover para trás, mover para a esquerda, mover para a direita.
O feed de vídeo do drone será exibido na janela.
O estado atual do drone, como a bateria, altitude e velocidade, será exibido na interface.


O script é um programa em Python que permite o controle de um drone Tello usando a biblioteca djitellopy. Ele oferece uma interface gráfica simples para decolar, pousar e controlar o drone em diferentes direções (para frente, para trás, para a esquerda e para a direita). Além disso, o script oferece funcionalidades adicionais, como captura de vídeo em tempo real, captura de fotos e gravação de vídeos.

O código começa verificando se as bibliotecas necessárias, como Pillow, djitellopy, netifaces e xvfbwrapper, estão instaladas no sistema. Se alguma biblioteca estiver faltando, o script tentará instalá-la usando o comando pip install. Em seguida, o código define funções para controlar o drone, como decolar, pousar e mover-se em diferentes direções.

A interface gráfica é criada usando a biblioteca tkinter. Ela exibe um rótulo para o feed de vídeo do drone e botões para as diferentes ações de controle. O feed de vídeo é obtido em uma thread separada e atualizado continuamente na interface.

O script também inclui funcionalidades para conexão e comunicação com o drone. Ele lista os IPs disponíveis na rede local e permite que o usuário selecione o IP do drone a ser controlado. Além disso, o script oferece a opção de derrubar um drone específico ou todos os drones disponíveis na rede.

É importante destacar que o script requer a presença física de um drone Tello e uma conexão Wi-Fi para que funcione corretamente. Certifique-se de ter as permissões necessárias para controlar o drone e tome todas as precauções de segurança ao utilizá-lo.
