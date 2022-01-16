#imports
import tkinter as tk
import time, threading, sys
import backend
from PIL import ImageTk, Image
import webbrowser
from tkinter import messagebox
from tkinter import ttk

#states
boolProd = False
boolBreak = False
global lstTask

#functions
#starts the productivity session
def function_prod():
    global boolProd
    boolProd = True
    btnProd.config(state = 'disable')
    btnEnd.config(state='normal')
    hours = entProdHour.get()
    minutes = entProdMin.get()
    btnProd.config(text = hours + minutes)
    if varWater.get() == 1:
        thread = threading.Thread(target = function_water, args = (1,))
        thread.start()
    if varPosture.get() == 1:
        thread = threading.Thread(target = function_posture, args = (1,))
        thread.start()
    thread2 = threading.Thread(target = function_prod_isolated, args = (hours, minutes))
    thread2.start()

#counts down the time for productivity, branaches off from function_prod()
def function_prod_isolated(hours, minutes):
    time_s = int(hours) * 3600 + int(minutes) * 60
    for i in range(time_s, 0, -5):
        hours = int(i/3600)
        minutes = int((i-3600*hours)/60)
        seconds = i - hours * 3600 - minutes * 60 
        lblProd.config(text = f'You should remain productive for {hours} hours, {minutes} minutes and {seconds} seconds')
        time.sleep(1)
    proLevel.config(value = backend.function_time(time_s)*100)
    backend.function_add_stats(round(time_s/3600,2))
    function_prod_popup()
    function_break()

#counts down the time for a break, is called by function_prod_isolated()
def function_break():
    global boolBreak
    hours = entBreakHour.get()
    minutes = entBreakMin.get()
    time_s = int(hours) * 3600 + int(minutes) * 60
    for i in range(time_s, 0, -5):
        hours = int(i/3600)
        minutes = int((i-3600*hours)/60)
        seconds = i - hours * 3600 - minutes * 60 
        lblBreak.config(text = f'Break: {hours} hours, {minutes} minutes and {seconds} seconds')
        time.sleep(1)
    if varMessage.get() == 1:
        number = entMessage.get()
        backend.function_message(number, "You have finished your break. Get back to work!")
    function_break_popup()
    btnProd.config(state = 'normal')
    lblSocials.grid()
    lblSocialsImage.grid()
    sys.exit()

#creates a pop-up function for when productivity ends to alert the user
def function_prod_popup():
    topProd = tk.Toplevel(root)
    topProd.geometry("750x250")
    topProd.title("Break Time!")
    tk.Label(topProd, text= "You've finished with your productivity, take a well-deserved break!", font=('Calibri 18 bold'), bg = 'black', fg = 'white').pack(fill = tk.Y, expand=True, side = tk.LEFT)

def function_break_popup():
    topBreak = tk.Toplevel(root)
    topBreak.geometry("750x250")
    topBreak.title("Break Time Over")
    tk.Label(topBreak, text= "Hope you've have a good break. Time to get back to work", font=('Calibri 18 bold'), bg = 'black', fg = 'white').pack(fill = tk.Y, expand=True, side = tk.LEFT)

#creates a pop-up window with a reminder to have a good posture after a set amount of time
#currently mapped to entWater and initiates when studying was started
def function_water(nothing):
    timeWater = int(entWater.get())
    time.sleep(timeWater*60)
    topWater = tk.Toplevel(root)
    imagee = ImageTk.PhotoImage(Image.open('waterreminder.jpg'))
    topWater.geometry("450x750")
    topWater.title("waterwaterwater")
    lblWater = tk.Label(topWater, image = imagee, font=('Calibri 18 bold'), bg = 'black', fg = 'white')
    lblWater.pack(fill = tk.Y, expand=True, side = tk.LEFT)
    lblWater.image = imagee
    sys.exit()

