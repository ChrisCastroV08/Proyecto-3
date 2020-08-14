from tkinter import *
from tkinter import messagebox
import os
import re
import Detector_de_rostros as fd
from tkinter import ttk
from reportlab.pdfgen import canvas

registerList = []
registeredUsers = []
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
userLogged = []
itemsRegistered = []
master = Tk()
master.title("Project 3")
master.geometry("600x400")
master.resizable(False, False)

main = Toplevel()
main.geometry("600x600")
main.resizable(False, False)
main.withdraw()
item = StringVar()

usuarios = []


def first_screen():
    master.geometry("600x400")
    bgLabel.config(image=menuBg)
    registerButton.config(command=register, font=("System", 18))
    loginButton.config(command=login, font=("System", 18))
    loginButton.place(x=350, y=200)
    registerButton.place(x=170, y=200)
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

    user = fd.User(registerList[2], "{} {}".format(registerList[0], registerList[1]),
                   registerList[6], registerList[5], registerList[4], registerList[3], False)
    usuarios.append(user)

    for i in range(len(usuarios)):
        if usuarios[i].identification == user.identification:
            usuarios[i].register()
            break


def login():
    bgLabel.config(image=loginBg)
    loginButton.config(command=verify_login, font=("System", 15))
    loginButton.place(x=350, y=300)
    backButton.place(x=0, y=357)
    registerButton.place_forget()

    saveFile = read_file("Saved.txt")
    registeredUsers.clear()
    users.delete(0, END)
    i = 0
    while i < len(saveFile):
        registeredUsers.append(saveFile[i].split(",")[0] + " " + saveFile[i].split(",")[1] + " " +
                               saveFile[i].split(",")[2] + " ID: " + saveFile[i].split(",")[5])

        user = fd.User(saveFile[i].split(",")[2], "{} {}".format(saveFile[i].split(",")[0], saveFile[i].split(",")[1]),
                       saveFile[i].split(",")[6], saveFile[i].split(",")[5], saveFile[i].split(",")[4],
                       saveFile[i].split(",")[3], True)
        usuarios.append(user)

        i = i + 1

    for i in registeredUsers:
        users.insert(END, i)
    users.place(x=73, y=40)


def verify_login():
    n = -1

    for i in range(len(usuarios)):
        if int(users.get(ANCHOR)[-9:]) == usuarios[i].identification:
            usuarios[i].identify()
            n = i
            break

    if n >= 0 and usuarios[n].joined == True:
        main_menu()


def main_close():
    if messagebox.askyesno("Exit", "Do you wanna exit?"):
        master.quit()


def on_closing():
    if messagebox.askyesno("Exit", "Are you sure you want to go back to the menu?"):
        main.withdraw()
        master.deiconify()


def main_menu():
    master.withdraw()
    main.deiconify()
    main.protocol("WM_DELETE_WINDOW", on_closing)
    menuLabel.config(image=mainBg)
    exitButton.config(command=on_closing)
    addServiceButton.config(command=add_service)
    createInvoiceButton.config(command=create_invoice)
    menuLabel.place(x=-2, y=-2)
    createInvoiceButton.place(x=120, y=200)
    searchBillsButton.place(x=325, y=200)
    deleteBillsButton.place(x=100, y=300)
    generateInformButton.place(x=325, y=300)
    addServiceButton.place(x=90, y=400)
    updateServiceButton.place(x=325, y=400)
    showPDFButton.place(x=330, y=500)
    exitButton.place(x=150, y=500)
    errorLabel2.place_forget()
    itemCost.place_forget()
    itemDescription.place_forget()
    items.place_forget()
    i = 0
    userLogged.clear()
    while i < len(saveFile):
        if users.get(ANCHOR)[-9:] == saveFile[i].split(",")[5]:
            userLogged.append(saveFile[i])
            print(userLogged)
            return
        else:
            i += 1


def create_invoice():
    exitButton.config(command=main_menu)
    createInvoiceButton.config(command=lambda: creating_invoice(itemDescription.get()))
    createInvoiceButton.place(x=350, y=500)
    searchBillsButton.place_forget()
    deleteBillsButton.place_forget()
    generateInformButton.place_forget()
    addServiceButton.place_forget()
    updateServiceButton.place_forget()
    showPDFButton.place_forget()
    items.place(x=100, y=200)


