import cv2
import numpy as np
import os
import imutils

#Esta lista contiene a todos los usuarios registrados
users=[]

class User(): #Esta clase nos permite crear usuarios
    def __init__(self, nombre, edad, cedula, email, residencia,registrado):
        self.nombre=nombre.capitalize()
        self.edad=edad
        self.cedula=cedula
        self.email=email.lower()
        self.residencia=residencia

        self.registrado=registrado


        self.cantidad_imagenes=300	#Nos indica la cantidad de imagenes tomará el programa para el reconocimiento
        self.camara=1				#Nos indica si se utilizará la webcam del pc (0) o una cámara externa (1)

        self.directorio="image/{}".format(self.nombre)

    #Permite al usuario registrarse en caso de que no lo esté
    def registrar(self):
        if self.registrado==False:

            #Verifica si existe el directorio propio de este usuario, si no existe crea el directorio
            if not os.path.exists(self.directorio):
                os.makedirs(self.directorio)

            #Activa la cámara
            cap = cv2.VideoCapture(self.camara)

            #Este método nos permite reconocer si se encuentra un rostro en una imagen
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            #Este contador toma la cantidad de imágenes que obtiene el programa
            contador=0

            while (cap.isOpened()):
                ret,frame = cap.read()


                if ret==True:

                	#Con esto podemos reescalar el frame
                    frame=imutils.resize(frame, width=640)

                    #Este método nos permite convertir un frame a escala de grises
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    #Se genera una copia del frame original
                    auxFrame=frame.copy()

                    #Detecta la presencia de un rostro en el frame con escala de grises
                    faces = faceClassif.detectMultiScale(gray,scaleFactor=1.2,
                            minNeighbors=5,minSize=(30,30),maxSize=(500,500))


                    for (x,y,w,h) in faces:

                    	#Dibuja un rectangulo sobre el rostro para indicar que se está detectando
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)

                        #Obtiene la imagen del rostro del usuario
                        face = auxFrame[y:y+h,x:x+w]
                        #Reescala la imagen del rostro del usuario
                        face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
                        #Guarda la imagen del usuario en su respectivo directorio
                        cv2.imwrite("{}/{}cara_{}.jpg".format(self.directorio,self.nombre,i), face)

                        #Se le brinda al usuario el porcentaje del proceso que se ha realizado
                        contador+=1
                        porcentaje_anterior = int(round((contador-1)/self.cantidad_imagenes*100,0))
                        porcentaje = int(round(contador/self.cantidad_imagenes*100,0))

                        if porcentaje>porcentaje_anterior:
                            print("Se ha completado el {}% del registro".format(porcentaje))

                    #Muestra la imagen que toma la cámara
                    cv2.imshow("frame",frame)


                	#Finaliza el proceso en caso de presionar la letra "q" o que la cantidad de imagenes tomadas sea la requerida
                    if cv2.waitKey(1) & 0xFF == ord("q") or contador>=self.cantidad_imagenes:
                        break
                else:
                    break

            #Al finalizar el proceso se cierra el video y todas las ventanas
            cap.release()
            cv2.destroyAllWindows()

            self.entrenamiento()

        #Le indica al usuario que ya se encuentra registrado, en caso de registrarse nuevamente
        else:
            print("El usuario {} ya se encuentra registrado".format(self.email))


#Se creó un usuario de prueba
joel=User("Joel",18,305400385,"joel.araya97@gmail.com","Cartago",True)
users.append(joel)

users[0].registrar()
#users[0].entrenamiento()