#creates a pop-up window with a reminder to have a good posture after a set amount of time
#currently mapped to entPosture and initiates when studying was started
def function_posture(nothing):
    timePosture = int(entPosture.get())
    time.sleep(timePosture*60)
    topPosture = tk.Toplevel(root)
    imagee = ImageTk.PhotoImage(Image.open('posturereminder.jpg'))
    topPosture.geometry("450x750")
    topPosture.title("Posture Check-In")
    lblPosture = tk.Label(topPosture, image = imagee, font=('Calibri 18 bold'), bg = '#9FEFE5', fg = 'white')
    lblPosture.pack(fill = tk.Y, expand=True, side = tk.LEFT)
    lblPosture.image = imagee
    sys.exit()

#used to change the theme of the ui 
#currently coded with assumption that there is only two set colours
#currently NOT MAPPED TO ANY BUTTON
def function_theme():
    global colours
    #widgets with colour 1
    lstWidgets1 = []
    #widgets with colour 2
    lstWidgets2 = []
    for wid in lstWidgets1:
        wid.config(bg = colours[0])
    for wid in lstWidgets2:
        wid.config(bg = colours[1])

#used to create a pop up window containnig a scatterplot of the hours studied over time
#currently mapped to btnStor
def function_stats_button():
    backend.function_stats()
    imagee = ImageTk.PhotoImage(Image.open('figure.png'))
    topPosture = tk.Toplevel(root)
    topPosture.geometry("700x600")
    topPosture.title("waterwaterwater")
    lblImage = tk.Label(topPosture, image = imagee, bg = 'black', fg = 'white', width = 600, height = 1000)
    lblImage.pack(fill = tk.Y, expand=True, side = tk.LEFT)
    lblImage.image = imagee

def function_Spotify_button():
    selection = int(str(v.get()))
    stor = backend.spotify_playlists()
    lstPlaylists = str(stor[0]).split(', ')
    lstDescriptions = str(stor[1]).split(', ')
    lstLink = str(stor[2]).split(', ')
    for i in range(len(lstLink)):
        lstLink[i] = lstLink[i].replace('"', "")
        lstLink[i] = lstLink[i].replace("'", "")
        lstLink[i] = lstLink[i].replace('{', "")
        lstLink[i] = lstLink[i].replace('}', "")
    webbrowser.open(lstLink[selection])

def function_end():
    btnProd.config(state = 'normal')
    btnEnd.config(state='disabled')
    lblProd.config(text = 'Set a timer - how productive are you feeling?')
    lblBreak.config(text = 'How long would you like your break to be?')

def newTask():
    global lstTask
    task = entTask.get()
    if task != '':
        lboTask.insert(tk.END, task)
        entTask.delete(0, 'end')
        lstTask.append('\n'+ task)
        f = open('tasks.txt', 'wt')
        for item in lstTask:
            f.write(item)
        f.close()
    else:
        messagebox.showwarning("Warning", "Please enter some task.")
 
def deleteTask():
    global lstTask
    task = (lboTask.get(tk.ACTIVE))
    lstTask.remove(task)
    f = open('tasks.txt', 'wt')
    for item in lstTask:
        f.write(item)
    f.close()
    lboTask.delete(tk.ANCHOR)
    
def SQ3R_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("SQ3R")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text= backend.function_text_pop(0), font=('Alata 12')).pack(side  = tk.TOP)

def Retrieval_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Retrieval Practive")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(1), font=('Alata 12')).pack(side  = tk.TOP)

def Spaced_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Spaced Practice")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(2), font=('Alata 12')).pack(side  = tk.TOP)

def Exercise_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Exercising Before Studying")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(3), font=('Alata 12')).pack(side  = tk.TOP)

def PQ4R_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("PQ4R")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(4), font=('Alata 12')).pack(side  = tk.TOP)

def Feynman_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("The Feynman Technique")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(5), font=('Alata 12')).pack(side  = tk.TOP)

def Leitner_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Leitner System")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(6), font=('Alata 12')).pack(side  = tk.TOP)

def Color_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Color-Coded Notes")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(7), font=('Alata 12')).pack(side  = tk.TOP)

