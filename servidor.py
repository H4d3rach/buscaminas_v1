import socket
import random
import time 
HOST = "localhost"  # Direccion ip del host (En este caso la wifi)
PORT = 65432  # Puerto al que se conectará el cliente
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket: #Se crea un socket TCP(Familia de direcciones en este caso ipv4, sock_stream es tcp)
    TCPServerSocket.bind((HOST, PORT)) #Vincula la direccion ip y el puerto al socket
    TCPServerSocket.listen() #El servidor se pone en modo escucha para las solicitudes de tipo tcp
    print("El servidor para el juego del Buscaminas está disponible para partidas:")

    Client_conn, Client_addr = TCPServerSocket.accept() #()Nuevo objeto que se puede usar para enviar y recibir datos ()Direcion vinculada al cliente
    with Client_conn:
        inicio = time.time()
        print("Usuario conectado: ", Client_addr)
        print("Esperando dificultad")
        dificultad = Client_conn.recv(buffer_size) #Se recibe la dificultad
        dificultad = dificultad.lower() #Como la dificultad es una cadena, se convierten a minúsculas para las condiciones siguientes
        if dificultad==b'principiante': #Condiciones para crear el tablero
            print("Eligio principiante")
            n = 9 #Longitud del tablero
            m = 10 #Minas a poner
            Client_conn.sendall(str(n).encode('utf-8')) #Servidor envía la longitud del tablero al cliente
        elif dificultad==b'avanzado':
            print("Eligio avanzado")
            n = 16
            m = 40
            Client_conn.sendall(str(n).encode('utf-8'))
        elif dificultad==b'prueba' : #Tablero para pruebas, mas pequeño
            print("Entro a la prueba")
            n = 3
            m = 4
            Client_conn.sendall(str(n).encode('utf-8'))
        print("Creando tablero...")
        def mostrarTablero(tablero): #Funcion para mostrar el tablero
            for filaT in tablero:
                for v in filaT:
                    print(v, end=" ")
                print()
        tablero = [] #Se empieza a crear el tablero
        for i in range(n):
            tablero.append([])
            for j in range(n):
                tablero[i].append(0) #Se rellena con 0's
        print("Poniendo minas...")
        i = 1
        while i <= m: #Se ponen las minas
            rand1 = random.randint(0,n-1) #Se crean posciciones de manera aleatoria
            rand2 = random.randint(0,n-1)
            if tablero[rand1][rand2] == 0: #Se pueden repetir, por lo que debemos confirmar que la casilla esté vacía
                tablero[rand1][rand2] = 1
            else :
                minascontrolador = 1
                while minascontrolador: #En caso de repetirse, iterar hasta obtener una casilla vacía
                    rand1 = random.randint(0,n-1)
                    rand2 = random.randint(0,n-1)
                    if tablero[rand1][rand2] == 1:
                        minascontrolador = 1
                    else:
                        tablero[rand1][rand2] = 1
                        minascontrolador = 0
            i = i + 1
        mostrarTablero(tablero) #Se usa para mostrar el tablero 0's son casillas vacias y 1's son las minas
        contador_jugadas = 0 #Se utiliza para contar las casillas que son acertadas por el usuario
        controlador = 1
        while controlador : #Ciclo del juevo
            coordenadas = Client_conn.recv(buffer_size) #Se reciben las coordenadas del cliente en formato (**,**)
            print(coordenadas) 
            filas = int(coordenadas[1:3])-1 
            print(filas)
            columnas = int(coordenadas[4:6])-1
            print(columnas)
            if filas >= n or columnas >= n: #Excepcion fuera de rango
                print("Fuera de rango")
                Client_conn.sendall(b'3') #Se envia respuesta al cliente de código 3
                print("Tablero actual")
                mostrarTablero(tablero)  
            else:
                condicion = tablero[filas][columnas] 
                if condicion != 1:  #Se verifica que la casilla no tenga minas
                    print("Casilla válida")
                    tablero[filas][columnas] = 2 #Se coloca la jugada en la casilla
                    contador_jugadas = contador_jugadas + 1 #Se incrementa el contador de las jugadas
                    condicion_gane = (n*n)-m #Se necesita cumplir la condicion para ganar
                    if contador_jugadas == condicion_gane:  #Se verifica el número de jugadas
                        Client_conn.sendall(b'1')   #Si gana, se envía el código 1 al usuario
                        controlador = 0 #En caso de ganar se sale del ciclo del juego y acaba
                    Client_conn.sendall(b'2') #En dado caso de que todavía no gane se sigue en el juego y se envia el codigo 2
                elif condicion == 1: #Condicion para cuando se encuentra una mina
                    print("Se ha encontrado una mina")
                    Client_conn.sendall(b'4') #Se envía el codigo 4 para el usuario
                    controlador = 0 #Se sale del ciclo del juego
                print("Tablero actual")
                mostrarTablero(tablero)   
        time.sleep(1)
        fin = time.time()
        tiempotranscurrido = fin - inicio
        print("El tiempo desde que se conectó el usuario fue: ",tiempotranscurrido," segundos") 
