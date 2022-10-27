#!/usr/bin/env python3
import qrcode, openpyxl, warnings

#este programa crea los codigos qr basandose en 
#un archivo de excel, del cual extrae datos de
#columnas de A a D, y le pone el nombre de la columna A

#url =  'https://docs.google.com/spreadsheets/d/e/2PACX-1vQX6DR9Q3xJSvQtDlbuZJVQ-nODyIR1R8mB6DafWF8gcR-T1QzqeqgnpmjNftF3S_4Tgv30qnGPMtk2/pub?gid=0&single=true&output=xlsx'

catalogo ='Polish library - KSIAZKI.xlsx'
wb = openpyxl.load_workbook(catalogo)
sheet = wb.active
filas =sheet.max_row

for fila in range(filas-1):
    codigo = sheet["A"+str(fila+2)].value
    if codigo is None:
        continue
    nombre = sheet["B"+str(fila+2)].value
    if nombre is None:
        nombre = ''
    apellido = sheet["C"+str(fila+2)].value
    if apellido is None:
        apellido = ''
    titulo = sheet["D"+str(fila+2)].value
    if titulo is None:
        titulo = ''
    libro = codigo + ' - ' + nombre + ' - ' + apellido + ' - ' + titulo
    QRCodefile = codigo.strip()+".png"
    QRimage = qrcode.make(libro)
    QRimage.save(QRCodefile)
    print (libro)

print('listo')