def Mapping_popup():
   top= tk.Toplevel(root)
#    top.geometry("1900x700")
   top.title("Mind Mapping")
   tk.Label(top, text = 'All About the Study Method', font = ('Alata 16 bold')).pack(side = tk.TOP)
   tk.Label(top, text = backend.function_text_pop(8), font=('Alata 12')).pack(side  = tk.TOP)

root = tk.Tk()
imagee = ImageTk.PhotoImage(Image.open('icon.jpg'))
root.iconphoto(False, imagee)
root.title('Breaks Without Barriers')
root.resizable(width = False, height = False)

#top frame
frmTop = tk.Frame(root, borderwidth = 5, relief = 'raised', bg = '#BBADE6')
frmTop.grid(row=0, column = 0, columnspan = 3, sticky = 'nesw')
lblProfile = tk.Label(frmTop, text = 'Profile', font = ('Alata', 16, 'bold'), bg = '#BBADE6')
lblProfile.grid(row=0, column = 0, columnspan = 4, sticky = 'nesw')
imagee3 = ImageTk.PhotoImage(Image.open('profile.jpg'))
lblPerson = tk.Label(frmTop, text = 'User:\n'+ backend.function_read(0), width = 25, font =('Alata'), justify = tk.LEFT, bg = '#BBADE6')
lblPerson.grid(row = 1, column = 1, sticky = 'NW')
lblEmail = tk.Label(frmTop, text = 'Email:\n' + backend.function_read(1), width = 25, font =('Alata'), justify = tk.LEFT, bg = '#BBADE6')
lblEmail.grid(row = 1, column = 2, sticky = 'NW')
lblContact = tk.Label(frmTop, text = 'Phone Number:\n+12896892188', font =('Alata'), justify = tk.LEFT, width = 25, bg = '#BBADE6')
lblContact.grid(row = 1, column = 3, sticky = 'NW')
style = ttk.Style()
style.theme_use('clam')
style.configure('blue.Horizontal.TProgressbar', foreground = 'white', background = "#ADBCE6")
proLevel = ttk.Progressbar(frmTop, orient = tk.HORIZONTAL, style = 'blue.Horizontal.TProgressbar', length = 100, value = (backend.function_read(3)%1)*100, mode = 'determinate')
proLevel.grid(row = 2, column = 1, columnspan = 2, sticky = 'nesw')
lblLevel = tk.Label(frmTop, text = 'Level: ' + str(round(backend.function_read(3), 2)), width = 22, font =('Alata'), bg = '#BBADE6')
lblLevel.grid(row = 2, column = 0, sticky = 'nesw')
lblExp = tk.Label(frmTop, text = 'Exp Left to Level Up: ' + str(round((1-backend.function_read(3)%1)*100, 2)), font =('Alata'), bg = '#BBADE6')
lblExp.grid(row = 2, column = 3, sticky = 'nesw')
lblIcon = tk.Label(frmTop, image = imagee3, bg = '#BBADE6')
lblIcon.grid(row = 1 , column = 0, sticky = 'W', pady = 5)

#left frame
frmLeft = tk.Frame(root, borderwidth = 5, relief = 'sunken', bg = '#BBADE6')
frmLeft.grid(row=1, column = 0, sticky = 'nesw')
lblTDL = tk.Label(frmLeft, text = 'To Do List', bg = '#BBADE6', font = ('Alata', 16, 'bold'))
lblTDL.grid(row=0, column = 0)
frmTDL = tk.Frame(frmLeft, borderwidth = 5, relief = 'sunken', bg = '#BBADE6')
frmTDL.grid(row=1, column = 0, sticky = 'nesw')
lboTask = tk.Listbox(frmTDL, width = 30, height = 10, font = 'Alata', bg = 'white')
lboTask.pack(side=tk.LEFT, fill = tk.BOTH)

f = open('tasks.txt', 'rt')
lstTask = []
for line in f:
    lstTask.append(line)
    lboTask.insert(tk.END, line)

