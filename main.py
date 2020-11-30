from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import ImageTk, Image
import tkinter
import time
import os
from win32api import GetMonitorInfo, MonitorFromPoint

currentPath = __file__.split("main.py")[0]

windowHeight = 0
windowWidth = 0
timeToWaitForScan = 90

currentChat = None
messagesList = []

top = tkinter.Tk()

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
screenWidth = work_area[2]
screenHeight = work_area[3]

top.overrideredirect(1)
top.wm_attributes("-topmost", 1)

loadingText = tkinter.Label(top, text="Loading...")
loadingText.pack(side="bottom", fill="both", expand="yes")
windowHeight = 25
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


def closeButton():
    global driver
    global top

    driver.quit()
    top.destroy()
    exit()


def getChatContactsListNames(chatContactsListItem):
    chatContactsListName = chatContactsListItem.find_element_by_class_name(
        "_3Tw1q").text
    if (chatContactsListName != ""):
        return chatContactsListName
    else:
        return "Chat"


def getMessageText(parentClass):
    messageTimeAndSource = parentClass.text.rsplit("\n", 1)
    if ("message-in" in parentClass.get_attribute("class")):
        messageTimeAndSource.append("0")
    if ("message-out" in parentClass.get_attribute("class")):
        messageTimeAndSource.append("1")
    return (messageTimeAndSource)


def setCurrentChat(currentChatName, chatContactsListNames, chatContactsList):
    global driver

    currentChat = currentChatName
    chatContactsList[chatContactsListNames.index(currentChatName)].click()
    time.sleep(1)
    updateChatMessages()


def updateChatMessages():
    global messagesList
    global top
    global driver

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
        allMessagesText = list(
            filter(lambda item: len(item) == 3, allMessagesTextTemp))[-7:]
    except:
        pass

    if (len(allMessagesText) == 7):
        for i in range(7):
            messagesList[i]["text"] = allMessagesText[i][0]
            if (allMessagesText[i][2] == "0"):
                messagesList[i]["anchor"] = tkinter.constants.W
            else:
                messagesList[i]["anchor"] = tkinter.constants.E
    else:
        for i in range(7):
            messagesList[i]["text"] = ""

    top.after(1000, updateChatMessages)


def sendMessage(driver, value):
    try:
        inputBox = driver.find_element_by_class_name(
            "DuUXI").find_element_by_class_name("_1awRl")
        inputBox.send_keys(value)
        inputBox.send_keys('\ue007')
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
    driver.quit()
    top.destroy()
    exit()

if (loadingText):
    loadingText.destroy()

if (qrCodeImg):
    qrCodeImg.destroy()
    top.update()

loadingText = tkinter.Label(top, text="Loading...")
loadingText.pack(side="bottom", fill="both", expand="yes")
windowHeight = 25
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

closeButton = tkinter.Button(top, text="X", command=closeButton)
closeButton.config(width=2)
closeButton.pack(side=tkinter.LEFT, anchor=tkinter.NW)

dropDownMenu = tkinter.OptionMenu(top, listChatNames, *chatContactsListNames,
                                  command=lambda currentChatName: setCurrentChat(currentChatName, chatContactsListNames, chatContactsList))
dropDownMenu.config(width=150)
dropDownMenu.pack(side=tkinter.LEFT, anchor=tkinter.NW)

windowHeight = 200
windowWidth = 300
top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
             "+" + str(screenHeight - windowHeight))

for i in range(7):
    message = tkinter.Label(
        top, text="", anchor=tkinter.constants.W)
    messagesList.append(message)

for message in messagesList:
    message.pack(fill="x")

inputBox = tkinter.Entry(top)
inputBox.bind("<Return>", (lambda event: sendMessage(
    driver, inputBox.get()) or inputBox.delete(0, 'end')))
inputBox.pack(fill="x")
top.update()
time.sleep(2)

top.after(1, updateChatMessages)

top.mainloop()

if os.path.exists(currentPath + "check.png"):
    os.remove(currentPath + "check.png")

driver.quit()
top.destroy()
