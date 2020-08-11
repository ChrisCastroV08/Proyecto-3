from tkinter import *
from tkinter import ttk
import os
import re

registerList = []
registeredUsers = []
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

master = Tk()
master.title("Project 3")
master.geometry("600x400")
master.configure(bg="#525659")
master.resizable(False, False)

main = Toplevel()
main.geometry("700x700")
main.resizable(False, False)
main.withdraw()


def first_screen():
    master.geometry("600x400")
    bgLabel.config(image=menuBg)
    registerButton.config(command= register, font = ("System", 18))
    loginButton.place(x=350, y=200)
    registerButton.place(x=170, y=200)
    lastNameEntry.place_forget()
    firstNameEntry.place_forget()
    nameEntry.place_forget()
    IDEntry.place_forget()
    ageEntry.place_forget()
    emailEntry.place_forget()
    residenceEntry.place_forget()
    backButton.place_forget()
    errorLabel.place_forget()


def main_menu():
    master.withdraw()
    main.deiconify()


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
    registeredUsers.clear()
    registerList = [firstNameEntry.get(), lastNameEntry.get(), nameEntry.get()
                    , residenceEntry.get(), emailEntry.get(), IDEntry.get(),ageEntry.get()]
    saveFile = read_file("Saved.txt")
    i = 0
    while i < len(registerList):
        if len(registerList[i]) == 0:
            errorLabel.config(text="Make sure to fill all the blanks")
            return
        else:
            i=i+1
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
            errorLabel.config(text="This user is already registered!")
            return
        else:
            i = i + 1
    if int(ageEntry.get()) >= 18:
        pass
    else:
        errorLabel.config(text="You must be 18 years old or older")
        return
    if (re.search(regex, emailEntry.get())):
        pass
    else:
        errorLabel.config(text="Please enter a valid email")
        return
    errorLabel.config(text="")
    write_save(registerList)
    i = 0

    while i < len(saveFile):
        registeredUsers.append(saveFile[i].split(",")[2])
        print(registeredUsers)
        i = i+1
    print(registeredUsers)

def login():
    users['values'] = ()


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
        i = i+1
    file.close()


def load_image(image_name):
    image_path = os.path.join("Images", image_name)
    return PhotoImage(file=image_path)


menuBg = load_image("MenuBg.png")
registerBg = load_image("RegisterBg.png")

bgLabel = Label(master)
bgLabel.place(x=-2, y=-2)
errorLabel = Label(master, text="", font=("System", 15), fg="red", bg="#525659")
saveFile = read_file("Saved.txt")
loginButton = Button(master, text="Login", font=("System", 18))
registerButton = Button(master, text="Register")
backButton = Button(master, text="Go\nBack", font=("System", 15), command=first_screen)
users = ttk.Combobox(master, state="readonly", width=27)
nameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
firstNameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
lastNameEntry = Entry(master, width=12, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
IDEntry = Entry(master, width=20, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
ageEntry = Spinbox(master, width=3, from_=0, to=100, font=("Times New Roman", 15), bg="lightgrey")
emailEntry = Entry(master, width=25, font=("Times New Roman", 15), bg="lightgrey")
residenceEntry = Entry(master, width=25, font=("Times New Roman", 15), bg="lightgrey")
first_screen()
master.mainloop()