sb = tk.Scrollbar(frmTDL)
sb.pack(side = tk.RIGHT, fill = tk.BOTH)

lboTask.config(yscrollcommand = sb.set)
sb.config(command = lboTask.yview)



frmButton = tk.Frame(frmLeft, bg = '#BBADE6')
frmButton.grid(row = 2, column = 0)

entTask = tk.Entry(frmButton, bg = '#ADBCE6')
entTask.grid(row = 0, column = 0, columnspan = 2, sticky = 'nesw', pady = 5)
btnAdd = tk.Button(frmButton, text = 'Add Task', padx = 10, pady = 5, font =('Alata', 12), bg = '#ADBCE6', command = newTask)
btnAdd.grid(row = 1, column = 0, sticky = 'nesw')
btnDel = tk.Button(frmButton, text = 'Completed Task', padx = 10, pady = 5, font =('Alata', 12), bg = '#ADBCE6', command = deleteTask)
btnDel.grid(row = 1, column = 1, sticky = 'nesw')

frmStudy = tk.Frame(frmLeft, bg = '#BBADE6')
frmStudy.grid(row = 3, column = 0, pady = 10)

tk.Label(frmStudy, text= "Popular Study Techniques", font=('Alata 16 bold'), bg = '#BBADE6').grid(row=1,column=1,columnspan=3, pady = 5) 
#study technique buttons
TechniqueButton1 = tk.Button(frmStudy, text="SQ3R",width=15, bg = '#ADBCE6',command=SQ3R_popup).grid(row=2, column=1)
TechniqueButton2 = tk.Button(frmStudy, text="Retrieval Practice",width=15, bg = '#ADBCE6',command=Retrieval_popup).grid(row=2, column=2)
TechniqueButton3 = tk.Button(frmStudy, text="Spaced Practice",width=15, bg = '#ADBCE6',command=Spaced_popup).grid(row=2, column=3)
TechniqueButton4 = tk.Button(frmStudy, text="PQ4R",width=15, bg = '#ADBCE6',command=PQ4R_popup).grid(row=3, column=1)
TechniqueButton5 = tk.Button(frmStudy, text="Feynman Technique",width=15, bg = '#ADBCE6',command=Feynman_popup).grid(row=3, column=2)
TechniqueButton6 = tk.Button(frmStudy, text="Leitner System",width=15, bg = '#ADBCE6', command=Leitner_popup).grid(row=3, column=3)
TechniqueButton7 = tk.Button(frmStudy, text="Color-Coded Notes",width=15, bg = '#ADBCE6',command=Color_popup).grid(row=4, column=1)
TechniqueButton8 = tk.Button(frmStudy, text="Mind Mapping",width=15, bg = '#ADBCE6',command=Mapping_popup).grid(row=4, column=2)
TechniqueButton9 = tk.Button(frmStudy, text="Exercise Before Studying",width=15, bg = '#ADBCE6',command=Exercise_popup).grid(row=4, column=3)



#middle frame
frmMiddle = tk.Frame(root, borderwidth = 5, relief = 'sunken', bg = '#BBADE6')
frmMiddle.grid(row=1, column = 1, sticky = 'nesw')
#productive set
frmProd = tk.Frame(frmMiddle, width = 200, height = 100, borderwidth = 5, relief = 'ridge', bg = '#BBADE6')
frmProd.grid(row = 0, column = 0, sticky = 'nesw')
lblProductivity = tk.Label(frmProd, text = 'Productivity!', bg = '#BBADE6', font = ('Alata', 16, 'bold'))
lblProductivity.grid(row = 0, column = 0, columnspan = 4)
lblProd = tk.Label(frmProd, text = 'Set a timer - how productive are you feeling?', bg = '#BBADE6', font=("Alata"))
lblProd.grid(row = 1, column = 0, columnspan = 4, pady = 10)
entProdHour = tk.Entry(frmProd, bg = '#ADBCE6')
entProdHour.grid(row=2, column=1, sticky = 'nesw', pady = 10, padx = 10)
entProdMin = tk.Entry(frmProd, bg = '#ADBCE6')
entProdMin.grid(row=2, column=2, sticky = 'nesw', pady = 10, padx = 10)

