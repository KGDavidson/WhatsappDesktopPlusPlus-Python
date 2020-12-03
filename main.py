from win32api import GetMonitorInfo, MonitorFromPoint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import ImageTk, Image
import tkinter
import time
import os
import copy

currentPath = __file__.split("main.py")[0]
dontNotif = False
dropDownMenu = None

numberOfMessagesShown = 12
screenMinHeight = 23
screenMaxHeight = 300

closed = False

windowHeight = 0
windowWidth = 0
timeToWaitForScan = 90

currentChat = None
messagesList = []
prevMessagesList = []
imageUrls = []

top = tkinter.Tk()

monitorInfo = GetMonitorInfo(MonitorFromPoint((0, 0)))
workArea = monitorInfo.get("Work")
screenWidth = workArea[2]
screenHeight = workArea[3]

top.overrideredirect(1)
top.wm_attributes("-topmost", 1)
top.configure(bg="#0d1418")

loadingText = tkinter.Label(top, text="Loading...")
loadingText.configure(bg="#2a2f32", fg="#e1e2e3")
loadingText.pack(side="bottom", fill="both", expand="yes")

windowHeight = screenMinHeight
windowWidth = 300
top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
             "+" + str(screenHeight - windowHeight))
top.update()

chromeOptions = Options()
chromeOptions.add_argument("user-data-dir=" + currentPath + "selenium")
chromeOptions.add_argument('headless')
chromeOptions.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36")
chromeOptions.add_argument("remote-debugging-port=9222")

driver = webdriver.Chrome(
    currentPath + r"Driver\chromedriver.exe", options=chromeOptions)

driver.get("http://web.whatsapp.com")

qrCode = False
qrCodeScanned = True


def exitApp():
    global driver
    global top

    if os.path.exists(currentPath + "check.png"):
        os.remove(currentPath + "check.png")

    driver.close()
    top.destroy()
    exit()


def messageClicked(event):
    global top
    global imageUrls

    labelValue = event.widget.cget("text")
    if ("Click to Open Image" in labelValue):
        urlNumber = int(labelValue.split("Image ")[1])
        os.system("DisplayImageMessage.py " + imageUrls[urlNumber - 1])
    else:
        top.clipboard_clear()
        top.clipboard_append(labelValue)


def closeButton():
    exitApp()


def setNotifImg(x):
    global dropDownMenu

    if (x):
        img = ImageTk.PhotoImage(Image.open(
            currentPath + "notif.png"))
        dropDownMenu['image'] = img
        img.image = img
    else:
        img = ImageTk.PhotoImage(Image.open(
            currentPath + "null.png"))
        dropDownMenu['image'] = img
        img.image = img


def minimiseButton():
    global top
    global closed
    global minimiseButton
    global dontNotif
    global notifImg
    global dropDownMenu

    closed = not closed

    if (closed):
        windowHeight = screenMinHeight
        windowWidth = 300
        top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
                     "+" + str(screenHeight - windowHeight))
        minimiseButton["text"] = "ᐱ"
        setNotifImg(False)
        top.update()
    else:
        windowHeight = screenMaxHeight
        windowWidth = 300
        top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
                     "+" + str(screenHeight - windowHeight))
        minimiseButton["text"] = "ᐯ"
        setNotifImg(False)
        top.update()


def getChatContactsListNames(chatContactsListItem):
    chatContactsListName = chatContactsListItem.find_element_by_class_name(
        "_3Tw1q").text
    if (chatContactsListName != ""):
        return chatContactsListName
    else:
        return "Emoji"


