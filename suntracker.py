#!/usr/bin/env python3
# coding: latin-1

#Import library functions we need
import PicoBorgRev
from time import sleep
from pysolar.solar import *
import datetime
import time
from tkinter import*
from threading import Thread
import microstacknode.hardware.gps.l80gps as mst
gps=mst.L80GPS()
window=Tk()

# Tell the system how to drive the stepper
sequence = [[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]] # Order for stepping 
stepDelay = 0.002                                               # Delay between steps

# Name the global variables here:
global step
global PBR

#Setup the PicoBorg Reverse here:
PBR = PicoBorgRev.PicoBorgRev()
PBR.i2cAddress = 0x44                   # Uncomment and change the value if you have changed the board address
PBR.Init()



#add varibles here:
step = -1
#highlight thickness
ht=3
#colour
colour="blue"
#text colour
tc="white"
#background colour
bg="light green"


#setting up window here:
window.title("Stepper control")
global end
end = 1
varible=StringVar(window)
varible.set("auto")
window.geometry("500x500+700+200")
window.configure(background=bg)

#add functions here:
def MoveStep(count):
    global step
    global PBR

    # Choose direction based on sign (+/-)
    if count < 0:
        dir = -1
        count *= -1
    else:
        dir = 1

    # Loop through the steps
    while count > 0:
        # Set a starting position if this is the first move
        if step == -1:
            drive = sequence[-1]
            PBR.SetMotor1(drive[0])
            PBR.SetMotor2(drive[1])
            step = 0
        else:
            step += dir

        # Wrap step when we reach the end of the sequence
        if step < 0:
            step = len(sequence) - 1
        elif step >= len(sequence):
            step = 0

        # For this step set the required drive values
        if step < len(sequence):
            drive = sequence[step]
            PBR.SetMotor1(drive[0])
            PBR.SetMotor2(drive[1])
        sleep(stepDelay)
        count -= 1
def auto():
    end=False
    print("Please point the umbrella to south. This program will start in 10 seconds.")
    sleep(10)

    # Start by turning all drives off
    PBR.MotorsOff()
    # Loop forever
    oldc=0
    proc=0
    g=gps.get_gpgll()
    while True:
        
        d=datetime.datetime.now()
        a=get_azimuth(g['latitude'], g['longitude'], d)
        c=a/1.8
        print(str(round(c))+'  '+str(round(a)))
        proc=c-oldc
        steps = int(round(proc))
        oldc=round(c)
        if varible.get() == "manuel":
            end = True
            
        elif varible.get() == "auto":
            end == False
            
        if (end == True):
            
            PBR.MotorsOff()
            print("ended")
            break
        
        else:
            MoveStep(steps)
            sleep(4)
            PBR.MotorsOff()
            sleep(56)
        # Move the specified amount of steps
           
            
            
def manuel1():
    MoveStep(20)
def manuel2():
    MoveStep(-20)
    
def gget():
    #print(varible.get())
    gget2=varible.get()
    if gget2 == "auto":
        thread1()
    else:
        manual()

def thread1():
    threads = []
    t1=Thread(target=auto)
    t1.start()
    b.place(relx=0.5,rely=0.05,anchor=CENTER)
    l.place(relx=0.5,rely=0.15,anchor=CENTER)
    bt.place(relx=0.5,rely=0.25,anchor=CENTER)
    l2.place_forget()
    bt2.place_forget()
    bt3.place_forget()
    bt5.place_forget()
    s.place_forget()
    e.place_forget()
    bt6.place_forget()


  
def manual():
    global end
    end=True
    l2.place(relx=0.5,rely=0.4,anchor=CENTER)
    bt2.place(relx=0.5,rely=0.5,anchor=CENTER)
    bt3.place(relx=0.5,rely=0.6,anchor=CENTER)
    bt5.place(relx=0.5,rely=0.8,anchor=CENTER)
    s.place(relx=0.5,rely=0.7,anchor=CENTER)
    e.place(relx=0.5,rely=0.9,anchor=CENTER)
    bt6.place(relx=0.5,rely=0.95,anchor=CENTER)
 
def close():
    exit()
    
   
def movespef():
    v=int(s.get())
    MoveStep(v)

def confirm():
    v2=int(e.get())
    if v2 > int(500):
        e.delete(0,END)
        e.insert(0,"0")
        print("too high")
    elif v2 < int(-500):
        e.delete(0,END)
        e.insert(0,"0")
        print("too low")
    else:
        e.delete(0,END)
        e.insert(0,"0")
        MoveStep(v2)

def stop():
    if varible.get() == "auto":
        print("cant do that")
    else:
        PBR.MotorsOff()

def clock():
    while True:
        t=time.asctime(time.localtime(time.time()))
        l3.pack_forget()
        l3.config(text=t)
        l3.place(relx=0.8,rely=0.1,anchor=CENTER)
              

l3=Label(window,text="hello",fg=tc,bg=colour)
l3.place(relx=0.8,rely=0.1,anchor=CENTER)

threads2=[]
t2=Thread(target=clock)
t2.start()


#add auto/buttons at top here:                   
b=OptionMenu(window,varible,"auto","manuel")
b.place(relx=0.5,rely=0.05,anchor=CENTER)

l=Label(window,text="Auto or Manual",bg=colour,fg=tc)
l.place(relx=0.5,rely=0.15,anchor=CENTER)

bt=Button(window,text="press to confirm",command=gget,highlightbackground=colour,highlightthickness=ht)
bt.place(relx=0.5,rely=0.25,anchor=CENTER)

#add manuel controlls here:
l2=Label(window,text="----------------------------Manual controls----------------------------",bg=colour,fg=tc)
l2.place(relx=0.5,rely=0.4,anchor=CENTER)

bt2=Button(window,text="forwards",command=manuel1,highlightbackground=colour,highlightthickness=ht)
bt2.place(relx=0.5,rely=0.5,anchor=CENTER)

bt3=Button(window,text="back",command=manuel2,highlightbackground=colour,highlightthickness=ht)
bt3.place(relx=0.5,rely=0.6,anchor=CENTER)

s = Scale(window,from_=-100,to=100,orient=HORIZONTAL,highlightbackground=colour,highlightthickness=ht)
s.place(relx=0.5,rely=0.7,anchor=CENTER)

bt5=Button(window,command=movespef,text="move steps",highlightbackground=colour,highlightthickness=ht)
bt5.place(relx=0.5,rely=0.8,anchor=CENTER)

e=Entry(window,bg="red",highlightbackground=colour,highlightthickness=ht)
e.place(relx=0.5,rely=0.9,anchor=CENTER)
e.insert(0,"0")

bt6=Button(window,text="confirm",command=confirm,highlightbackground=colour,highlightthickness=ht)
bt6.place(relx=0.5,rely=0.95,anchor=CENTER)

#~~~~~~~~~~~~~~~~~~~~~~#
menu = Menu(window,bg=colour,fg=tc)
sub = Menu(menu, tearoff=False)
sub2 = Menu(menu, tearoff=False)

#add menu options here:
sub.add_command(label="Stop All",command=stop)
sub.add_command(label="Exit",command=close)


#add more menus here:
menu.add_cascade(label="Menu", menu=sub)
window.config(menu=menu)


#add place_forget here:
s.place_forget()
bt5.place_forget()
e.place_forget()
bt6.place_forget()
l2.place_forget()
bt2.place_forget()
bt3.place_forget()
mainloop()
