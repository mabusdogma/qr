#!/usr/bin/env python3
import cv2, datetime
from os import system, name

#este programa decodifica nombre a partir del qr usando camara
captura = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
    
def clear(): #borra la consola segun sistema operativo
    #para windows
    if name == 'nt':
        _ = system('cls')
    # para linux y mac
    else:
        _ = system('clear')

def capturaqr(): #mantiene camara encendida y buscando qr
    while True:
        #primero que limpie la consola
        clear()
        _, img = captura.read()
        # detecta y decodifica
        data, vertices_array, _ = detector.detectAndDecode(img)
        # revisa si hay QR en la imagen
        if vertices_array is not None:
            if data:
                print("Libro:     ", data)          
                # pide datos sobre el libro
                opcion = input('Seleccione opcion:\n    1 Libro nuevo\n 2 Se presta libro\n 3 Se devuelve libro\n   4 Cancelar \n\n')
                codigo = data.split(' - ')[0]
                nombre = data.split(' - ')[1]
                apellido = data.split(' - ')[2]
                titulo = data.split(' - ')[3]
                print(codigo,nombre,apellido,titulo)
                ahora = datetime.datetime.now()
                match opcion:
                    case "1":
                        with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},nuevo\n')
                        print('Marcado como nuevo')
                    case "2":
                        with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},prestado\n')
                        print('Marcado como prestado')
                    case "3":
                        with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},devuelto\n')
                        print('Marcado como devuelto')
                    case "4":
                        print('Opción cancelada')
                    case _:
                        print('Error, intente de nuevo')
                        #seleccionar()                         
                    #pregunta si desea escanear otro libro
                otro = input('Desea escanear otro? (s/N) ')
                if otro.lower()!= "s":
                    exit()
                else: #en caso de continuar escaneando, limpia pantalla y va de nuevo
                    clear()

def main(): #parte inicial
    #manda a funcion de captura (limpiando pantalla)
    capturaqr()
    #termina
    captura.release()
    cv2.destroyAllWindows()

if __name__== "__main__" :
    main()



