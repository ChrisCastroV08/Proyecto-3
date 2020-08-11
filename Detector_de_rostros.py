import cv2
import numpy as np
import os
import imutils
from shutil import rmtree

#Esta lista contiene a todos los usuarios registrados
users=[]

class User(): #Esta clase nos permite crear usuarios
    def __init__(self, nombre, apellidos, edad, cedula, email, residencia,registrado):
        self.nombre=nombre.capitalize()
        self.edad=edad
        self.cedula=cedula
        self.email=email.lower()
        self.residencia=residencia

        self.registrado=registrado
        self.actualizando=False

        self.cantidad_imagenes=300	        #Nos indica la cantidad de imagenes nuevas que tomará el programa en el reconocimiento
        self.camara=1				#Nos indica si se utilizará la webcam del pc (0) o una cámara externa (1)
        self.contador=0                  	#Este contador toma la cantidad de imágenes que obtiene el programa
        self.version=0
        self.directorio="image/{}".format(self.nombre)  #Carpeta donde se guardaráan los archivos de cada usuario
            

    #Permite al usuario registrarse en caso de que no lo esté
    def registrar(self):

        #Verifica si se está realizando un registro o una actuaalización
        if self.registrado==False or self.actualizando==True:

            #Toma en cuenta la cantidad de imagenes a obtener
            if self.registrado==False and self.actualizando==False:
                self.cantidad_imagenes=300

            #Verifica si existe el directorio propio de este usuario, si no existe crea el directorio
            if not os.path.exists(self.directorio):
                os.makedirs(self.directorio)

            #Activa la cámara
            cap = cv2.VideoCapture(self.camara)

            #Este método nos permite reconocer si se encuentra un rostro en una imagen
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            #indica la cantidad máxima de imagenes que se obtendrán para el modelo
            limite=self.contador+self.cantidad_imagenes

            #Inicia el bucle de la cámara
            while (cap.isOpened()):
                ret,frame = cap.read()


                if ret==True:

                    #Con esto podemos reescalar el frame
                    frame=imutils.resize(frame, width=640)

                    #Invierte la imagen para que se vea correctamente
                    frame=cv2.flip(frame, 1)

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
                        cv2.imwrite("{}/{}cara_{}.jpg".format(self.directorio,self.nombre,self.contador), face)

                        #Se obtiene la cantidad de imagenes que se han generado en total
                        self.contador+=1

                        #Se obtiene el porcentaje del proceso realizado           
                        if self.version==0:
                            aux1=round((((users[0].contador-1)%users[0].cantidad_imagenes)/users[0].cantidad_imagenes*100),0)
                            aux2=round(((users[0].contador%users[0].cantidad_imagenes)/users[0].cantidad_imagenes*100),0)
                        else:
                            aux1=round((((users[0].contador-1-300)%users[0].cantidad_imagenes)/users[0].cantidad_imagenes*100),0)
                            aux2=round((((users[0].contador-300)%users[0].cantidad_imagenes)/users[0].cantidad_imagenes*100),0)
                        
                        porcentaje_anterior = int(aux1)
                        porcentaje = int(aux2)

                        if self.contador%self.cantidad_imagenes==0:
                            porcentaje=100
                            
                        #Se le brinda al usuario el porcentaje del proceso que se ha realizado
                        if porcentaje>porcentaje_anterior and porcentaje%5==0:
                            print("Se ha completado el {}% del registro".format(porcentaje))

                    #Muestra la imagen que toma la cámara
                    cv2.imshow("frame",frame)


                    #Finaliza el proceso en caso de presionar la letra "q" o que la cantidad de imagenes tomadas sea la requerida
                    if cv2.waitKey(1) & 0xFF == ord("q") or self.contador>=limite:
                        break
                else:
                    break

            #Al finalizar el proceso se cierra el video y todas las ventanas
            cap.release()
            cv2.destroyAllWindows()

            self.entrenamiento()

        #Le indica al usuario que ya se encuentra registrado, en caso de registrarse nuevamente
        else:
            print("El usuario {} ya se encuentra registrado".format(self.nombre))


    #Realiza el entrenamiento del modelo para la detección del rostro del usuario
    def entrenamiento(self):

        #Verifica si se está actualizando o registrando
        if self.actualizando==True:

            #Verifica si existen modelos del usuario creados
            if os.path.exists("{}/EigenFaces_{}.xml".format(self.directorio,self.nombre)):

                #Si existen modelos del usuario, se eliminan
                print("Realizando preparaciones para actualizar...")
                os.remove("{}/EigenFaces_{}.xml".format(self.directorio,self.nombre))

        label,labels,rostros = 0,[],[]
        print("Leyendo las imagenes registradas...")

        #Se toman las imágenes creadas
        for archivo in os.listdir(self.directorio):
            #print("Imagen: {}".format(archivo))

            #Se guardan etiquetas que identifican al usuario en una lista
            labels.append(label)

            #Se guardan las imágenes con los rostros en escala de grises del usuario en una lista
            rostros.append(cv2.imread("{}/{}".format(self.directorio,archivo),0))

        #Se declara la variable que puede identificar la similitud de los rostros
        face_recognizer = cv2.face.EigenFaceRecognizer_create()

        print("Entrenando el programa...")

        #Se inicia el entrenamiento del programa
        face_recognizer.train(rostros, np.array(labels))
        #Se guradan los modelos del programa en un archivo ".xml"
        face_recognizer.write("{}/EigenFaces_{}.xml".format(self.directorio,self.nombre))

        print("Se ha completado el entrenamiento del modelo")

        #Se le indica al usuario la finalización del proceso realizado
        if self.registrado==False:
            print("Se ha completado el registro")
        if self.actualizando==True:
            print("Se han actualizado los modelos")

        #Se restauran las variables a sus valores correspondientes
        self.registrado=True
        self.actualizando=False

    #Permite actualizar los modelos que el usuario tenga, agregando más
    def actualizar(self):

        #Activa el modo de actualización
        self.actualizando=True
        #Determina la cantidad de nuevas imagenes que se van a agregar
        self.cantidad_imagenes=100
        #Indica la cantidad de veces que se han actualizado los modelos del usuario
        self.version+=1
        print("Se empezará a actualizar el modelo...")

        self.registrar()

    #Permite al usuario eliminar su propio directorio
    def eliminar_usuario(self):
        
        #Se reestablecen los atributos del usuario a sus valores originales
        self.contador=0
        self.version=0
        self.cantidad_imagenes=300
        
        #Comprueba si el directorio existe
        if os.path.exists(self.directorio):

            #Elimina el directorio y todo los archivos que contenga
            print("El usuario {} se está eliminando...".format(self.nombre))
            rmtree(self.directorio)
            print("El usuario ha sido eliminado")

    #Este método confirma la identidad del usuario
    def identificar(self):
        print("Realizando preparativos para iniciar la identificación...")

        #Se declara la variable que puede identificar la similitud de los rostros
        face_recognizer = cv2.face.EigenFaceRecognizer_create()
        #Se le indica a la variable la ubicación del archivo entrenado
        face_recognizer.read("{}/EigenFaces_{}.xml".format(self.directorio,self.nombre))

        #Inicia la cámara
        cap = cv2.VideoCapture(self.camara)

        #Se agrega el método que permite reconocer la presencia de un rostro en una imagen
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        #Se agregaron 2 variables para comprobar si la identidad del usuario es correcta
        verificacion_positiva=0
        verificacion_negativa=0

        while (cap.isOpened()):
            ret,frame = cap.read()
            
            if ret==True:

                #Se invierte la imagen para evitar el efecto espejo
                frame=cv2.flip(frame, 1)
                #Este método nos permite convertir un frame a escala de grises
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #Se genera una copia del frame en escala de grises
                auxFrame=gray.copy()

                #Detecta la presencia de un rostro en el frame con escala de grises
                faces = faceClassif.detectMultiScale(gray,scaleFactor=1.2,
                            minNeighbors=5,minSize=(30,30),maxSize=(500,500))
                                    
                for (x,y,w,h) in faces:
                    #Obtiene la imagen del rostro del usuario
                    face = auxFrame[y:y+h,x:x+w]
                    #Reescala la imagen del rostro del usuario
                    face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)

                    resultado = face_recognizer.predict(face)

                    if resultado[1]<4000:
                        #Se indica el nombre del usuario
                        cv2.putText(frame, "{}".format(self.nombre),(x,y-5),1,1.2,(255,0,0),1,cv2.LINE_AA)
                        #Dibuja un rectángulo azul sobre el rostro para indicar que se está detectando el rostro del usuario
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
                        #Se incrementa en 1 la variable que confirma la precensia del usuario
                        verificacion_positiva+=1
                    else:
                        #Se indica que el usuario que se encuentra en la cámara es desconocido
                        cv2.putText(frame, "Desconocido",(x,y-5),1,1.2,(0,0,200),1,cv2.LINE_AA)
                        #Dibuja un rectángulo rojo sobre el rostro para indicar que se está detectando un rostro desconocido
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
                        #Se incrementa en 1 la variable que indica que no es el usuario correcto
                        verificacion_negativa+=1

                    #print("pos {}, neg {}".format(verificacion_positiva,verificacion_negativa))

                #Si la variable de verificaion del rostro del usuario llega a 100 se confirma su identidad
                if verificacion_positiva>=100:
                    print("Hola {}, se ha comprobado tu identidad, puedes ingresar".format(self.nombre))
                    break

                #Si la variable de verificación de un rostro diferente al del usuario supera los 600, indica que no es el usuario correspondiente y prohíbe el acceso 
                if verificacion_negativa>=600:
                    print("No eres {}, no puedes ingresar".format(self.nombre))
                    break
                    

                #Muestra las imágenes que obtiene la cámara
                cv2.imshow("frame",frame)


                #Finaliza el proceso en caso de presionar la letra "q" o que la cantidad de imagenes tomadas sea la requerida
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        #Cierra la cámara y las ventanas abiertas
        cap.release()
        cv2.destroyAllWindows()

#Se creó un usuario de prueba
joel=User("Joel", "Gómez Araya", 18, 305400385,"joel.araya97@gmail.com","Cartago",True)
users.append(joel)

#users[0].registrar()
#users[0].entrenamiento()
#users[0].actualizar()
#users[0].eliminar_usuario()

users[0].identificar()
