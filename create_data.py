#crear la base de datos
import cv2
import sys, numpy, os
haar_file = 'haarcascade_frontalface_alt.xml'
datos = 'datos' 
sub_data = input('ingrese su nombre: ')
#se guardara en un directorioi con el nombre del usuario y el id de la imagen

path = os.path.join(datos, sub_data)
if not os.path.isdir(path):
    os.mkdir(path)
(width, height) = (130, 100)    # tamaño de la imagen


face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0) #id de la camara que esta conectada

#bucle de 30 capturas de imagen
count = 1
while count < 50:
    #(_, im) = webcam.read()
    ret, im = webcam.read()  
   
    if not ret: continue
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        equ = cv2.equalizeHist(face_resize);
        cv2.imwrite('%s/%s.png' % (path,count), equ)
    count += 1

    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()