def getMessageText(parentClass):
    global imageUrls

    imgTag = None
    try:
        imgTag = parentClass.find_element_by_tag_name('img')
    except:
        pass
    inputText = parentClass.text.rsplit("\n", 1)
    messageSourceTime = []
    n = 40

    timeSent = ""
    inOut = "0"

    try:
        timeSent = inputText[1]
    except:
        pass

    chunks = [inputText[0][i:i+n]
              for i in range(0, len(inputText[0]), n)]

    if ("message-in" in parentClass.get_attribute("class")):
        inputText.append("0")
        inOut = "0"
    if ("message-out" in parentClass.get_attribute("class")):
        inputText.append("1")
        inOut = "1"

    if (imgTag is not None):
        imageUrls.append(imgTag.get_attribute("src"))
        messageSourceTimeAdd = []
        messageSourceTimeAdd.append(
            "Click to Open Image " + str(len(imageUrls)))
        messageSourceTimeAdd.append(timeSent)
        messageSourceTimeAdd.append(inOut)
        messageSourceTime.append(messageSourceTimeAdd)
    else:
        for chunk in chunks:
            messageSourceTimeAdd = []
            messageSourceTimeAdd.append(chunk)
            if (timeSent != ""):
                messageSourceTimeAdd.append(timeSent)
            messageSourceTimeAdd.append(inOut)
            messageSourceTime.append(messageSourceTimeAdd)

    return (messageSourceTime)


def setCurrentChat(currentChatName, chatContactsListNames, chatContactsList):
    global driver
    global dontNotif

    currentChat = currentChatName
    chatContactsList[chatContactsListNames.index(currentChatName)].click()
    dontNotif = True
    setNotifImg(False)


def updateChatMessages():
    global messagesList
    global prevMessagesList
    global top
    global driver
    global imageUrls
    global dontNotif
    global closed

    notif = False
    prevMessagesList = list(map(lambda x: x["text"], messagesList))

    imageUrls = []
    allMessagesText = []

    try:
        loadingIcon = ""
        while (loadingIcon):
            try:
                loadingIcon = driver.find_element_by_css_selector("svg.aLK5N")
            except:
                loadingIcon = None
            time.sleep(1)
        allMessages = driver.find_elements_by_css_selector("div.tSmQ1 > div")
        allMessagesTextTemp = list(
            map(lambda currentMessage: getMessageText(currentMessage), allMessages))
        allMessagesTextTemp = [
            item for sublist in allMessagesTextTemp for item in sublist]
        allMessagesText = list(
            filter(lambda item: len(item) >= 3, allMessagesTextTemp))[-numberOfMessagesShown:]
    except:
        pass

    if (len(allMessagesText) == numberOfMessagesShown):
        for i in range(numberOfMessagesShown):
            messagesList[i]["text"] = allMessagesText[i][0]
            if (allMessagesText[i][2] == "0"):
                messagesList[i]["anchor"] = tkinter.constants.W
            else:
                messagesList[i]["anchor"] = tkinter.constants.E
    else:
        for i in range(numberOfMessagesShown):
            messagesList[i]["text"] = ""

    if dontNotif or not closed:
        dontNotif = False
    else:
        try:
            if (len(messagesList) != len(prevMessagesList)):
                notif = True
            else:
                for i in range(len(messagesList)):
                    if (messagesList[i]["text"] != prevMessagesList[i]):
                        notif = True
                        break
            if (notif):
                setNotifImg(True)
        except:
            pass

    top.after(1000, updateChatMessages)


def sendMessage(driver, value):
    global dontNotif

    try:
        inputBox = driver.find_element_by_class_name(
            "DuUXI").find_element_by_class_name("_1awRl")
        inputBox.send_keys(value)
        inputBox.send_keys('\ue007')
        dontNotif = True
        setNotifImg(False)
    except:
        pass


while (not driver.find_elements_by_class_name("_3LtPa")):
    if (driver.find_elements_by_class_name("_1PTz1")):
        driver.find_element_by_class_name(
            '_1yHR2').screenshot(currentPath + "check.png")
        qrCode = True
        break
    time.sleep(1)

qrCodeImg = None

if (qrCode):
    if (loadingText):
        loadingText.destroy()

    img = ImageTk.PhotoImage(Image.open(currentPath + "check.png"))
    qrCodeImg = tkinter.Label(top, image=img)
    qrCodeImg.configure(bg="#FFFFFF")
    qrCodeImg.pack(side="bottom", fill="both", expand="yes")
    windowHeight = 300
    windowWidth = 300
    top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
                 "+" + str(screenHeight - windowHeight))
    time.sleep(1)
    top.update()

    timePassed = 0

    while ((not driver.find_elements_by_class_name("_3LtPa")) and (timePassed < timeToWaitForScan)):
        time.sleep(1)
        timePassed += 1

    if (timePassed > timeToWaitForScan):
        qrCodeScanned = False

