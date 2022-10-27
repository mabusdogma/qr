#!/usr/bin/env python3
import streamlit as st
import cv2, datetime
from streamlit_webrtc import webrtc_streamer



st.title("Biblioteca")
st.write("Actualizador del catalogo de libros")
log= "movimientos.csv"



#esconde el primer radio button
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)


def capturaqr(): #mantiene camara encendida y buscando qr


    if run:
        detector = cv2.QRCodeDetector()
        ctx = cv2.VideoCapture(0)
        img_display = st.empty()
        _, img = ctx.read()
        img_display.image(img, channels='BGR')
        # detecta y decodifica
        data, vertices_array, _ = detector.detectAndDecode(img)
        # revisa si hay QR en la imagen
        if vertices_array is not None:
            if data:
                st.write("Libro:\n", data)
                estado = ''
                #Se separa información del codigo de barras
                codigo = data.split(' - ')[0]
                nombre = data.split(' - ')[1]
                apellido = data.split(' - ')[2]
                titulo = data.split(' - ')[3]
                ahora = datetime.datetime.now()
                
                # pide datos sobre el libro
                with st.form(key="forma"):
                    status = st.radio("Seleccione opcion: ", ('nada','Libro nuevo', 'Se presta libro', 'Se devuelve libro'))
                    if (status == 'Libro nuevo'):
                        estado = 'nuevo'    
                        with st.form(key='nuevo'):
                            nuevo = st.text_input(label='Identificación de quien lo regala', key="nuevo2")
                            submit_button = st.form_submit_button(label='OK')
                            nuevo = nuevo.strip()
                        st.success("Marcado como nuevo")
                    if (status == 'Se presta libro'):
                        estado = 'prestado'
                        with st.form(key='prestado'):
                            prestado = st.text_input(label='Identificación de quien lo pide prestado', key="prestado2")
                            submit_button = st.form_submit_button(label='OK')
                            prestado = prestado.strip()                       
                        st.success("Marcado como prestado")
                    if (status == 'Se devuelve libro'):
                        estado = 'devuelto'
                        with st.form(key='devuelto'):
                            devuelto = st.text_input(label='Identificación de quien lo pide devuelto', key="devuelto2")
                            submit_button = st.form_submit_button(label='OK')
                            devuelto = devuelto.strip()                        
                        st.success("Marcado como devuelto")
                    submit_button = st.form_submit_button(label="Confirmar")     
                #pregunta si desea escanear otro libro
                otro = st.checkbox("No mas libros", False, help="Permite escanear un nuevo codigo de barras")

                with open(log, 'a',encoding="utf-8-sig") as o:
                    o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},tarjeta\n')                   
        # muestra resultado
        cv2.imshow("QR", img)
        # presione q para salir


def main(): #parte inicial
    #manda a funcion de captura (limpiando pantalla)
    capturaqr()
    #termina
    ctx.release()
    cv2.destroyAllWindows()

if __name__== "__main__" :
    main()




