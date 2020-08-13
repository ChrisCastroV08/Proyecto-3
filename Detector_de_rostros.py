import cv2
import numpy as np
import os
import imutils
from shutil import rmtree

#This list contains all registered users
users=[]

class User(): #This class allows us to create users
    def __init__(self, name, surnames, age, identification, email, residence,registered):
        self.name=name.capitalize()
        self.surnames=surnames.capitalize()
        self.age=age
        self.identification=identification
        self.email=email.lower()
        self.residence=residence

        self.joined=False
        self.testing=False

        self.registered=registered
        self.updating=False

        self.quantity_images=300	        #It indicates the amount of new images that the program will take in recognition
        self.camera=1				#It tells us if the pc webcam (0) or an external camera (1) is used
        self.count=0                  	#This counter gives the number of images that the program obtains
        self.version=0
        self.directory="image/{}".format(self.name)  #Folder where the files of each user are saved
            

    #Allows the user to register in case they are not
    def register(self):

        #Check if a registration or an update is taking place
        if self.registered==False or self.updating==True:

            #Take into account the number of images to obtain
            if self.registered==False and self.updating==False:
                self.quantity_images=300

            #Check if this user's own directory exists, if it does not exist create the directory
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

            #Turn on the camera
            cap = cv2.VideoCapture(self.camera)

            #This method allows us to recognize if a face is found in an image
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            #Indicates the maximum number of images that will be obtained for the model
            limit=self.count+self.quantity_images

            #Start the camera loop
            while (cap.isOpened()):
                ret,frame = cap.read()


                if ret==True:

                    #Resize the frame
                    frame=imutils.resize(frame, width=640)

                    #Invert the image to make it look correct
                    frame=cv2.flip(frame, 1)

                    #This method allows us to convert a frame to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    #A copy of the original frame is generated
                    auxFrame=frame.copy()

                    #Detects the presence of a face in the grayscale frame
                    faces = faceClassif.detectMultiScale(gray,scaleFactor=1.2,
                            minNeighbors=5,minSize=(30,30),maxSize=(500,500))

                    
                    for (x,y,w,h) in faces:

                    	#Draw a rectangle on the face to indicate that it is being detected
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)

                        #Get the image of the user's face
                        face = auxFrame[y:y+h,x:x+w]
                        #Resize the user's face image
                        face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
                        #Save the user's image in his respective directory
                        cv2.imwrite("{}/{}cara_{}.jpg".format(self.directory,self.name,self.count), face)

                        #Get the amount of images that have been generated
                        self.count+=1

                        #The percentage of the process carried out is obtained           
                        if self.version==0:
                            aux1=round((((users[0].count-1)%users[0].quantity_images)/users[0].quantity_images*100),0)
                            aux2=round(((users[0].count%users[0].quantity_images)/users[0].quantity_images*100),0)
                        else:
                            aux1=round((((users[0].count-1-300)%users[0].quantity_images)/users[0].quantity_images*100),0)
                            aux2=round((((users[0].count-300)%users[0].quantity_images)/users[0].quantity_images*100),0)
                        
                        last_percentage = int(aux1)
                        percentage = int(aux2)

                        if self.count%self.quantity_images==0:
                            percentage=100
                            
                        #The user is given the percentage of the process that has been carried out
                        if percentage>last_percentage and percentage%5==0:
                            print("{}% of registration is complete".format(percentage))

                    #Displays the image taken by the camera
                    cv2.imshow("frame",frame)


                    #The process ends in case of pressing the letter "q" or that the amount of images taken is the required
                    if cv2.waitKey(1) & 0xFF == ord("q") or self.count>=limit:
                        break
                else:
                    break

            #At the end of the process the video and all the windows are closed
            cap.release()
            cv2.destroyAllWindows()

            self.training()

        #It indicates to the user that he is already registered, in case of registering again
        else:
            print("User {} is already registered".format(self.name))


    #Perform the model training for the detection of the user's face
    def training(self):

        #Check if it is updating or registering
        if self.updating==True:

            #Check if there are user models created
            if os.path.exists("{}/EigenFaces_{}.xml".format(self.directory,self.name)):

                #If user models exist, they are removed
                print("Making preparations to upgrade...")
                os.remove("{}/EigenFaces_{}.xml".format(self.directory,self.name))

        label,labels,rostros = 0,[],[]
        print("Reading the registered images...")

        #The created images are taken
        for archivo in os.listdir(self.directory):
            #print("Imagen: {}".format(archivo))

            #The labels that identify the user are stored in a list
            labels.append(label)

            #Images with the user's grayscale faces are saved in a list
            rostros.append(cv2.imread("{}/{}".format(self.directory,archivo),0))

        #The variable that can identify the similarity of the faces is declared
        face_recognizer = cv2.face.EigenFaceRecognizer_create()

        print("Training the program...")

        #Program training starts
        face_recognizer.train(rostros, np.array(labels))
        #The program models are saved in a ".xml" file
        face_recognizer.write("{}/EigenFaces_{}.xml".format(self.directory,self.name))

        print("Model training is completed")

        #The user is informed of the completion of the process performed
        if self.registered==False:
            print("Registration is complete")
        if self.updating==True:
            print("Models have been updated")

        #Variables are restored to their corresponding values
        self.registered=True
        self.updating=False

        self.testing=True

        

    #It allows updating the models that the user has, adding more
    def update(self):

        #Activate update mode
        self.updating=True
        #Determines the number of new images to add
        self.quantity_images=100
        #Indicates the number of times the user's models have been updated
        self.version+=1
        print("The model will begin to update...")

        self.register()

    #Allows user to delete their own directory
    def delet_user(self):
        
        #User attributes are reset to their original values
        self.count=0
        self.version=0
        self.quantity_images=300
        
        #Check if the directory exists
        if os.path.exists(self.directory):

            #Delete the directory and all files it contains
            print("User {} is being removed...".format(self.name))
            rmtree(self.directory)
            print("User has been deleted")

    #This method confirms the identity of the user
    def identify(self):
        print("Making preparations to start identification...")

        #The variable that can identify the similarity of the faces is declared
        face_recognizer = cv2.face.EigenFaceRecognizer_create()
        #The location of the trained file is indicated to the variable
        face_recognizer.read("{}/EigenFaces_{}.xml".format(self.directory,self.name))

        #Start the camera
        cap = cv2.VideoCapture(self.camera)

        #The method that allows to recognize the presence of a face in an image is added
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        #2 variables added to check if user identity is correct
        positive_check=0
        negative_check=0

        while (cap.isOpened()):
            ret,frame = cap.read()
            
            if ret==True:

                #Image is inverted to avoid mirror effect
                frame=cv2.flip(frame, 1)
                #This method allows us to convert a frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #A grayscale copy of the frame is generated
                auxFrame=gray.copy()

                #Detects the presence of a face in the frame with grayscale
                faces = faceClassif.detectMultiScale(gray,scaleFactor=1.2,
                            minNeighbors=5,minSize=(30,30),maxSize=(500,500))
                                    
                for (x,y,w,h) in faces:
                    #Get the image of the user's face
                    face = auxFrame[y:y+h,x:x+w]
                    #Resize the user's face image
                    face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)

                    resultado = face_recognizer.predict(face)

                    if resultado[1]<4000:
                        #Username is indicated
                        cv2.putText(frame, "{}".format(self.name),(x,y-5),1,1.2,(255,0,0),1,cv2.LINE_AA)
                        #Draw a blue rectangle on the face to indicate that the user's face is being detected
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
                        #The variable that confirms the presence of the user is increased by 1
                        positive_check+=1
                    else:
                        #It indicates that the user who is in the camera is unknown
                        cv2.putText(frame, "Desconocido",(x,y-5),1,1.2,(0,0,200),1,cv2.LINE_AA)
                        #Draw a red rectangle on the face to indicate that an unknown face is being detected
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
                        #The variable that indicates that it is not the correct user is increased by 1
                        negative_check+=1

                    #print("pos {}, neg {}".format(positive_check,negative_check))

                #If the verification variable of the user's face reaches 100, his identity is confirmed
                if positive_check>=100:
                    print("Hello {}, your identity has been verified, you can enter".format(self.name))
                    self.joined=True
                    break

                #If the verification variable of a face other than that of the user exceeds 600, it indicates that it is not the corresponding user and prohibits access
                if negative_check>=600:
                    print("You are not {}, you cannot enter".format(self.name))
                    Self.joined=False
                    break
                    

                #Displays the images obtained by the camera
                cv2.imshow("frame",frame)


                #The process ends in case of pressing the letter "q" or that the amount of images taken is the required
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        #Close the camera and open windows
        cap.release()
        cv2.destroyAllWindows()

#A test user was created that only runs if this file is run
if __name__ == "__main__":

    joel=User("Joel", "Gómez Araya", 18, 305400385,"joel.araya97@gmail.com","Cartago",True)
    users.append(joel)

    #users[0].register()
    #users[0].training()
    #users[0].update()
    #users[0].delet_user()
    #users[0].identify()


