import socket
import time 

#HOST = input("Ingrese la ip del host: ")
#PORT = int(input("Ingrese el puerto de salida: "))
HOST = "localhost"
PORT = 65432
buffer_size = 1024
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    inicio = time.time()
    print("**************Bienvenido al jugo del Buscaminas******************")
    dificultad_i = input("Ingrese la dificultad (Ej. Principiante / Avanzado): ")
    TCPClientSocket.sendall(dificultad_i.encode('utf-8'))
    print("Esperando al servidor")

    confirmacion = TCPClientSocket.recv(buffer_size)
    if confirmacion :
        print("Partida confirmada en breve se aparecerá el tablero")
        n = int(confirmacion)
    elif not confirmacion:
        print("Su partida no se pudo crear")
    print("**************Buscaminas*****************")
    tablero = []
    for i in range(n):
        tablero.append([])
        for j in range(n):
            tablero[i].append('-')
    def mostrarTablero(tablero):
        filas = 0
        columnas = 0
        counter1 = 1
        counter2 = 1
        while filas <= n :
            columnas = 0
            while columnas <= n :
                if filas == 0 and columnas == 0:
                    print(" ", end=" ")
                elif filas == 0 and columnas !=0:
                    print(str(counter1).zfill(2), end=" ")
                    counter1 = counter1 + 1
                elif filas != 0 and columnas ==0:
                    print(str(counter2).zfill(2), end=" ")
                    counter2 = counter2 + 1
                elif filas !=0 and columnas != 0 :
                    print(tablero[filas-1][columnas-1],end=" ")
                columnas = columnas + 1
            print("")
            filas = filas + 1
    mostrarTablero(tablero)        
    controlador = 1
    while controlador:
        tiro=input("Ingrese la coordenada de su tiro Ej((**,**)): ")
        TCPClientSocket.sendall(tiro.encode('utf-8'))
        resp_server = int(TCPClientSocket.recv(buffer_size))
        if resp_server == 4:
            print("Chispas encontraste una mina ")
            tablero[int(tiro[1:3])-1][int(tiro[4:6])-1] = '*'
            mostrarTablero(tablero)
            controlador=0
        elif resp_server == 1:
            print("Felicidades has ganado el juego :) ")
            tablero[int(tiro[1:3])-1][int(tiro[4:6])-1]='X'
            i = 0
            while i < n:
                j = 0
                while j < n:
                    if tablero[i][j]=='-':
                        tablero[i][j]='*'
                    j = j +1
                i = i + 1        
            mostrarTablero(tablero)
            controlador=0
        elif resp_server == 2:
            tablero[int(tiro[1:3])-1][int(tiro[4:6])-1]='X'
            mostrarTablero(tablero)
        elif resp_server == 3:
            print("La casilla está fuera de rango ")
            mostrarTablero(tablero)
    time.sleep(1)
    fin = time.time()
    tiempotranscurrido = fin - inicio
    print("El tiempo desde que se conectó al servidor fue: ",tiempotranscurrido," segundos") 
            