def creating_invoice(itemes):
    pdf = canvas.Canvas("invoices/invoice 1.pdf", pagesize=(200, 250), bottomup=0)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.line(0, 20, 200, 20)
    pdf.drawCentredString(100, 30, "3C COMPANY")
    pdf.drawCentredString(100, 40, "BILL GENERATOR")

    pdf.line(0, 45, 200, 45)

    pdf.setFont("Times-Bold", 5)
    pdf.drawRightString(55, 55, "INVOICE No. :")
    pdf.drawRightString(55, 65, "CUSTOMER NAME :")
    pdf.drawRightString(55, 75, "CUSTOMER EMAIL :")
    pdf.drawRightString(160, 55, "DATE :")
    pdf.drawRightString(160, 65, "DUE DATE :")
    pdf.drawRightString(160, 75, "RESIDENCE :")

    pdf.roundRect(15, 80, 170, 130, 10, stroke=1, fill=0)
    pdf.line(15, 95, 185, 95)
    pdf.drawCentredString(60, 90, "DESCRIPTION")
    pdf.drawCentredString(125, 90, "QTY")
    pdf.drawCentredString(148, 90, "PRICE")
    pdf.drawCentredString(173, 90, "TOTAL")

    pdf.drawCentredString(30, 105, "ITEM 1")
    pdf.drawCentredString(60, 105, "{}".format(itemes))
    pdf.drawCentredString(145, 105, "{}".format(itemCost.get()))
    pdf.line(15, 200, 185, 200)
    pdf.line(115, 80, 115, 210)
    pdf.line(135, 80, 135, 210)
    pdf.line(160, 80, 160, 210)
    # pdf.showPage()
    pdf.save()


def add_service():
    menuLabel.config(image=addBg)
    exitButton.config(command=main_menu)
    addServiceButton.config(command=adding_service)
    errorLabel2.config(text="")
    errorLabel2.place(x=300, y=300)
    itemDescription.place(x=100, y=200)
    itemCost.place(x=350, y=200)
    addServiceButton.place(x=300, y=500)
    createInvoiceButton.place_forget()
    searchBillsButton.place_forget()
    deleteBillsButton.place_forget()
    generateInformButton.place_forget()
    updateServiceButton.place_forget()
    showPDFButton.place_forget()


def adding_service():
    servicesList = [itemCost.get(), itemDescription.get()]
    i = 0
    while i < len(servicesList):
        if len(servicesList[i]) == 0:
            errorLabel2.config(text="Make sure to fill all the blanks")
            return
        else:
            i = i + 1
    try:
        int(itemCost.get())
    except ValueError:
        errorLabel2.config(text="You must use numbers for the price")
        return
    itemsRegistered.append(itemDescription.get())
    i = 0
    while i < len(itemsRegistered):
        items["values"] = ("{}".format(itemsRegistered[i]))
        i += 1
    errorLabel2.config(fg="lightgreen", text="Service registered succesfully")
    main.after(1500, add_service)


def read_file(path):
    archive = open(path)
    content = archive.readlines()
    archive.close()
    return content


def write_save(saved):
    file = open(saved, 'r+')
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
addBg = load_image("AddBg.png")
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

# ------------------------------------------------------------------

createInvoiceButton = Button(main, text="Create Bill", font=("System", 18), command=create_invoice)
searchBillsButton = Button(main, text="Search Bills", font=("System", 18))
deleteBillsButton = Button(main, text="Delete Bills", font=("System", 18))
generateInformButton = Button(main, text="Generate Inform", font=("System", 18))
addServiceButton = Button(main, text="Add Services", font=("System", 18), command=add_service)
updateServiceButton = Button(main, text="Update Services", font=("System", 18))
showPDFButton = Button(main, text="Show a PDF", font=("System", 18))
itemDescription = Entry(main, width=20, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
itemCost = Entry(main, width=5, font=("Times New Roman", 15), justify=CENTER, bg="lightgrey")
exitButton = Button(main, text="Exit", font=("System", 18))
errorLabel2 = Label(main, text="", font=("System", 15), fg="red", bg="#525659")
items = ttk.Combobox(main, width=20, textvariable=item, font=("Times New Roman", 15), state="readonly")

first_screen()
master.mainloop()
