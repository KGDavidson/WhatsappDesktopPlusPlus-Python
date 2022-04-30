from tkinter import *
import traceback
import base64
import io
from PIL import ImageTk, Image
import threading

class GUI(threading.Thread):
    screen = 0

    screenFunctions = []

    def __init__(self) -> None:
        self.b64 = ""
        self.screenFunctions = [
            self.buildQRCodeScreen
        ]

        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def changeQRCodeImage(self, b64):
        self.b64 = b64

    def QRCodeScanned(self, value):
        if value:
            self.screen += 1

    def run(self):
        try:
            self.root = Tk()
            self.root.overrideredirect(1)

            self.root.after(200, self.mainloop)

            self.root.mainloop()
        except:
            print(traceback.print_exception())

    def mainloop(self):
        self.screenFunctions[self.screen]()

        print("test")

        self.root.after(200, self.mainloop)

    def buildQRCodeScreen(self):
        w = 1008
        h = 670
        self.root.geometry(str(w) + "x" + str(h))
        self.mainFrame = Frame(self.root, width=w, height=h, bg="white")
        self.mainFrame.pack()
        self.mainFrame.place(anchor='center', relx=0.5, rely=0.5)

        if self.b64:
            try: self.label.destroy() 
            except: pass
            dataBytesIO = io.BytesIO(self.b64)
            self.img = PhotoImage(data=dataBytesIO.read())
            self.label = Label(self.mainFrame, image= self.img)
            self.label.pack()