if (not qrCodeScanned):
    exitApp()

if (loadingText):
    loadingText.destroy()
if (qrCodeImg):
    qrCodeImg.destroy()
    top.update()

loadingText = tkinter.Label(top, text="Loading...")
loadingText.configure(bg="#2a2f32", fg="#e1e2e3")
loadingText.pack(side="bottom", fill="both", expand="yes")
windowHeight = screenMinHeight
windowWidth = 300
top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
             "+" + str(screenHeight - windowHeight))
top.update()

chatContactsList = driver.find_elements_by_class_name("_1MZWu")
chatContactsList[1:] = reversed(chatContactsList[1:])
chatContactsListNames = list(
    map(getChatContactsListNames, chatContactsList))

if (loadingText):
    loadingText.destroy()

listChatNames = tkinter.StringVar(top)
"""
closeButton = tkinter.Button(top, text="X", command=closeButton)
closeButton.config(width=2)
closeButton.pack(side=tkinter.LEFT, anchor=tkinter.NW)"""

topFrame = tkinter.Frame(top)
topFrame.configure(bg="#2a2f32")
topFrame.pack(side=tkinter.TOP, fill="x", expand=True)

closeButton = tkinter.Button(
    topFrame, text="X", command=closeButton, highlightthickness=0, bd=0, relief='flat')
closeButton.configure(width=2, bg="#2a2f32", fg="#e1e2e3",
                      activebackground='#323739', activeforeground='#e1e2e3')
closeButton.pack(side=tkinter.LEFT, fill="y")

dropDownMenu = tkinter.OptionMenu(topFrame, listChatNames, *chatContactsListNames,
                                  command=lambda currentChatName: setCurrentChat(currentChatName, chatContactsListNames, chatContactsList))
dropDownMenu.configure(width=5, bg="#2a2f32", fg="#e1e2e3",
                       activebackground='#323739', activeforeground='#e1e2e3', highlightthickness=0, bd=0, relief='flat', indicatoron=0, compound='right')
dropDownMenu["menu"].config(bg="#2a2f32", fg="#e1e2e3",
                            activebackground='#323739', activeforeground='#e1e2e3', bd=0, relief='flat')
dropDownMenu.pack(side=tkinter.LEFT, fill="x", expand=True)

minimiseButton = tkinter.Button(
    topFrame, text="ᐯ", command=minimiseButton, highlightthickness=0, bd=0, relief='flat')
minimiseButton.configure(width=2, bg="#2a2f32", fg="#e1e2e3",
                         activebackground='#323739', activeforeground='#e1e2e3')
minimiseButton.pack(side=tkinter.LEFT, fill="y")

windowHeight = screenMaxHeight
windowWidth = 300
top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
             "+" + str(screenHeight - windowHeight))

for i in range(numberOfMessagesShown):
    message = tkinter.Label(
        top, text="", anchor=tkinter.constants.W)
    message.bind("<Button-1>", messageClicked)
    messagesList.append(message)

for message in messagesList:
    message.configure(width=150, bg="#0d1418", fg="#e1e1e2")
    message.pack(side=tkinter.TOP, fill="x", expand=True)


bottomFrame = tkinter.Frame(top)
bottomFrame.configure(bg="#33383b")
bottomFrame.pack(side=tkinter.TOP, fill="x", expand=True)

inputBox = tkinter.Label(bottomFrame)
inputBox.configure(width="2", bg="#33383b", fg="#e1e1e2",
                   highlightthickness=0, bd=0, relief='flat')
inputBox.pack(side=tkinter.LEFT)

inputBox = tkinter.Entry(bottomFrame)
inputBox.bind("<Return>", (lambda event: sendMessage(
    driver, inputBox.get()) or inputBox.delete(0, 'end')))
inputBox.configure(bg="#33383b", fg="#e1e1e2",
                   highlightthickness=0, bd=0, relief='flat', insertbackground="#FFFFFF")
inputBox.pack(side=tkinter.LEFT, fill="x", expand=True)
top.update()
time.sleep(2)

top.after(1, updateChatMessages)

top.mainloop()

exitApp()
