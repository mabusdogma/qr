#!/usr/bin/env python3

import cv2
#este programa decodifica nombre a partir del qr


libro = "foto2.jpeg"
# lee imagen del codigo QR
image = cv2.imread(libro)
detector = cv2.QRCodeDetector()
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
#si hay codigo QR, imprime datos
if vertices_array is not None:
  print("Datos del libro:")
  print(data)
else:
  print("Error al leer los datos del código QR")