lblProdHour = tk.Label(frmProd, text = 'hours', font =('Alata',10), bg = '#BBADE6')
lblProdHour.grid(row=3, column = 1, sticky = 'nesw')
lblProdMin = tk.Label(frmProd, text = 'mins', font =('Alata',10), bg = '#BBADE6')
lblProdMin.grid(row=3, column = 2, sticky = 'nesw')

lblEmpty = tk.Label(frmProd, width = 5, bg = '#BBADE6')
lblEmpty.grid(row=2, column = 0, pady = 10)
lblEmpty2 = tk.Label(frmProd, width = 5, bg = '#BBADE6')
lblEmpty2.grid(row=2, column = 3, pady = 10)

lblBreak = tk.Label(frmProd, text = 'How long would you like your break to be?', font ='Alata', width = 46, bg = '#BBADE6')
lblBreak.grid(row=4, column = 0, columnspan = 4,  sticky = 'nesw', pady = 10)
entBreakHour = tk.Entry(frmProd, width = 5, bg = '#ADBCE6')
entBreakHour.grid(row=5, column=1, sticky = 'nesw', pady = 10, padx = 10)
entBreakMin = tk.Entry(frmProd, width = 5, bg = '#ADBCE6')
entBreakMin.grid(row=5, column=2, sticky = 'nesw', pady = 10, padx = 10)

lblBreakHour = tk.Label(frmProd, text = 'hours', font =('Alata',10), bg = '#BBADE6')
lblBreakHour.grid(row=6, column = 1, sticky = 'nesw')
lblBreakMin = tk.Label(frmProd, text = 'mins', font =('Alata',10), bg = '#BBADE6')
lblBreakMin.grid(row=6, column = 2, sticky = 'nesw')

btnProd = tk.Button(frmProd, text='Start Study Period', bg = '#ADBCE6', font =('Alata', 12), command = function_prod)
btnProd.grid(row=7, column=0, columnspan = 2, sticky = 'nesw', pady = 10, padx = 2)
btnEnd = tk.Button(frmProd, text = 'End Productivity >:(', state = 'disabled', font =('Alata', 12), bg = '#ADBCE6', command = function_end)
btnEnd.grid(row=7, column=2, columnspan = 2, sticky = 'nesw', pady = 10, padx = 2)


#reminder set
frmRem = tk.Frame(frmMiddle, width = 200, height = 100, borderwidth = 5, relief = 'ridge', bg = '#BBADE6')
frmRem.grid(row = 1, column = 0, sticky = 'nesw')
#water & posture
varWater = tk.IntVar()
varPosture = tk.IntVar()
varMessage = tk.IntVar()
chkWater = tk.Checkbutton(frmRem, text = 'Water Reminder', font ='Alata', variable = varWater, bg = '#BBADE6')
chkWater.grid(row=0, column= 0)
chkPosture = tk.Checkbutton(frmRem, text = 'Posture Reminder', font ='Alata', variable = varPosture, bg = '#BBADE6')
chkPosture.grid(row=1, column=0)
chkMessage = tk.Checkbutton(frmRem, text = 'Text Reminder', font ='Alata', variable = varMessage, bg = '#BBADE6')
chkMessage.grid(row=2, column=0)
lblWater = tk.Label(frmRem, text = 'Reminder Frequency (mins):', font ='Alata', bg = '#BBADE6')
lblWater.grid(row=0, column = 1)
lblPosture = tk.Label(frmRem, text = 'Reminder Frequency (mins):', font ='Alata', bg = '#BBADE6')
lblPosture.grid(row=1, column = 1)
lblMessage = tk.Label(frmRem, text = 'Phone Number (Add +1)', font ='Alata', bg = '#BBADE6')
lblMessage.grid(row=2, column = 1)
entWater = tk.Entry(frmRem, width = 5, bg = '#ADBCE6')
entWater.grid(row=0, column = 2)
entPosture = tk.Entry(frmRem, width = 5, bg = '#ADBCE6')
entPosture.grid(row=1, column=2)
entMessage = tk.Entry(frmRem, width = 10, bg = '#ADBCE6')
entMessage.grid(row=2, column=2)

