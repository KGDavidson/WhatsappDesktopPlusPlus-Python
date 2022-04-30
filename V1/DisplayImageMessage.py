from win32api import GetMonitorInfo, MonitorFromPoint
from PIL import ImageTk, Image
import tkinter
import sys
from io import BytesIO
import base64
import re


def closeButton():
    exit()


url = sys.argv[1]

monitorInfo = GetMonitorInfo(MonitorFromPoint((0, 0)))
workArea = monitorInfo.get("Work")
screenWidth = workArea[2]
screenHeight = workArea[3]

top = tkinter.Tk()

top.overrideredirect(1)
top.wm_attributes("-topmost", 1)

imageData = re.sub('^data:image/.+;base64,', '', url)
pilImg = Image.open(BytesIO(base64.b64decode(imageData)))
imgWidth, imgHeight = pilImg.size

windowHeight = imgHeight + 30
windowWidth = imgWidth
top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
             "+" + str(screenHeight - windowHeight - 300))

closeButton = tkinter.Button(top, text="X", command=closeButton)
closeButton.config(width=imgWidth)
closeButton.pack(side=tkinter.TOP)

img = ImageTk.PhotoImage(pilImg)
qrCodeImg = tkinter.Label(top, image=img)
qrCodeImg.pack(side=tkinter.TOP, fill="both", expand="yes")

top.mainloop()
