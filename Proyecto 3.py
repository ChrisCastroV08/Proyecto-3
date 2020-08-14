from tkinter import *
from tkinter import messagebox
import os
import re
import Detector_de_rostros as fd

registerList = []
registeredUsers = []
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

master = Tk()
master.title("Project 3")
master.geometry("600x400")
master.resizable(False, False)

main = Toplevel()
main.geometry("600x600")
main.resizable(False, False)
main.withdraw()

usuarios=[]

def first_screen():
    master.geometry("600x400")
    bgLabel.config(image=menuBg)
    registerButton.config(command=register, font=("System", 18))
    loginButton.config(command=login)
    loginButton.place(x=350, y=200)
    registerButton.place(x=170, y=200)
    bot.pack()
    users.place_forget()
    lastNameEntry.place_forget()
    firstNameEntry.place_forget()
    nameEntry.place_forget()
    IDEntry.place_forget()
    ageEntry.place_forget()
    emailEntry.place_forget()
    residenceEntry.place_forget()
    backButton.place_forget()
    errorLabel.place_forget()


def register():
    bgLabel.config(image=registerBg)
    registerButton.config(command=verify_register, font=("System", 15))
    firstNameEntry.place(x=90, y=50)
    lastNameEntry.place(x=240, y=50)
    nameEntry.place(x=390, y=50)
    IDEntry.place(x=90, y=120)
    ageEntry.place(x=390, y=120)
    emailEntry.place(x=180, y=190)
    residenceEntry.place(x=180, y=260)
    registerButton.place(x=350, y=300)
    errorLabel.place(x=280, y=330)
    backButton.place(x=0, y=357)
    loginButton.place_forget()


def verify_register():
    registerList = [firstNameEntry.get().capitalize(), lastNameEntry.get().capitalize(),
                    nameEntry.get().capitalize(), residenceEntry.get().capitalize(), emailEntry.get(),
                    IDEntry.get(), ageEntry.get()]
    saveFile = read_file("Saved.txt")
    i = 0
    while i < len(registerList):
        if len(registerList[i]) == 0:
            errorLabel.config(text="Make sure to fill all the blanks")
            return
        else:
            i = i + 1
    i = 0
    while i < 4:
        try:
            int(registerList[i])
            errorLabel.config(text="Your name, first name, last name \nor residence cannot be numbers")
            return
        except ValueError:
            pass
            i = i + 1
    if len(IDEntry.get()) == 9:
        try:
            int(IDEntry.get())
        except ValueError:
            errorLabel.config(text="You must use numbers for the ID")
            return
    else:
        errorLabel.config(text="Make sure to write a valid 9 digit ID")
        return
    i = 0
    while i < len(saveFile):
        if IDEntry.get() == saveFile[i].split(",")[5]:
            errorLabel.config(fg="red", text="This user is already registered!")
            return
        else:
            i = i + 1
    if int(ageEntry.get()) >= 18:
        pass
    else:
        errorLabel.config(text="You must be 18 years old or older")
        return
    if re.search(regex, emailEntry.get()):
        pass
    else:
        errorLabel.config(text="Please enter a valid email")
        return
    errorLabel.config(fg="lightgreen", text="User successfully registered!")
    write_save(registerList)

    user = fd.User(registerList[2],"{} {}".format(registerList[0],registerList[1]),
                    registerList[6],registerList[5],registerList[4],registerList[3],False)
    usuarios.append(user)

    for i in range(len(usuarios)):
        if usuarios[i].identification==user.identification:
            usuarios[i].register()
            break


def login():
    bgLabel.config(image=loginBg)
    loginButton.config(command=verify_login)
    loginButton.place(x=350,y=300)
    backButton.place(x=0, y=357)
    registerButton.place_forget()

    saveFile = read_file("Saved.txt")
    registeredUsers.clear()
    users.delete(0, END)
    i = 0
    while i < len(saveFile):
        registeredUsers.append(saveFile[i].split(",")[0] + " " + saveFile[i].split(",")[1] + " " +
                               saveFile[i].split(",")[2] + " ID: " + saveFile[i].split(",")[5])
        
        user = fd.User(saveFile[i].split(",")[2],"{} {}".format(saveFile[i].split(",")[0],saveFile[i].split(",")[1]),
                    saveFile[i].split(",")[6],saveFile[i].split(",")[5],saveFile[i].split(",")[4],saveFile[i].split(",")[3],True)
        usuarios.append(user)
        
        i = i + 1

    for i in registeredUsers:
        users.insert(END, i)
    users.place(x=73, y=40)


def verify_login():
    n=-1

    for i in range(len(usuarios)):
        if int(users.get(ANCHOR)[-9:])==usuarios[i].identification:
            usuarios[i].identify()
            n=i
            break

    if n>=0 and usuarios[n].joined==True:
        print("Ingresado")
        
            



def main_close():
    if messagebox.askyesno("Exit", "Do you wanna exit?"):
        master.quit()


def on_closing():
    if messagebox.askyesno("Back", "Are you sure you want to go back to the menu?"):
        main.withdraw()
        master.deiconify()


def main_menu():
    master.withdraw()
    main.deiconify()
    main.protocol("WM_DELETE_WINDOW", on_closing)
    menuLabel.config(image=mainBg)
    menuLabel.place(x=-2, y=-2)
    createBillButton.place(x=0, y=0)


def read_file(path):
    archive = open(path)
    content = archive.readlines()
    archive.close()
    return content


def write_save(saved):
    file = open("Saved.txt", 'r+')
    file.read()
    file.write('\n')
    i = 0
    while i < len(saved):
        file.write(str(saved[i]) + ',')
        i = i + 1
    file.close()


def load_image(image_name):
    image_path = os.path.join("image", image_name)
    return PhotoImage(file=image_path)


menuBg = load_image("MenuBg.png")
registerBg = load_image("RegisterBg.png")
loginBg = load_image("LoginBg.png")
mainBg = load_image("MainBg.png")

bgLabel = Label(master)
bgLabel.place(x=-2, y=-2)
menuLabel = Label(main)
# master.protocol("WM_DELETE_WINDOW", main_close)
saveFile = read_file("Saved.txt")
errorLabel = Label(master, text="", font=("System", 15), fg="red", bg="#525659")
loginButton = Button(master, text="Login", font=("System", 18))
registerButton = Button(master, text="Register")
backButton = Button(master, text="Go\nBack", font=("System", 15), command=first_screen)
users = Listbox(master, width=52, bg="lightgrey", font=("Times New Roman", 15),
                selectmode=SINGLE, justify=CENTER)
nameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
firstNameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
lastNameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
IDEntry = Entry(master, width=20, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
ageEntry = Spinbox(master, width=3, from_=0, to=100, font=("Times New Roman", 15), bg="lightgrey")
emailEntry = Entry(master, width=25, font=("Times New Roman", 15), bg="lightgrey")
residenceEntry = Entry(master, width=25, font=("Times New Roman", 15), bg="lightgrey")

bot = Button(master, text="Enter", command=main_menu)

# ------------------------------------------------------------------

createBillButton = Button(main, text="Create Bill", font=("System", 16))
searchBillsButton = Button(main, text="Search Bills", font=("System", 16))
deleteBillsButton = Button(main, text="Delete Bills", font=("System", 16))
generateInformButton = Button(main, text="Generate Inform", font=("System", 16))
addServiceButton = Button(main, text="Add Services", font=("System", 16))
updateServiceButtonButton = Button(main, text="Update Services", font=("System", 16))
showPDFButton = Button(main, text="Show a PDF", font=("System", 16))

first_screen()
master.mainloop()
