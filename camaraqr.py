#!/usr/bin/env python3
import cv2, datetime
from os import system, name

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
                print("Libro:\n", data)
                # pide datos sobre el libro
                otro = input('\nSeleccione opcion:\n    1 Libro nuevo\n    2 Se presta libro\n    3 Se regresa libro\n    4 Cancelar\n')
                codigo = data.split(' - ')[0]
                nombre = data.split(' - ')[1]
                apellido = data.split(' - ')[2]
                titulo = data.split(' - ')[3]
                #print(codigo,nombre,apellido,titulo)
                ahora = datetime.datetime.now()
                match otro:
                    case "1":
                        tarjeta = input('\nIdentificación de quien lo regala\n')
                        with open(log, 'a',encoding="utf-8-sig") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},nuevo,tarjeta\n')
                        print('Marcado como nuevo\n')
                    case "2":
                        tarjeta = input('Identificación de quien lo pide\n')
                        with open(log, 'a',encoding="utf-8-sig") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},prestado,tarjeta\n')
                        print('Marcado como prestado\n')
                    case "3":
                        tarjeta = input('Identificación de quien lo devuelve\n')
                        with open(log, 'a',encoding="utf-8-sig") as o:
                            o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},devuelto,tarjeta\n')
                        print('Marcado como devuelto\n')
                    case "4":
                        print('Opción cancelada')
                    case _:
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



