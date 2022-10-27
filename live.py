import cv2, datetime
import numpy as np
import streamlit as st

from camera_input_live import camera_input_live

#Configuración inicial, esconde menu hamburguesa arriba a la derecha y publicidad debajo(footer)
st.set_page_config(page_title='Actualizador del catalogo de libros', page_icon='pb.ico', layout="centered", initial_sidebar_state="collapsed", menu_items=None)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;background-color: #ffffff;}
           footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#Quita el hueco en la parte superior
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)


log= "movimientos.csv"
image = camera_input_live(debounce=500)

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


if image is not None:
    st.image(image)
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    if data:
        st.write(data)
        with st.expander("Detalles"):
            st.write("BBox:", bbox)
            st.write("Codigo QR:", straight_qrcode)
 
        #Se separa información del codigo de barras
        codigo = data.split(' - ')[0]
        nombre = data.split(' - ')[1]
        apellido = data.split(' - ')[2]
        titulo = data.split(' - ')[3]
        ahora = datetime.datetime.now()

        # pide datos sobre el libro
        #with st.form(key="forma"):
        status = st.radio("Seleccione opcion: ", ('nada','Libro nuevo', 'Se presta libro', 'Se devuelve libro'))
        if (status == 'Libro nuevo'):
            estado = 'nuevo'    
            with st.form(key='nuevo'):
                id = st.text_input(label='Identificación de quien lo regala', key="nuevo2").strip()
                submit_button = st.form_submit_button(label='OK')
                if submit_button:
                    st.success("Marcado como nuevo")
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
        if (status == 'Se presta libro'):
            estado = 'prestado'
            with st.form(key='prestado'):
                id = st.text_input(label='Identificación de quien lo pide prestado', key="prestado2").strip()  
                submit_button = st.form_submit_button(label='OK')
                if submit_button:                     
                    st.success("Marcado como prestado")
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
        if (status == 'Se devuelve libro'):
            estado = 'devuelto'
            with st.form(key='devuelto'):
                id = st.text_input(label='Identificación de quien lo pide devuelto', key="devuelto2").strip()  
                submit_button = st.form_submit_button(label='OK')
                if submit_button:                      
                    st.success("Marcado como devuelto")
                    with open(log, 'a',encoding="utf-8-sig") as o:
                        o.write(f'{codigo},{nombre},{apellido},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
        cv2.waitKey(1)