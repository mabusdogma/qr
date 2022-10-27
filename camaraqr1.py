#!/usr/bin/env python3
import cv2
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
                otro = input('Seleccione opcion:\n1 Libro nuevo\n2 Se presta libro\n3 Se regresa libro\n4 Cancelar')
                
                #pregunta si desea escanear otro libro
                otro = input('Desea escanear otro? (s/N) ')
                if otro.lower()!= "s":
                    break
            else: #en caso de continuar escaneando, limpia pantalla y va de nuevo
                clear()
        # muestra resultado
        cv2.imshow("QR", img)
        # presione q para salir
        if cv2.waitKey(1) == ord("q"):
            break

def main(): #parte inicial
    #manda a funcion de captura (limpiando pantalla)
    capturaqr()
    #termina
    captura.release()
    cv2.destroyAllWindows()

if __name__== "__main__" :
    main()



