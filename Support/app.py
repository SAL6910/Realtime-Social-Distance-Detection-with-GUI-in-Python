from os import truncate
from tkinter import *
from tkinter import tix
import tkinter
from typing import NoReturn
from Support.functions import start
from Support import social_distancing_config as config
from PIL import Image, ImageTk
import PIL.Image
from tkinter import messagebox
from tkinter.tix import *
from urllib.parse import urlparse
import re
from Support.loadstream import LoadingSplash
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import cv2
import time
import Pmw
import sys
from fpdf import FPDF
import pandas as pd
import webbrowser
from tkinter import ttk
import socket
process = 0
process1=0

regexURL = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  #to check whether url is correct

regexIP = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

def MainPage():
    w = Tk()
    w.attributes("-fullscreen",True)
    w.state('zoomed')
    w.resizable(0,0)
    w.configure(bg='blue')
    w.title("CoviEYE")
    tip=Balloon(w)
    config.webcamworking=False
    

    def on_closing():
        w.attributes('-disabled',True)
        resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
        if resultquit=="yes":
            w.attributes('-disabled',False)
            w.destroy()
        else:
            w.attributes('-disabled',False)
        
        
    class Example(Frame):
        def __init__(self, master, *pargs):
            Frame.__init__(self, master, *pargs)
            self.image = PIL.Image.open("./Images/cctv.png")
            self.img_copy= self.image.copy()
            self.background_image = ImageTk.PhotoImage(self.image)
            self.background = Label(self, image=self.background_image)
            self.background.pack(fill=BOTH, expand=YES)
            self.background.bind('<Configure>', self._resize_image)
        
        def _resize_image(self,event):
            new_width = event.width
            new_height = event.height
            self.image = self.img_copy.resize((new_width, new_height))
            self.background_image = ImageTk.PhotoImage(self.image)
            self.background.configure(image =  self.background_image)

    e = Example(w)
    e.pack(fill=BOTH, expand=YES)

    def about():
        y1=Toplevel(w)
        y1.focus_set()
        y1.state('zoomed')
        y1.title("Credits")
        y1.attributes("-fullscreen",True)
        menubar = Menu(y1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Back", command=y1.withdraw)
        menubar.add_cascade(label="File", menu=filemenu)
        y1.config(menu=menubar)
        class Example(Frame):
            def __init__(self, master, *pargs):
                Frame.__init__(self, master, *pargs)
                self.image = PIL.Image.open("./Images/ABOUT.jpeg")
                self.img_copy= self.image.copy()
                self.background_image = ImageTk.PhotoImage(self.image)
                self.background = Label(self, image=self.background_image)
                self.background.pack(fill=BOTH, expand=YES)
                self.background.bind('<Configure>', self._resize_image)

            def _resize_image(self,event):
                new_width = event.width
                new_height = event.height
                self.image = self.img_copy.resize((new_width, new_height))
                self.background_image = ImageTk.PhotoImage(self.image)
                self.background.configure(image =  self.background_image)

        e = Example(y1)
        e.pack(fill=BOTH, expand=YES)

    def CUDASetup():
        w.attributes('-disabled',True)
        result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
        if result=="yes":
            webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
        else:
            pass
        w.attributes('-disabled',False)

    def SelectRenderer():
        w.withdraw()
        global x1
        x1=Toplevel(w)
        x1.focus_set()
        x1.overrideredirect(False)
        x1.attributes("-fullscreen",True)
        x1.state('zoomed')
        x1.resizable(0,0)
        x1.configure(bg='blue')
        e = Example(x1)
        e.pack(fill=BOTH, expand=YES)
        config.USE_GPU=False
        config.USE_CPU=False
        if os.path.exists("Converted/AllData-Converted.pdf"):
            os.remove("Converted/AllData-Converted.pdf")
        if os.path.exists("Converted/AllData-Converted.xlsx"):
            os.remove("Converted/AllData-Converted.xlsx")
     
        def CUDASetup():
            x1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            x1.attributes('-disabled',False)
            x1.focus_set()
        
        def on_closing():
            x1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                x1.attributes('-disabled',False)
                w.destroy()
            else:
                x1.attributes('-disabled',False)
                x1.focus_set()
                
        x1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            x1.withdraw()
            w.deiconify()
            w.state('zoomed')
            w.overrideredirect(False)

        menubar = Menu(x1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        x1.config(menu=menubar)

        def CPU():
            if(config.USE_CPU==True):
                x1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                x1.attributes('-disabled',False)
                x1.focus_set()
            else:
                x1.attributes('-disabled',True)
                messagebox.showinfo("Select CPU or GPU", "CPU is Selected.")
                x1.attributes('-disabled',False)
                x1.focus_set()
                config.USE_CPU=True
                config.USE_GPU=False
                gpuButton['state']=DISABLED
                nextButton['state']=NORMAL
            

        def GPU():
            def is_cuda_cv(): # 1 == using cuda, 0 = not using cuda
                try:
                    count = cv2.cuda.getCudaEnabledDeviceCount()
                    if count > 0:
                        return 1
                    else:
                        return 0
                except:
                    return 0

            if(is_cuda_cv()==1):
                if(config.USE_GPU==True):
                    x1.attributes('-disabled',True)
                    messagebox.showwarning("Warning", "Already Selected")
                    x1.attributes('-disabled',False)
                    x1.focus_set()
                else:
                    x1.attributes('-disabled',True)
                    messagebox.showinfo("Select CPU or GPU", "GPU is Selected.")
                    x1.attributes('-disabled',False)
                    x1.focus_set()
                    config.USE_GPU=True
                    config.USE_CPU=False
                    cpuButton['state']=DISABLED
                    nextButton['state']=NORMAL
            else:
                x1.attributes('-disabled',True)
                messagebox.showerror("Error", "CUDA not enabled for GPU on this device.")
                x1.attributes('-disabled',False)
                x1.attributes('-disabled',True)
                result = messagebox.askquestion("Setup", "Do you want to check the steps to setup CUDA? You will be redirected to an external webpage.")
                if result=="yes":
                    webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
                else:
                    pass
                x1.attributes('-disabled',False)
                x1.focus_set()
                config.USE_GPU=False
                config.USE_CPU=False
                cpuButton['state']=NORMAL
                gpuButton['state']=DISABLED
                nextButton['state']=DISABLED
                resetButton['state']=DISABLED

            
            
        labelMainImage=PhotoImage(file = r"Images/SELECT_CPU_OR_GPU.png")
        labelMainLabel=Label(x1,image=labelMainImage, compound = TOP)
        labelMainLabel.place(x=420, y = 100)
        labelMainLabel.image=labelMainImage
        cpuImage=PhotoImage(file = r"Images/CPU.png")
        cpuButton=Button(x1,image=cpuImage, compound = TOP,command=CPU,state=NORMAL)
        cpuButton.place(x=200,y=200)
        cpuButton.image=cpuImage
        tip.bind_widget(cpuButton,balloonmsg="This will use the machine processor for computation.")
        gpuImage=PhotoImage(file = r"Images/GPU.png")
        gpuButton=Button(x1,image=gpuImage, compound = TOP,command=GPU, state=NORMAL)
        gpuButton.place(x=900,y=200)
        gpuButton.image=gpuImage
        tip.bind_widget(gpuButton,balloonmsg="This will use the machine Graphics Card for computation.")
        
        def SwitchStateRender():
            if cpuButton['state']==NORMAL and gpuButton['state']==NORMAL:
                x1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "No option is selected!")
                x1.attributes('-disabled',False)
                x1.focus_set()
            else:
                config.USE_GPU=False
                config.USE_CPU=False
                cpuButton['state']=NORMAL
                gpuButton['state']=NORMAL
                nextButton['state']=DISABLED

        resetImage=PhotoImage(file = r"Images/RESET.png")
        resetButton=Button(x1,image=resetImage, compound = TOP,command=SwitchStateRender)
        resetButton.place(x=650,y=600)
        resetButton.image=resetImage
        tip.bind_widget(resetButton,balloonmsg="This will deselect the option.")
        nextImage=PhotoImage(file = r"Images/NEXT.png")
        nextButton=Button(x1,image=nextImage, compound = TOP,command=ChooseOption)
        nextButton.place(x=1250,y=700)
        nextButton.image=nextImage
        tip.bind_widget(nextButton,balloonmsg="This will proceed to the next page.")
        nextButton['state']=DISABLED
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(x1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")
        
    

    def CamSelect():
        if(config.USE_SOCIAL_DISTANCE==True):
            f1.withdraw()
        else:
            z1.withdraw()
        global y1
        y1=Toplevel(w)
        y1.focus_set()
        y1.overrideredirect(False)
        y1.attributes("-fullscreen",True)
        y1.state('zoomed')
        y1.resizable(0,0)
        y1.configure(bg='blue')
        e = Example(y1)
        e.pack(fill=BOTH, expand=YES)
        config.USE_MOBILE_CAMERA=False
        config.USE_DEVICE_CAMERA=False
        
        def CUDASetup():
            y1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            y1.attributes('-disabled',False)
            y1.focus_set()
        
        def on_closing():
            y1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                y1.attributes('-disabled',False)
                w.destroy()
            else:
                y1.attributes('-disabled',False)
                y1.focus_set()

        y1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            if(config.USE_SOCIAL_DISTANCE==True):
                y1.withdraw()
                f1.deiconify()
                f1.state('zoomed')
                f1.overrideredirect(False)
            else:  
                y1.withdraw()
                z1.deiconify()
                z1.state('zoomed')
                z1.overrideredirect(False)

        menubar = Menu(y1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        y1.config(menu=menubar)
        labelMainImageCamera=PhotoImage(file = r"Images/camera_select.png")
        labelMainLabelCamera=Label(y1,image=labelMainImageCamera, compound = TOP)
        labelMainLabelCamera.place(x=475, y = 100)
        labelMainLabelCamera.image=labelMainImageCamera 

        def DeviceCamera():
            cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            while(True):
                ret, frame = cap.read()
                if cap.isOpened():
                    config.webcamworking=True
                    break
                else:
                    config.webcamworking=False
                    break
            cap.release()
            cv2.destroyAllWindows()
            if(config.webcamworking==True):
                if(config.USE_DEVICE_CAMERA==True):
                    y1.attributes('-disabled',True)
                    messagebox.showwarning("Warning", "Already Selected")
                    y1.attributes('-disabled',False)
                    y1.focus_set()
                else:
                    y1.attributes('-disabled',True)
                    messagebox.showinfo("Select Camera", "Current device camera has been selected.")
                    y1.attributes('-disabled',False)
                    y1.focus_set()
                    config.USE_DEVICE_CAMERA=True
                    config.USE_MOBILE_CAMERA=False
                    MobileCameraButton['state']=DISABLED
                    DeviceCameraButton['state']=NORMAL
                    nextButton['state']=NORMAL
            else:
                y1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "No webcam found.")
                y1.attributes('-disabled',False)
                y1.focus_set()
                DeviceCameraButton['state']=DISABLED
                resetButton['state']=DISABLED
                   
        def MobileCamera():
            if(config.USE_MOBILE_CAMERA==True):
                y1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                y1.attributes('-disabled',False)
                y1.focus_set()
            else:
                y1.attributes('-disabled',True)
                messagebox.showinfo("Select Camera", "Mobile camera has been selected")
                y1.attributes('-disabled',False)
                y1.focus_set()
                config.USE_MOBILE_CAMERA=True
                config.USE_DEVICE_CAMERA=False
                DeviceCameraButton['state']=DISABLED
                MobileCameraButton['state']=NORMAL
                nextButton['state']=NORMAL

        def NextSwitch():
            if config.USE_DEVICE_CAMERA==True:
                WriteData()
            else:
                OSselect()

        DeviceCameraImage=PhotoImage(file = r"Images/DeviceCamera.png")
        DeviceCameraButton=Button(y1,image=DeviceCameraImage,command=DeviceCamera, compound = TOP,state=NORMAL)
        DeviceCameraButton.place(x=200,y=200)
        DeviceCameraButton.image=DeviceCameraImage
        tip.bind_widget(DeviceCameraButton,balloonmsg="This will select the camera device on this machine.")
        MobileCameraImage=PhotoImage(file = r"Images/MobileCamera.png")
        MobileCameraButton=Button(y1,image=MobileCameraImage,command=MobileCamera, compound = TOP, state=NORMAL)
        MobileCameraButton.place(x=900,y=200)
        MobileCameraButton.image=MobileCameraImage
        tip.bind_widget(MobileCameraButton,balloonmsg="This will select the mobile device camera.")

        def SwitchStateCamera():
            if DeviceCameraButton['state']==NORMAL and MobileCameraButton['state']==NORMAL:
                y1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "No option is selected!")   
                y1.attributes('-disabled',False)     
                y1.focus_set()    
            else:
                DeviceCameraButton['state']=NORMAL
                MobileCameraButton['state']=NORMAL
                nextButton['state']=DISABLED
                config.USE_DEVICE_CAMERA=False
                config.USE_MOBILE_CAMERA=False

        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(y1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")
        resetImage=PhotoImage(file = r"Images/RESET.png")
        resetButton=Button(y1,image=resetImage, compound = TOP,command=SwitchStateCamera)
        resetButton.place(x=650,y=600)
        resetButton.image=resetImage
        tip.bind_widget(resetButton,balloonmsg="This will deselect the option.")
        nextImage=PhotoImage(file = r"Images/NEXT.png")
        nextButton=Button(y1,image=nextImage, compound = TOP,command=NextSwitch)
        nextButton.place(x=1250,y=700)
        nextButton.image=nextImage
        tip.bind_widget(nextButton,balloonmsg="This will proceed to the next page.")
        nextButton['state']=DISABLED

     
    def OSselect():
        y1.withdraw()
        global u1
        u1=Toplevel(w)
        u1.focus_set()
        u1.overrideredirect(False)
        u1.attributes("-fullscreen",True)
        u1.state('zoomed')
        u1.resizable(0,0)
        u1.configure(bg='blue')
        e = Example(u1)
        e.pack(fill=BOTH, expand=YES)
        
        def CUDASetup():
            u1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            u1.attributes('-disabled',False)
            u1.focus_set()
        
        def on_closing():
            u1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                u1.attributes('-disabled',False)
                w.destroy()
            else:
                u1.attributes('-disabled',False)
                u1.focus_set()

        u1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            u1.withdraw()
            y1.deiconify()
            y1.state('zoomed')
            y1.overrideredirect(False)

        menubar = Menu(u1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        u1.config(menu=menubar)
        UserEntry = Entry(u1,width = 22,font=("default",40),justify='center')
        UserEntry.place(x = 435, y = 700)
        UserEntry.insert(0, "IP ADDRESS")
        UserEntry.configure(state=DISABLED)
        
        def on_click(event):
            UserEntry.configure(state=NORMAL)
            UserEntry.delete(0, END)
            UserEntry.unbind('<Button-1>', on_click_id)

        on_click_id = UserEntry.bind('<Button-1>', on_click)
        titleImage=PhotoImage(file = r"Images/STEPS_TO_SETUP.png")
        titleLabel=Label(u1,image=titleImage, compound = TOP)
        titleLabel.place(x=450, y = 10)
        titleLabel.image=titleImage
        descImage=PhotoImage(file=r"Images/IP_Webcam.png")
        descLabel=Label(u1,image=descImage, compound = TOP) 
        descLabel.place(x=180, y = 85)
        descLabel.image=descImage

        def IPAddress():
            addr=UserEntry.get()
            if(re.match(regexURL, addr) is not None):
                parsed = urlparse(addr)
                IP=parsed.hostname
                if(re.search(regexIP,IP)):
                    try:
                        PORT=parsed.port	
                        sideAddress="/video"
                        global completeAddress
                        completeAddress=addr+sideAddress
                        config.IP_WEBCAM_ADDRESS=completeAddress
                        UserEntry.delete(0,'end')
                        UserEntry.insert(0, "IP ADDRESS")
                        UserEntry.configure(state=DISABLED)
                        h1="URL: "
                        h2=h1+addr+" set successfully."
                        u1.attributes('-disabled',True)
                        messagebox.showinfo("Information",h2)	
                        u1.attributes('-disabled',False)
                        u1.focus_set()
                        nextButton['state']=NORMAL
                        on_click_id = UserEntry.bind('<Button-1>', on_click)
                    except ValueError:
                        UserEntry.delete(0,'end')
                        UserEntry.insert(0, "IP ADDRESS")
                        UserEntry.configure(state=DISABLED)
                        nextButton['state']=DISABLED
                        u1.attributes('-disabled',True)
                        messagebox.showwarning("Warning","PORT number Invalid.")	
                        u1.attributes('-disabled',False)
                        u1.focus_set()
                        on_click_id = UserEntry.bind('<Button-1>', on_click)                  
                else:
                    UserEntry.delete(0,'end')
                    UserEntry.insert(0, "IP ADDRESS")
                    UserEntry.configure(state=DISABLED)
                    nextButton['state']=DISABLED
                    u1.attributes('-disabled',True)
                    messagebox.showwarning("Warning","IP Address Invalid")
                    u1.attributes('-disabled',False)
                    u1.focus_set()
                    on_click_id = UserEntry.bind('<Button-1>', on_click)
            else:
                UserEntry.delete(0,'end')
                UserEntry.insert(0, "IP ADDRESS")
                UserEntry.configure(state=DISABLED)
                u1.attributes('-disabled',True)
                messagebox.showwarning("Warning","URL Invalid")
                u1.attributes('-disabled',False)
                u1.focus_set()
                on_click_id = UserEntry.bind('<Button-1>', on_click)  

        setImage=PhotoImage(file = r"Images/SET.png")
        setButton=Button(u1,image=setImage, compound = TOP,command=IPAddress)
        setButton.place(x=675,y=770)
        setButton.image=setImage
        tip.bind_widget(setButton,balloonmsg="This will set the Maximum number of Persons.")
        nextImage=PhotoImage(file = r"Images/NEXT.png")
        nextButton=Button(u1,image=nextImage, compound = TOP,command=WriteData)
        nextButton.place(x=1250,y=700)
        nextButton.image=nextImage
        tip.bind_widget(nextButton,balloonmsg="This will proceed to the next page.")
        nextButton['state']=DISABLED
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(u1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")


    def ChooseOption():
        x1.withdraw()
        global f1
        f1=Toplevel(w)
        f1.focus_set()
        f1.overrideredirect(False)
        f1.attributes("-fullscreen",True)
        f1.state('zoomed')
        f1.resizable(0,0)
        f1.configure(bg='blue')
        e = Example(f1)
        e.pack(fill=BOTH, expand=YES)
        config.USE_SOCIAL_DISTANCE=False
        config.USE_HUMAN_COUNT=False
        config.USE_BOTH=False
        
        def CUDASetup():
            f1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            f1.attributes('-disabled',False)
            f1.focus_set()
        
        def on_closing():
            f1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                f1.attributes('-disabled',False)
                w.destroy()
            else:
                f1.attributes('-disabled',False)
                f1.focus_set()

        f1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            f1.withdraw()
            x1.deiconify()
            x1.state('zoomed')
            x1.overrideredirect(False)

        menubar = Menu(f1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        f1.config(menu=menubar)
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(f1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")

        def SocialDistance():
            if(config.USE_SOCIAL_DISTANCE==True):
                f1.attributes('-disabled',True)
                messagebox.showwarning("Warning","Already Selected")
                f1.attributes('-disabled',False)
                f1.focus_set()
            else:
                f1.attributes('-disabled',True)
                messagebox.showinfo("Select Functionality","Social Distancing Only Enabled.")
                f1.attributes('-disabled',False)
                f1.focus_set()
                config.USE_SOCIAL_DISTANCE=True
                config.USE_BOTH=False
                config.USE_HUMAN_COUNT=False
                HumanCountButton['state']=DISABLED
                BothButton['state']=DISABLED
                nextButton['state']=NORMAL	

        def HumanCount():
            if(config.USE_HUMAN_COUNT==True):
                f1.attributes('-disabled',True)
                messagebox.showwarning("Warning","Already Selected")
                f1.attributes('-disabled',False)
                f1.focus_set()
            else:
                f1.attributes('-disabled',True)
                messagebox.showinfo("Select Functionality","Realtime Human Count Only Enabled.")
                f1.attributes('-disabled',False)
                f1.focus_set()
                config.USE_SOCIAL_DISTANCE=False
                config.USE_BOTH=False
                config.USE_HUMAN_COUNT=True
                SocialDButton['state']=DISABLED
                BothButton['state']=DISABLED
                nextButton['state']=NORMAL
        
        def Both():
            if(config.USE_BOTH==True):
                f1.attributes('-disabled',True)
                messagebox.showwarning("Warning","Already Selected")
                f1.attributes('-disabled',False)
                f1.focus_set()
            else:
                f1.attributes('-disabled',True)
                messagebox.showinfo("Select Functionality","Both Social Distancing and Realtime Human Count Enabled.")
                f1.attributes('-disabled',False)
                f1.focus_set()
                config.USE_SOCIAL_DISTANCE=False
                config.USE_BOTH=True
                config.USE_HUMAN_COUNT=False
                SocialDButton['state']=DISABLED
                HumanCountButton['state']=DISABLED
                nextButton['state']=NORMAL

        
        def switchFunc():
            if(config.USE_SOCIAL_DISTANCE==True):
                CamSelect()
            else:
                MaxPerson()

        def SwitchStateRender():
            if SocialDButton['state']==NORMAL and HumanCountButton['state']==NORMAL and BothButton['state']==NORMAL:
                f1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "No option is selected!")
                f1.attributes('-disabled',False)
                f1.focus_set()
            else:
                SocialDButton['state']=NORMAL
                HumanCountButton['state']=NORMAL
                BothButton['state']=NORMAL
                nextButton['state']=DISABLED
                config.USE_SOCIAL_DISTANCE=False
                config.USE_BOTH=False
                config.USE_HUMAN_COUNT=False

        SocialDImage=PhotoImage(file = r"Images/Social_Distance.png")
        SocialDButton=Button(f1,image=SocialDImage, compound = TOP,command=SocialDistance,state=NORMAL)
        SocialDButton.place(x=100,y=200)
        SocialDButton.image=SocialDImage
        tip.bind_widget(SocialDButton,balloonmsg="Only Social Distance violations will be displayed.")
        HumanCountImage=PhotoImage(file = r"Images/Human_Count.png")
        HumanCountButton=Button(f1,image=HumanCountImage, compound = TOP,command=HumanCount, state=NORMAL)
        HumanCountButton.place(x=565,y=200)
        HumanCountButton.image=HumanCountImage
        tip.bind_widget(HumanCountButton,balloonmsg="Only Realtime Human Count will be displayed.")
        BothImage=PhotoImage(file = r"Images/BOTH.png")
        BothButton=Button(f1,image=BothImage, compound = TOP,command=Both, state=NORMAL)
        BothButton.place(x=1030,y=200)
        BothButton.image=BothImage
        tip.bind_widget(BothButton,balloonmsg="Both Social Distance and Human Count will be displayed.")
        resetImage=PhotoImage(file = r"Images/RESET.png")
        resetButton=Button(f1,image=resetImage, compound = TOP,command=SwitchStateRender)
        resetButton.place(x=650,y=675)
        resetButton.image=resetImage
        tip.bind_widget(resetButton,balloonmsg="This will deselect the option.")
        titleImage=PhotoImage(file = r"Images/SELECT_FUNCTIONALITY.png")
        titleLabel=Label(f1,image=titleImage, compound = TOP)
        titleLabel.place(x=415, y = 100)
        titleLabel.image=titleImage
        nextImage=PhotoImage(file = r"Images/NEXT.png")
        nextButton=Button(f1,image=nextImage, compound = TOP,command=switchFunc)
        nextButton.place(x=1250,y=700)
        nextButton.image=nextImage
        tip.bind_widget(nextButton,balloonmsg="This will proceed to the next page.")
        nextButton['state']=DISABLED


    def MaxPerson(): 
        f1.withdraw()
        global z1
        z1=Toplevel(w)
        z1.focus_set()
        z1.overrideredirect(False)
        z1.attributes("-fullscreen",True)
        z1.state('zoomed')
        z1.resizable(0,0)
        z1.configure(bg='blue')
        e = Example(z1)
        e.pack(fill=BOTH, expand=YES)
        
        def CUDASetup():
            z1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            z1.attributes('-disabled',False)
            z1.focus_set()
        
        def on_closing():
            z1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                z1.attributes('-disabled',False)
                w.destroy()
            else:
                z1.attributes('-disabled',False)
                z1.focus_set()

        z1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            z1.withdraw()
            f1.deiconify()
            f1.state('zoomed')
            f1.overrideredirect(False)
            

        nextImage=PhotoImage(file = r"Images/NEXT.png")
        nextButton=Button(z1,image=nextImage, compound = TOP,command=CamSelect)
        nextButton.place(x=1250,y=700)
        nextButton.image=nextImage
        tip.bind_widget(nextButton,balloonmsg="This will proceed to the next page.")
        nextButton['state']=DISABLED
        labelMain1Image=PhotoImage(file = r"Images/ENTER_MAX_NO_OF_PERSON.png")
        labelMain1Label=Label(z1,image=labelMain1Image, compound = TOP)
        labelMain1Label.place(x=280, y = 90)
        labelMain1Label.image=labelMain1Image    
        MaxLimitImage=PhotoImage(file = r"Images/MAXLIMIT.png")
        MaxLimitLabel=Label(z1,image=MaxLimitImage, compound = TOP)
        MaxLimitLabel.place(x=618, y = 160)
        MaxLimitLabel.image=MaxLimitImage    
        menubar = Menu(z1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        z1.config(menu=menubar)
        MaxPersonImage=PhotoImage(file = r"Images/MAXPERSON.png")
        MaxPersonLabel=Label(z1,image=MaxPersonImage, compound = TOP)
        MaxPersonLabel.place(x=600,y=200)
        MaxPersonLabel.image=MaxPersonImage
        tip.bind_widget(MaxPersonLabel, balloonmsg="Maximum Person")
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(z1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")
        UserEntry = Entry(z1,width = 9,font=("default",40),justify='center')
        UserEntry.place(x = 600, y = 475)
        UserEntry.insert(0, "Value")
        UserEntry.configure(state=DISABLED)
        
        def on_click(event):
            UserEntry.configure(state=NORMAL)
            UserEntry.delete(0, END)
            UserEntry.unbind('<Button-1>', on_click_id)

        on_click_id = UserEntry.bind('<Button-1>', on_click)

        def SetMaxPeople():
            try:
                if int(UserEntry.get())<=50 and int(UserEntry.get())>0:
                    x=int(UserEntry.get())
                    config.MAX_PEOPLE=x
                    UserEntry.delete(0,'end')
                    UserEntry.insert(0, "Value")
                    UserEntry.configure(state=DISABLED)
                    a="Maximum Number of Person Set:"
                    b=str(x)
                    msg= a + " " + b
                    z1.attributes('-disabled',True)
                    messagebox.showinfo("Information",msg)
                    z1.attributes('-disabled',False)
                    z1.focus_set()
                    nextButton['state']=NORMAL
                    on_click_id = UserEntry.bind('<Button-1>', on_click)
                else:
                    z1.attributes('-disabled',True)
                    messagebox.showwarning("Warning", "Please Enter an Integer Number <=50 and >0 .")
                    z1.attributes('-disabled',False)
                    z1.focus_set()
                    nextButton['state']=DISABLED
                    UserEntry.delete(0,'end')
                    UserEntry.insert(0, "Value")
                    UserEntry.configure(state=DISABLED)
                    on_click_id = UserEntry.bind('<Button-1>', on_click)
            except ValueError:
                if UserEntry.get()=='':
                    z1.attributes('-disabled',True)
                    messagebox.showwarning("Warning", "Please Enter a Number!")
                    z1.attributes('-disabled',False)
                    z1.focus_set()
                    nextButton['state']=DISABLED
                    UserEntry.insert(0, "Value")
                    UserEntry.configure(state=DISABLED)
                    on_click_id = UserEntry.bind('<Button-1>', on_click)
                else:
                    z1.attributes('-disabled',True)
                    messagebox.showwarning("Warning", "Please Enter an Integer Number!")
                    z1.attributes('-disabled',False)
                    z1.focus_set()
                    UserEntry.delete(0,'end')
                    nextButton['state']=DISABLED
                    UserEntry.insert(0, "Value")
                    UserEntry.configure(state=DISABLED)
                    on_click_id = UserEntry.bind('<Button-1>', on_click)
        setImage=PhotoImage(file = r"Images/SET.png")
        setButton=Button(z1,image=setImage, compound = TOP, command=SetMaxPeople)
        setButton.place(x=665,y=575)
        setButton.image=setImage
        tip.bind_widget(setButton,balloonmsg="This will set the Maximum number of Persons.")

    

    def WriteData():
        if(config.USE_DEVICE_CAMERA==True):
            y1.withdraw()
        else:
            u1.withdraw()
        global g1
        g1=Toplevel(w)
        g1.focus_set()
        g1.overrideredirect(False)
        g1.attributes("-fullscreen",True)
        g1.state('zoomed')
        g1.resizable(0,0)
        g1.configure(bg='blue')
        e = Example(g1)
        e.pack(fill=BOTH, expand=YES)
        config.Write_Data_Text_File=False
        config.Write_Data_Word_File=False
        config.Write_Data_Excel_File=False
        config.No_Data_Write=False

        def CUDASetup():
            g1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            g1.attributes('-disabled',False)
            g1.focus_set()
        
        def on_closing():
            g1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                g1.attributes('-disabled',False)
                w.destroy()
            else:
                g1.attributes('-disabled',False)
                g1.focus_set()

        g1.protocol("WM_DELETE_WINDOW", on_closing)

        def Back():
            if(config.USE_DEVICE_CAMERA==True):
                g1.withdraw()
                y1.deiconify()
                y1.state('zoomed')
                y1.overrideredirect(False)
            else:
                g1.withdraw()
                u1.deiconify()
                u1.state('zoomed')
                u1.overrideredirect(False)
        
        def begin():
            g1.withdraw()
            w.deiconify()
            w.state('zoomed')
     
            if os.path.exists("Data.txt"):
                os.remove("Data.txt")
            if os.path.exists("Data.docx"):
                os.remove("Data.docx")
            if os.path.exists("Data.csv"):
                os.remove("Data.csv")
            if os.path.exists("DataTemp.txt"):
                os.remove("DataTemp.txt")   
            if os.path.exists("Data.xlsx"):
                os.remove("Data.xlsx") 
            if(config.USE_DEVICE_CAMERA==True):
                cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
                while(True):
                    ret, frame = cap.read()
                    if cap.isOpened():
                        config.webcamworking=True
                        break
                    else:
                        config.webcamworking=False
                        break
                cap.release()
                cv2.destroyAllWindows()
                if(config.webcamworking==True):
                    LoadingSplash()
                else: 
                    messagebox.showerror("Error", "No Camera detected.")
            elif(config.USE_DEVICE_CAMERA==False):
                cap = cv2.VideoCapture(completeAddress)
                while(True):
                    ret, frame = cap.read()
                    if cap.isOpened():
                        config.webcamworking=False 
                        break
                    else:
                        w.attributes('-disabled',True)
                        messagebox.showerror("Error","IP Webcam Application not working.")
                        w.attributes('-disabled',False)
                        break
                cap.release()
                cv2.destroyAllWindows()
                if(config.webcamworking==False):
                    LoadingSplash()

        def WriteDataText():
            if(config.Write_Data_Text_File==True):
                g1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                g1.attributes('-disabled',False)
                g1.focus_set()
            else:
                g1.attributes('-disabled',True)
                messagebox.showinfo("Write Data", "Data will be stored in a text file.")
                g1.attributes('-disabled',False)
                g1.focus_set()
                config.Write_Data_Word_File=False
                config.Write_Data_Excel_File=False
                config.Write_Data_Text_File=True
                config.No_Data_Write=False
                NoDataWriteButton['state']=DISABLED
                DataWriteWordButton['state']=DISABLED
                DataWriteExcelButton['state']=DISABLED
                startButton['state']=NORMAL
                if(config.USE_SOCIAL_DISTANCE==True):
                    config.USE_DATA_SOCIAL_DISTANCE=True
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=False
                elif(config.USE_HUMAN_COUNT==True):
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=True
                    config.USE_DATA_BOTH=False
                else:
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=True

        def WriteDataWord():
            if(config.Write_Data_Word_File==True):
                g1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                g1.attributes('-disabled',False)
                g1.focus_set()
            else:
                g1.attributes('-disabled',True)
                messagebox.showinfo("Write Data", "Data will be stored in a word file.")
                g1.attributes('-disabled',False)
                g1.focus_set()
                config.Write_Data_Word_File=True
                config.Write_Data_Excel_File=False
                config.Write_Data_Text_File=False
                config.No_Data_Write=False
                NoDataWriteButton['state']=DISABLED
                DataWriteTextButton['state']=DISABLED
                DataWriteExcelButton['state']=DISABLED
                startButton['state']=NORMAL
                if(config.USE_SOCIAL_DISTANCE==True):
                    config.USE_DATA_SOCIAL_DISTANCE=True
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=False
                elif(config.USE_HUMAN_COUNT==True):
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=True
                    config.USE_DATA_BOTH=False
                else:
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=True

        def WriteDataExcel():
            if(config.Write_Data_Excel_File==True):
                g1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                g1.attributes('-disabled',False)
                g1.focus_set()
            else:
                g1.attributes('-disabled',True)
                messagebox.showinfo("Write Data", "Data will be stored in a Excel file.")
                g1.attributes('-disabled',False)
                g1.focus_set()
                config.Write_Data_Word_File=False
                config.Write_Data_Excel_File=True
                config.Write_Data_Text_File=False
                config.No_Data_Write=False
                NoDataWriteButton['state']=DISABLED
                DataWriteTextButton['state']=DISABLED
                DataWriteWordButton['state']=DISABLED
                startButton['state']=NORMAL
                if(config.USE_SOCIAL_DISTANCE==True):
                    config.USE_DATA_SOCIAL_DISTANCE=True
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=False
                elif(config.USE_HUMAN_COUNT==True):
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=True
                    config.USE_DATA_BOTH=False
                else:
                    config.USE_DATA_SOCIAL_DISTANCE=False
                    config.USE_DATA_HUMAN_COUNT=False
                    config.USE_DATA_BOTH=True

        def NoWriteData():
            if(config.No_Data_Write==True):
                g1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Already Selected")
                g1.attributes('-disabled',False)
                g1.focus_set()
            else:
                g1.attributes('-disabled',True)
                messagebox.showinfo("Write Data", "Data will not be stored in a text file.")
                g1.attributes('-disabled',False)
                g1.focus_set()
                DataWriteTextButton['state']=DISABLED
                DataWriteWordButton['state']=DISABLED
                DataWriteExcelButton['state']=DISABLED
                startButton['state']=NORMAL
                config.No_Data_Write=True
                config.Write_Data_Text_File=False
                config.Write_Data_Word_File=False
                config.Write_Data_Excel_File=False
                config.USE_DATA_SOCIAL_DISTANCE=False
                config.USE_DATA_HUMAN_COUNT=False
                config.USE_DATA_BOTH=False

        def SwitchStateDataWrite():
            if DataWriteTextButton['state']==NORMAL and NoDataWriteButton['state']==NORMAL and DataWriteWordButton['state']==NORMAL and DataWriteExcelButton['state']==NORMAL:
                g1.attributes('-disabled',True)
                messagebox.showwarning("Warning", "No option is selected!")
                g1.attributes('-disabled',False)
                g1.focus_set()
            else:
                DataWriteTextButton['state']=NORMAL
                DataWriteWordButton['state']=NORMAL
                DataWriteExcelButton['state']=NORMAL
                NoDataWriteButton['state']=NORMAL
                startButton['state']=DISABLED
                config.No_Data_Write=False
                config.Write_Data_Text_File=False
                config.Write_Data_Word_File=False
                config.Write_Data_Excel_File=False
        

        menubar = Menu(g1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        g1.config(menu=menubar)
        startImage=PhotoImage(file = r"Images/START.png")
        startButton=Button(g1,image=startImage, compound = TOP, command=begin)
        startButton.place(x=1200,y=700)
        startButton.image=startImage
        tip.bind_widget(startButton,balloonmsg="This will start the application.")
        startButton['state']=DISABLED
        titleImage=PhotoImage(file = r"Images/WRITE_DATA.png")
        titleLabel=Label(g1,image=titleImage, compound = TOP)
        titleLabel.place(x=575, y = 100)
        titleLabel.image=titleImage
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(g1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")
        DataWriteTextImage=PhotoImage(file = r"Images/txt.png")
        DataWriteTextButton=Button(g1,image=DataWriteTextImage, compound = TOP,command=WriteDataText,state=NORMAL)
        DataWriteTextButton.place(x=150,y=200)
        DataWriteTextButton.image=DataWriteTextImage
        tip.bind_widget(DataWriteTextButton,balloonmsg="This will write the data in a text file.")
        DataWriteWordImage=PhotoImage(file = r"Images/word.png")
        DataWriteWordButton=Button(g1,image=DataWriteWordImage, compound = TOP,command=WriteDataWord,state=NORMAL)
        DataWriteWordButton.place(x=980,y=200)
        DataWriteWordButton.image=DataWriteWordImage
        tip.bind_widget(DataWriteWordButton,balloonmsg="This will write the data in a word file.")
        DataWriteExcelImage=PhotoImage(file = r"Images/excel.png")
        DataWriteExcelButton=Button(g1, image=DataWriteExcelImage, compound = TOP,command=WriteDataExcel,state=NORMAL)
        DataWriteExcelButton.place(x=150,y=450)
        DataWriteExcelButton.image=DataWriteExcelImage
        tip.bind_widget(DataWriteExcelButton,balloonmsg="This will write the data in a Excel file.")
        NoDataWriteImage=PhotoImage(file = r"Images/NO_DATA_WRITE.png")
        NoDataWriteButton=Button(g1,image=NoDataWriteImage, compound = TOP,command=NoWriteData, state=NORMAL)
        NoDataWriteButton.place(x=980,y=450)
        NoDataWriteButton.image=NoDataWriteImage
        tip.bind_widget(NoDataWriteButton,balloonmsg="This will not write the data in a file.")
        resetImage=PhotoImage(file = r"Images/RESET.png")
        resetButton=Button(g1,image=resetImage, compound = TOP,command=SwitchStateDataWrite)
        resetButton.place(x=650,y=675)
        resetButton.image=resetImage
        tip.bind_widget(resetButton,balloonmsg="This will deselect the option.")
        
    def GPUCHECK():
        def is_cuda_cv(): # 1 == using cuda, 0 = not using cuda
            try:
                count = cv2.cuda.getCudaEnabledDeviceCount()
                if count > 0:
                    return 1
                else:
                    return 0
            except:
                return 0

        if(is_cuda_cv()==1):
            w.attributes('-disabled',True)
            messagebox.showinfo("Information", "CUDA is already enabled for the GPU.")
            w.attributes('-disabled',False)
            sublabelMainImage=PhotoImage(file = r"Images/sublabel1.png")
            sublabelMainLabel=Label(w,image=sublabelMainImage, compound = TOP)
            sublabelMainLabel.place(x=260, y = 120)
            sublabelMainLabel.image=sublabelMainImage
            gpucheckButton['state']=DISABLED
            cameracheckButton['state']=NORMAL
        else:
            w.attributes('-disabled',True)
            messagebox.showwarning("Warning", "CUDA is not enabled for the GPU. You will not be able to use the GPU.")
            w.attributes('-disabled',False)
            w.attributes('-disabled',True)
            result = messagebox.askquestion("Setup", "Do you want to check the steps to setup CUDA?")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            w.attributes('-disabled',False)
            sublabelMainImage=PhotoImage(file = r"Images/Sublabel1.png")
            sublabelMainLabel=Label(w,image=sublabelMainImage, compound = TOP)
            sublabelMainLabel.place(x=260, y = 120)
            sublabelMainLabel.image=sublabelMainImage
            cameracheckButton['state']=NORMAL
            
    def CAMERACHECK():
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while(True):
            ret, frame = cap.read()
            if cap.isOpened():
                w.attributes('-disabled',True)
                messagebox.showinfo("Information", "Webcam Detected and working properly.")
                w.attributes('-disabled',False)
                sublabelMainImage=PhotoImage(file = r"Images/Sublabel2.png")
                sublabelMainLabel=Label(w,image=sublabelMainImage, compound = TOP)
                sublabelMainLabel.place(x=260, y = 120)
                sublabelMainLabel.image=sublabelMainImage
                config.webcamworking=True
                break
            else:
                w.attributes('-disabled',True)
                messagebox.showwarning("Warning", "Webcam not detected. Please connect a webcam and try again.")
                w.attributes('-disabled',False)
                config.webcamworking=False
                break
        cap.release()
        cv2.destroyAllWindows()
        if(config.webcamworking==True):
            initializeButton['state']=NORMAL
        else:
            initializeButton['state']=DISABLED

    
    def Convert():
        t1.withdraw()
        global e1
        e1=Toplevel(w)
        e1.focus_set()
        e1.overrideredirect(False)
        e1.attributes("-fullscreen",True)
        e1.state('zoomed')
        e1.resizable(0,0)

        def CUDASetup():
            e1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            e1.attributes('-disabled',False)
            e1.focus_set()

        def on_closing():
            e1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                e1.attributes('-disabled',False)
                w.destroy()
            else:
                e1.attributes('-disabled',False)
                e1.focus_set()
                
        e1.protocol("WM_DELETE_WINDOW", on_closing)

        menubar = Menu(e1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        e1.config(menu=menubar)
        e = Example(e1)
        e.pack(fill=BOTH, expand=YES)
        
            
        def pdfclick():
            e1.attributes('-disabled',True)
            process=0
            global l1
            l1=Toplevel(e1)
            l1.focus_set()
            l1.overrideredirect(True)
            winWidth = 300
            winHeight = 150
            screenWidth = e1.winfo_screenwidth()
            screenHeight = e1.winfo_screenheight()
            x = int((screenWidth - winWidth) / 2)
            y = int((screenHeight - winHeight) / 2)
            l1.title("Converting")
            l1.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y)) 
            progress = ttk.Progressbar(l1, orient = HORIZONTAL, length = 100, mode = 'determinate')
            progress.pack(padx=100, pady = 50)   
            def update():
                global process 
                process += 10
                progress['value'] = process
                if progress['value'] >= progress['maximum']:
                    l1.withdraw()
                    e1.deiconify()
                    process=0
                    pdfconvert()
                    e1.attributes('-disabled',False)
                    return  # This will end the after() loop
                l1.after( 100, update )
            update()
            mainloop()    
            

        def excelclick():
            e1.attributes('-disabled',True)
            global k1
            k1=Toplevel(e1)
            k1.focus_set()
            k1.overrideredirect(True)
            winWidth = 300
            winHeight = 150
            screenWidth = e1.winfo_screenwidth()
            screenHeight = e1.winfo_screenheight()
            x = int((screenWidth - winWidth) / 2)
            y = int((screenHeight - winHeight) / 2)
            k1.title("Converting")
            k1.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y)) 
            progress1 = ttk.Progressbar(k1, orient = HORIZONTAL, length = 100, mode = 'determinate')
            progress1.pack(padx=100, pady = 50)   
            def update():
                global process1 
                process1 += 10
                progress1['value'] = process1
                if progress1['value'] >= progress1['maximum']:
                    k1.withdraw()
                    e1.deiconify()
                    process1=0
                    excelconvert()
                    e1.attributes('-disabled',False)
                    return  # This will end the after() loop
                k1.after( 100, update )
            update()
            mainloop()  
            

        def Back():
            e1.withdraw()
            t1.deiconify()
            t1.state('zoomed')
            t1.overrideredirect(False)  

        def pdfconvert():
            if os.path.exists("Converted/AllData-Converted.pdf"):
                e1.attributes('-disabled',True)
                messagebox.showinfo("Information","Pdf already exists. Check Converted directory.")
                e1.attributes('-disabled',False)
                DataConvertpdfButton['state']=DISABLED
                e1.focus_set()
            else:
                if os.path.exists("Converted/AllData-Converted.pdf"):
                    os.remove("Converted/AllData-Converted.pdf")
                
                pdf = FPDF()   
                pdf.add_page()
                pdf.set_font("Arial", size = 10)
                f = open("Records/AllData.txt", "r")

                for x in f:
                    pdf.cell(200, 10, txt = x, ln = 1)
                    
                pdf.output("Converted/AllData-Converted.pdf") 
                if os.path.exists("Converted/AllData-Converted.pdf"):
                    e1.attributes('-disabled',True)
                    messagebox.showinfo("Information","Pdf successfully Created. Check Converted directory.")
                    e1.attributes('-disabled',False)
                    DataConvertpdfButton['state']=DISABLED
                    e1.focus_set()
                else:
                    e1.attributes('-disabled',True)
                    messagebox.showerror("Error","Pdf creation unsuccessful.")
                    e1.attributes('-disabled',False)
                    e1.focus_set()
        
        def excelconvert():
            if os.path.exists("Converted/AllData-Converted.xlsx"):
                e1.attributes('-disabled',True)
                messagebox.showinfo("Information","Excel file already exists. Check Converted directory.")
                e1.attributes('-disabled',False)
                DataConvertexcelButton['state']=DISABLED
                e1.focus_set()
            else:
                if os.path.exists("Converted/AllData-Converted.xlsx"):
                    os.remove("Converted/AllData-Converted.xlsx")

                websites = pd.read_csv("Records/RawData.txt",header = None)
                websites.columns = ['Social Distance Violations', 'Human Count', 'Recorded at','Limit Reached?']
                websites.to_csv('Converted/AllData-Converted.csv', index = None)
                datafinal = pd.read_csv('Converted/AllData-Converted.csv') 
                datafinal.to_excel('Converted/AllData-Converted.xlsx', 'Output', index=False)

                writer = pd.ExcelWriter('Converted/AllData-Converted.xlsx') 
                datafinal.to_excel(writer, sheet_name='Output', index=False, na_rep='NA')
                col_idx1 = datafinal.columns.get_loc('Social Distance Violations')
                writer.sheets['Output'].set_column(col_idx1, col_idx1, 30)
                col_idx2 = datafinal.columns.get_loc('Human Count')
                writer.sheets['Output'].set_column(col_idx2, col_idx2, 30)
                col_idx3 = datafinal.columns.get_loc('Recorded at')
                writer.sheets['Output'].set_column(col_idx3, col_idx3, 30)
                col_idx4 = datafinal.columns.get_loc('Limit Reached?')
                writer.sheets['Output'].set_column(col_idx4, col_idx4, 30)
                writer.save()

                if os.path.exists("Converted/AllData-Converted.csv"):
                    os.remove("Converted/AllData-Converted.csv")
                if os.path.exists("Converted/AllData-Converted.xlsx"):
                    e1.attributes('-disabled',True)
                    messagebox.showinfo("Information","Excel file successfully Created. Check Converted directory.")
                    e1.attributes('-disabled',False)
                    DataConvertexcelButton['state']=DISABLED
                    e1.focus_set()
                else:
                    e1.attributes('-disabled',True)
                    messagebox.showerror("Error","Excel File creation unsuccessful.")
                    e1.attributes('-disabled',False)
                    e1.focus_set()

        DataConvertpdfImage=PhotoImage(file = r"Images/pdfconvert.png")
        DataConvertpdfButton=Button(e1,image=DataConvertpdfImage, compound = TOP,command=pdfclick,state=NORMAL)
        DataConvertpdfButton.place(x=200,y=200)
        DataConvertpdfButton.image=DataConvertpdfImage
        tip.bind_widget(DataConvertpdfButton,balloonmsg="This will convert the data in a text file into a pdf.")
        DataConvertexcelImage=PhotoImage(file = r"Images/excelconvert.png")
        DataConvertexcelButton=Button(e1,image=DataConvertexcelImage, compound = TOP,command=excelclick,state=NORMAL)
        DataConvertexcelButton.place(x=900,y=200)
        DataConvertexcelButton.image=DataConvertexcelImage
        tip.bind_widget(DataConvertexcelButton,balloonmsg="This will convert the data in a text file to an excel file.")
        backImage=PhotoImage(file = r"Images/BACK.png")
        backButton=Button(e1,image=backImage, compound = TOP,command=Back)
        backButton.place(x=100,y=700)
        backButton.image=backImage
        tip.bind_widget(backButton,balloonmsg="This will open the previous page.")
        titleImage=PhotoImage(file = r"Images/Conversion.png")
        titleLabel=Label(e1,image=titleImage, compound = TOP)
        titleLabel.place(x=565, y = 100)
        titleLabel.image=titleImage

    
    def Viewdata():
        w.withdraw()
        global t1
        t1=Toplevel(w)
        t1.focus_set()
        t1.overrideredirect(False)
        t1.attributes("-fullscreen",True)
        t1.state('zoomed')
        t1.resizable(0,0)
        t1.configure(bg='black')

        def CUDASetup():
            t1.attributes('-disabled',True)
            result = messagebox.askquestion("Information", "Are you sure? You will be directed to an external webpage.")
            if result=="yes":
                webbrowser.open('https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781')
            else:
                pass
            t1.attributes('-disabled',False)
            t1.focus_set()

        def on_closing():
            t1.attributes('-disabled',True)
            resultquit = messagebox.askquestion("Quit", "Do you want to quit?")
            if resultquit=="yes":
                t1.attributes('-disabled',False)
                w.destroy()
            else:
                t1.attributes('-disabled',False)
                t1.focus_set()
                
        t1.protocol("WM_DELETE_WINDOW", on_closing)
        
        def Back():
            t1.withdraw()
            w.deiconify()
            w.state('zoomed')
            w.overrideredirect(False)          

        menubar = Menu(t1)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Home", command=Back)
        if os.path.exists("Records/AllData.txt"):
            filemenu.add_command(label="Convert...", command=Convert)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
        helpmenu.add_separator()
        helpmenu.add_command(label="Credits...", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        t1.config(menu=menubar)
        filename = "Records/AllData.txt"           
        top = Frame(t1); top.pack(side='top')
        text = Pmw.ScrolledText(
            top,
            borderframe=1, 
            vscrollmode='dynamic', 
            hscrollmode='dynamic',
            labelpos='n', 
            label_text='All Data',
            text_width=200, 
            text_height=48,
            text_wrap='none',
            )
        text.pack()
        if os.path.exists("Records/AllData.txt"):
            text.insert('end', open(filename,'r').read())
        Button(top, text='Home', command=Back).pack(pady=15)
        


    menubar = Menu(w)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Quit", command=on_closing)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="CUDA Setup...", command=CUDASetup)
    helpmenu.add_separator()       
    helpmenu.add_command(label="Credits...", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)
    w.config(menu=menubar)
    labelMainImage=PhotoImage(file = r"Images/covieye.png")
    labelMainLabel=Label(w,image=labelMainImage, compound = TOP)
    labelMainLabel.place(x=650, y = 30)
    labelMainLabel.image=labelMainImage
    sublabelMainImage=PhotoImage(file = r"Images/sublabel.png")
    sublabelMainLabel=Label(w,image=sublabelMainImage, compound = TOP)
    sublabelMainLabel.place(x=260, y = 120)
    sublabelMainLabel.image=sublabelMainImage
    gpucheckImage=PhotoImage(file = r"Images/GPU_CHECK.png")
    gpucheckButton=Button(w,image=gpucheckImage, compound = TOP,command=GPUCHECK,state=NORMAL)
    gpucheckButton.place(x=100,y=200)
    gpucheckButton.image=gpucheckImage
    tip.bind_widget(gpucheckButton,balloonmsg="This will check whether CUDA is enabled for GPU or not.")
    cameracheckImage=PhotoImage(file = r"Images/CAMERA_CHECK.png")
    cameracheckButton=Button(w,image=cameracheckImage, compound = TOP,command=CAMERACHECK, state=DISABLED)
    cameracheckButton.place(x=565,y=200)
    cameracheckButton.image=cameracheckImage
    tip.bind_widget(cameracheckButton,balloonmsg="This will check whether camera is available or not.")
    viewdataImage=PhotoImage(file = r"Images/VIEW_DATA.png")
    viewdataButton=Button(w,image=viewdataImage, compound = TOP,command=Viewdata, state=NORMAL)
    viewdataButton.place(x=1030,y=200)
    viewdataButton.image=viewdataImage
    tip.bind_widget(viewdataButton,balloonmsg="This will show the all data.")
    initializeImage=PhotoImage(file = r"Images/BEGIN.png")
    initializeButton=Button(w,image=initializeImage, compound = TOP,command=SelectRenderer,state=DISABLED)
    initializeButton.place(x=1250,y=700)
    initializeButton.image=initializeImage
    tip.bind_widget(initializeButton,balloonmsg="Start the Application")
    w.protocol("WM_DELETE_WINDOW", on_closing)

    w.mainloop()
