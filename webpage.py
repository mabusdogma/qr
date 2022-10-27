#!/usr/bin/env python3
import streamlit as st
import cv2, datetime

st.title("Biblioteca")
st.write("Actualizador del catalogo de libros")
log= "movimientos.csv"
captura = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
    
def capturaqr(): #mantiene camara encendida y buscando qr
    while True:
        _, img = captura.read()
        # detecta y decodifica
        data, vertices_array, _ = detector.detectAndDecode(img)
        # revisa si hay QR en la imagen
        if vertices_array is not None:
            if data:
                st.write("Libro:\n", data)

                #Se separa información del codigo de barras
                codigo = data.split(' - ')[0]
                nombre = data.split(' - ')[1]
                apellido = data.split(' - ')[2]
                titulo = data.split(' - ')[3]
                ahora = datetime.datetime.now()
                
                # pide datos sobre el libro
                status = st.radio("Seleccione opcion: ", ('Libro nuevo', 'Se presta libro', 'Se devuelve libro'))
                if (status == 'Libro nuevo'):
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},nuevo,tarjeta\n')
                    st.success("Marcado como nuevo")
                if (status == 'Se presta libro'):
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},prestado,tarjeta\n')
                    st.success("Marcado como prestado")
                if (status == 'Se devuelve libro'):
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},devuelto,tarjeta\n')
                    st.success("Marcado como devuelto")
                #pregunta si desea escanear otro libro
                otro = st.checkbox("No mas libros", False, help="Permite escanear un nuevo codigo de barras")
                if otro:
                    break
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




