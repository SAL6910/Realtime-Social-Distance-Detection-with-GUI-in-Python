from tkinter import Tk, Label, font
from time import sleep
from Support.app import MainPage



class LoadingSplash:
    def __init__(self):
        self.root=Tk()
        self.root.config(bg="black")
        self.root.title("Custom Loader")
        self.root.attributes("-fullscreen",True)
        self.root.attributes("-disabled",True)

        Label(self.root, text="Initializing Application", font="Bahnschrift 30",bg="black", fg="#FFBD09").place(x=600,y=300)
        Label(self.root, text="CoviEYE", font="Bahnschrift 70",bg="black", fg="#FFFFFF").place(x=625,y=600)
        Label(self.root, text="Do not Switch Screen.", font="Bahnschrift 15",bg="black", fg="#FFFFFF").place(x=700,y=475)

        for i in range(16):
            Label(self.root, bg="#1F2732", width=5,height=3).place(x=(i+8)*50,y=400)

        self.root.update()
        self.play_animation()

        self.root.mainloop()
    
    def play_animation(self):
        for i in range(3):
            for j in range(16):
                Label(self.root,bg="#FFBD09",width=5,height=3).place(x=(j+8)*50,y=400)
                sleep(0.06)
                self.root.update_idletasks()
                Label(self.root,bg="#1F2732",width=5,height=3).place(x=(j+8)*50,y=400)
        else:
            self.root.destroy()
            MainPage()
            exit(0)



if __name__=="__main__":
    LoadingSplash()