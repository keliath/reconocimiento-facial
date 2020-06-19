import cv2, sys, numpy, os, serial, time, correo
import tkinter.messagebox
size = 4
recog = True
haar_file = 'haarcascade_frontalface_alt.xml'
datos = 'datos'
arduino = serial.Serial('/dev/ttyACM0', 9600)

# Parte 1: Crear el fisherRecognizer
print('ejecutando...')
# Crear una lista de imagenes y una lista de los nombres correspondientes
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datos):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datos, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
            
        id += 1
(width, height) = (130, 100)

# Crear un arreglo con las dos listas 
(images, labels) = [numpy.array(lis) for lis in [images, labels]]

# OpenCV entrena un modelo de las imagenes
model=cv2.face.LBPHFaceRecognizer_create()
#model = cv2.createFisherFaceRecognizer()
#model=cv2.createEigenFaceRecognizer()

model.train(images, labels)

# Parte 2: Usar el fisherRecognizer en la camara
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
while (recog==True):
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(100,15,200),3)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        #Se intentara reconocer el rostro
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (100,15,200), 3)

        if prediction[1]<48:

            cv2.putText(im,'%s ' % (names[prediction[0]]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)
            comando = ('H')
            arduino.write(comando.encode())
            usu=str(names[prediction[0]])
            recog = False
            correo.mail(usu)
            break
        
        else:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.putText(im,'No Reconocido',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255),3)

    cv2.imshow('Reconocimiento', im)
    
    key = cv2.waitKey(10)
    if key == 27:
        break
        
time.sleep(5)
arduino.close() 
webcam.release()
cv2.destroyAllWindows()
