from tkinter import *
import tkinter.messagebox
from pygame import mixer
mixer.init()
import webbrowser
import threading
from tkinter import ttk
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
import time


player = Tk()
player.title("DHUNN")
player.iconbitmap(r"my_icon.ico")
player.geometry("500x400")
player.configure(bg="white")


def About_Dhunn():
    tkinter.messagebox.showinfo("About Dhunn", "Hello User! This is Dhunn Version.1.0.20.\nThis is just a Music Player interface based on tkinter.\nFor creator info seek into Contact Us.\n(c) 2019-20 Nitin_Singh Inc.")

def Contact_Us():
    webbrowser.open("https://www.instagram.com/_nitinks_/")

def Browse_Song():
    global song_file
    Stop()
    time.sleep(1)
    song_file = filedialog.askopenfilename()
    mixer.music.load(song_file)
    mixer.music.play()

def Details():
    file_data = os.path.splitext(song_file)

    if file_data[1]==".mp3":
        audio = MP3(song_file)
        total_length= audio.info.length
    else:
        a = mixer.Sound(song_file)
        total_length = a.get_length()

    mins, secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    Song_length['text']= "Total Length - "+ timeformat

    t1 = threading.Thread(target=Count_down,args=(total_length,))
    t1.start()

def Count_down(t):
    global paused
    x= 0
    while x<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(x,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            Current_length['text']= "Current Length - "+ timeformat
            time.sleep(1)
            x+=1

def Play():
    try:
        Browse_Song()
        Sbar['text']= "Playing..."
        Song_name["text"]= os.path.basename(song_file)
        Details()
    except Exception:
        tkinter.messagebox.showerror("No Selection Error","No selected song! Please select a song")

paused = FALSE
def Pause():
    global paused
    if paused:
        mixer.music.unpause()
        Sbar['text']= "Resumed!"
        paused = FALSE
    else:
        mixer.music.pause()
        Sbar['text']= "Paused!"
        paused = TRUE

def Stop():
    mixer.music.stop()
    Sbar['text']= "Stopped!!"

def Rewind():
    mixer.music.load(song_file)
    mixer.music.play()
    Sbar['text']= "Rewinded...!!"

def Volume(val):
    vol = float(val)/100
    mixer.music.set_volume(vol)

muted = FALSE
def Mute():
    global muted
    if muted:
        scale.set(60)
        mixer.music.set_volume(0.6)
        Unmute_btn.config(image= unmute_image)
        muted = FALSE
        tkinter.messagebox.showinfo("Volume", "Volume Unmuted!")
    else:
        scale.set(0)
        mixer.music.set_volume(0)
        Unmute_btn.config(image= mute_image)
        muted = TRUE
        tkinter.messagebox.showinfo("Volume", "Volume Muted!")

def Close():
    Msg_box = tkinter.messagebox.askquestion("Exit!","Do you really want to leave us?")
    if Msg_box == "yes":
        Stop()
        player.destroy()
    else:
        pass


main_menu = Menu(player)
player.config(menu= main_menu)


sub_menu = Menu(main_menu,tearoff =0)
main_menu.add_cascade(label= "File", menu= sub_menu)
sub_menu.add_command(label = "Add Song", command = Browse_Song)
sub_menu.add_command(label = "Play", command= Play)
sub_menu.add_command(label = "Pause/Resume", command= Pause)
sub_menu.add_command(label = "Stop", command= Stop)
sub_menu.add_command(label = "Exit", command= player.destroy)

sub_menu = Menu(main_menu,tearoff =0)
main_menu.add_cascade(label= "Help", menu= sub_menu)
sub_menu.add_command(label = "About Dhunn", command= About_Dhunn)
sub_menu.add_command(label = "Contact Us",command= Contact_Us)


Tag_line = Label(player, text="Beat-up with 'Dhunn'", font='Garamond 25 bold', 
                                fg='black', bg='white', height=1, width=45)
Tag_line.pack()

Song_name = Label(player, text="", font=('Garamond',10), 
                                fg='black', bg='white', height=1, width=80)
Song_name.pack()

Song_length = ttk.Label(player, text = "Total Length - 00:00")
Song_length.pack()

Current_length = ttk.Label(player, text = "Current Length - 00:00")
Current_length.pack()

Alignment = Frame(player)
Alignment.pack(pady=10)

BAlignment= Frame(player)
BAlignment.pack(pady=10)

play_image = PhotoImage(file= "play.png")
pause_image = PhotoImage(file= "pause_resume.png")
stop_image = PhotoImage(file= "stop.png")
rewind_image = PhotoImage(file= "rewind.png")

Play_btn = ttk.Button(Alignment, image = play_image, command = Play)
Play_btn.grid(row=0, column=0, padx= 10, pady=10)
Pause_btn = ttk.Button(Alignment, image = pause_image, command = Pause)
Pause_btn.grid(row=0, column=1, padx= 10, pady=10)
Stop_btn = ttk.Button(Alignment, image = stop_image, command = Stop)
Stop_btn.grid(row=0, column=2, padx= 10, pady=10)
Rewind_btn = ttk.Button(Alignment, image = rewind_image, command = Rewind)
Rewind_btn.grid(row=0, column=3, padx= 10, pady=10)


mute_image = PhotoImage(file= "mute.png")
unmute_image = PhotoImage(file= "unmute.png")

Unmute_btn = ttk.Button(BAlignment, image = unmute_image, command= Mute)
Unmute_btn.grid(row=0, column=1, padx= 10, pady=10)


scale = ttk.Scale(BAlignment, from_=0, to=100, orient=HORIZONTAL, command= Volume)
scale.set(60)
mixer.music.set_volume(0.6)
scale.grid(row=0, column=2, padx= 10, pady=10)


Sbar = ttk.Label(player, text="Welcome to Dhunn!!", relief_= SUNKEN, anchor= W, font='Garamond 15 italic')
Sbar.pack(side=BOTTOM, fill=X)


player.protocol("WM_DELETE_WINDOW", Close)
player.mainloop()