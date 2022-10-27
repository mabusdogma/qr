#!/usr/bin/env python3
import cv2
from os import system, name, datetime
#este programa decodifica nombre a partir del qr usando camara

log= "movimientos.csv"
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
                # separa los datos del libro
                #codigo + ' - ' + nombre + ' - ' + apellido + ' - ' + titulo
                # pide datos sobre el libro
                opcion = input('Seleccione opcion:\n1 Libro nuevo\n2 Se presta libro\n3 Se devuelve libro\n4 Cancelar')
                ahora = datetime.datetime.now()
                with switch(dia) as s:
                    if s.case(1, True):
                        with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},nuevo\n')
                        print('Marcado como nuevo')    
                    if s.case(2, True):
                        with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},prestado\n')
                        print('Marcado como prestado')
                    if s.case(3, True):
                         with open(log, "a") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},devuelto\n')                   
                        print('Marcado como devuelto')
                    if s.case(4, True):
                        print('Opción cancelada')
                    if s.default():
                        print('Error, intente de nuevo')
                
                
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



