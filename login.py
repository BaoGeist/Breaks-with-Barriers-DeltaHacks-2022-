from tkinter import *
import os
from PIL import ImageTk, Image
import threading
import time

def validateLogin():
    input_email=email.get()
    input_name=name.get()
    with open('info.csv', 'r') as f:
        lines = f.read().splitlines()
        last_line_info = lines[-1].split(",")
        if input_email==last_line_info[0]:
            if input_name==last_line_info[1]:
                os.system('frontend.py')
            else:
                open_popup()


def open_popup():
   top= Toplevel(Window)
   top.geometry("800x250")
   top.title("Incorrect information")
   Label(top, text= "Incorrect information, please try again", font=('Mistral 18 bold')).place(x=150,y=80)         

#window
Window = Tk()
Window.geometry('400x800')  
Window.title('Breaks Without Barriers')
Window.configure(bg='white')

EmptyLabel=Label(Window,bg='#BBADE6').grid(row=0,column=0)

imagee = ImageTk.PhotoImage(Image.open('imagelogin.jpg'))
lblImage = Label(Window, bg='white', image = imagee).grid(row=0, column=1, columnspan = 2)

#username label and text entry box
frmLogin = Frame(Window, bg='white').grid(row=1, column = 1, columnspan = 2)
emailLabel = Label(frmLogin, text="Full Name", bg='white').grid(row=1, column=1)
email = StringVar()
emailEntry = Entry(frmLogin, textvariable=email, bg='white').grid(row=1, column=2)  

#password label and password entry box
nameLabel = Label(frmLogin,text="Email", bg='white').grid(row=2, column=1)  
name = StringVar()
nameEntry = Entry(frmLogin, textvariable=name, bg='white').grid(row=2, column=2)  

#login button
imagee2 = ImageTk.PhotoImage(Image.open('loginbutton.jpg'))
loginButton = Button(frmLogin, image = imagee2, bg='white', borderwidth = 0, command=validateLogin).grid(row=3, column=1, columnspan = 2)  

Window.mainloop()