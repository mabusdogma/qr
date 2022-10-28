import cv2, datetime,qrcode, csv
import numpy as np
import streamlit as st

#Configuración inicial, esconde menu hamburguesa arriba a la derecha y publicidad debajo(footer)
st.set_page_config(page_title='Actualizador del catalogo de libros', page_icon='qr.ico', layout="centered", initial_sidebar_state="collapsed", menu_items=None)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;background-color: #ffffff;}
           footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
#Quita el hueco en la parte superior
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
#esconde el primer radio button
st.markdown(""" <style>div[role="radiogroup"] >  :first-child{display: none !important;}</style>""",unsafe_allow_html=True)
  
 # -------------
  
#crea la camara  
image = st.camera_input("QR",label_visibility="collapsed")

#comienza video para buscar QR
if image is not None:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    #hace las columnas
    col1, col2, col3 = st.columns([2, 2, 1])

    if data:
        st.session_state["found_qr"] = True
        st.session_state["qr_code_image"] = image
        with col2.expander(data):
            #st.write("BBox:", bbox)
            #st.write("Codigo QR:", straight_qrcode)
            QRfile = "tempqr.png"
            QRimage = qrcode.make(data)
            QRimage.save(QRfile)
            st.image(QRfile)
            log= "movimientos.csv"
        #Se separa información del codigo de barras
        if re.search(r" - ", data):
            codigo = data.split(' - ')[0]
            nombre = data.split(' - ')[1]
            apellido = data.split(' - ')[2]
            titulo = data.split(' - ')[3]
            ahora = datetime.datetime.now()
        else:
            codigo = data
        # pide datos sobre el libro
        #with st.form(key="forma"):
        with col1:
            status = st.radio("Seleccione opción: ", ('nada','Libro nuevo', 'Se presta libro', 'Se devuelve libro'))
            if (status == 'Libro nuevo'):
                estado = 'nuevo'    
                with st.form(key='nuevo'):
                    id = st.text_input(label='Identificación de quien lo regala', key="nuevo2").strip()
                    submit_button = st.form_submit_button(label='OK')
                    if submit_button:
                        st.success("Libro nuevo!")
                        with open(log, 'a',encoding='utf-8-sig') as o:
                            o.write(f'{codigo},{apellido},{nombre},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
            if (status == 'Se presta libro'):
                estado = 'prestado'
                with st.form(key='prestado'):
                    id = st.text_input(label='Identificación de quien lo pide prestado', key="prestado2").strip()  
                    submit_button = st.form_submit_button(label='OK')
                    if submit_button:                     
                        st.success("Prestado!")
                        with open(log, 'a',encoding='utf-8-sig') as o:
                            o.write(f'{codigo},{apellido},{nombre},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
            if (status == 'Se devuelve libro'):
                estado = 'devuelto'
                with st.form(key='devuelto'):
                    id = st.text_input(label='Identificación de quien lo pide devuelto', key="devuelto2").strip()  
                    submit_button = st.form_submit_button(label='OK')
                    if submit_button:                      
                        st.success("Devuelto!")
                        with open(log, 'a',encoding='utf-8-sig') as o:
                            o.write(f'{codigo},{apellido},{nombre},{titulo},{ahora.strftime("%d/%m/%Y")},{ahora.strftime("%H:%M")},{estado},{id}\n') 
    
        #donde se guardan los cambios en los libros
        with open(log, "rb") as file:
            col3.download_button(
            label="Descarga CSV",
            data=file,
            file_name=log,
            mime="text/csv")