frmMisc = tk.Frame(frmMiddle, width = 200, height = 100, borderwidth = 5, relief = 'ridge', bg = '#BBADE6')
frmMisc.grid(row=2, column = 0, sticky = 'nesw')
lblMisc = tk.Label(frmMisc, text = 'Miscellaneous Settings', font =('Alata', 16, 'bold'), bg = '#BBADE6')
lblMisc.grid(row=0, column = 0, columnspan = 2, sticky = 'nesw')
btnStor = tk.Button(frmMisc, text = 'Statistics', bg = '#ADBCE6', width = 16, font =('Alata', 12), command = function_stats_button)
btnStor.grid(row=1, column = 0, padx = 5)
btnQuit = tk.Button(frmMisc, text = 'Quit', bg = '#ADBCE6', width = 16, font =('Alata', 12, 'bold'), command = root.destroy)
btnQuit.grid(row=1, column = 2, padx = 5)   
btnTheme = tk.Button(frmMisc, text = 'Themes', bg = '#ADBCE6', width = 16, font =('Alata', 12), command = root.destroy)
btnTheme.grid(row=1, column = 1, padx = 5)

frmRight = tk.Frame(root, borderwidth = 5, relief = 'sunken', bg = '#BBADE6')
frmRight.grid(row=1, column=2, sticky = 'nesw')
btnSpotify = tk.Button(frmRight, text = 'Play', font =('Alata',12), command = function_Spotify_button, width = 20, bg = '#ADBCE6')
btnSpotify.grid(row=1, column=0, pady = 10)
lblSpotify = tk.Label(frmRight, text = 'Spotify\'s Top 5 Playlists Right Now', font =('Alata', 14, 'bold'), width = 30, bg = '#BBADE6')
lblSpotify.grid(row=0, column=0, pady = 5)
frmRR = tk.Frame(frmRight)
frmRR.grid(row=2, column=0, pady = 5)
v = tk.StringVar(frmRR, '1')

stor = backend.spotify_playlists()
lstPlaylists = str(stor[0]).split(', ')
lstDescriptions = str(stor[1]).split(', ')
lstLink = str(stor[2]).split(', ')

for i in range(len(lstPlaylists)):
        lstPlaylists[i] = lstPlaylists[i].strip('"')
        lstPlaylists[i] = lstPlaylists[i].strip("'")
        lstPlaylists[i] = lstPlaylists[i].replace("{'", "")
        lstPlaylists[i] = lstPlaylists[i].replace("'}", "")
        
values = {lstPlaylists[0] : "0",
          lstPlaylists[1] : "1",
          lstPlaylists[2] : "2",
          lstPlaylists[3] : "3",
          lstPlaylists[4] : "4"}

for (text, value) in values.items():
    tk.Radiobutton(frmRR, text = text, variable = v, value = value, indicator = 0, font =('Alata', 12), bg = '#ADBCE6').pack(fill= tk.X)

frmSocials = tk.Frame(frmRight, bg = '#BBADE6')
frmSocials.grid(row=3, column = 0, pady = 5)
lblSocials = tk.Label(frmSocials, text = 'Connect with like-minded students\nduring your break', font = ('Atlata', 16, 'bold'), bg = '#BBADE6')
lblSocials.grid(row=0, column = 0, pady = 0)
imagee4 = ImageTk.PhotoImage(Image.open('socials.png'))
lblSocialsImage = tk.Label(frmSocials, image = imagee4, font = ('Atlata', 16, 'bold'), bg = '#BBADE6')
lblSocialsImage.grid(row=1, column = 0, pady = 0)
lblSocials.grid_forget()
lblSocialsImage.grid_forget()
root.mainloop()
