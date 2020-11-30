from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
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


def getChatContactsListNames(chatContactsListItem):
    chatContactsListName = chatContactsListItem.select_one('._3Tw1q').text
    if (chatContactsListName != ""):
        return chatContactsListName
    else:
        return "Chat"


def setCurrentChat(value):
    currentChat = value


while True:
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
    # chromeOptions.add_argument('headless')
    chromeOptions.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36")
    chromeOptions.add_argument("remote-debugging-port=9222")

    driver = webdriver.Chrome(
        currentPath + r"Driver\chromedriver.exe", options=chromeOptions)

    driver.get("http://web.whatsapp.com")

    html = driver.page_source
    soup = bs(html, 'lxml')

    qrCode = False
    qrCodeScanned = True

    while (not soup.find_all("div", {"class": "_3LtPa"})):
        if (soup.find_all("div", {"class": "_1PTz1"})):
            driver.find_element_by_class_name(
                '_1yHR2').screenshot(currentPath + "check.png")
            qrCode = True
            break
        html = driver.page_source
        soup = bs(html, 'lxml')
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
        top.update()

        timePassed = 0

        while ((not soup.find_all("div", {"class": "_3LtPa"})) and (timePassed < timeToWaitForScan)):
            html = driver.page_source
            soup = bs(html, 'lxml')
            time.sleep(1)
            timePassed += 1

        if (timePassed > timeToWaitForScan):
            qrCodeScanned = False

    print(qrCodeScanned)
    if (not qrCodeScanned):
        break

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
    print("Tag Found")

    chatContactsList = soup.find_all("div", {"class": "_1MZWu"})
    chatContactsList[1:] = reversed(chatContactsList[1:])
    chatContactsListNames = list(
        map(getChatContactsListNames, chatContactsList))

    if (loadingText):
        loadingText.destroy()

    listChatNames = tkinter.StringVar(top)
    listChatNames.set(chatContactsListNames[0])
    setCurrentChat(chatContactsListNames[0])

    dropDownMenu = tkinter.OptionMenu(
        top, listChatNames, *chatContactsListNames, command=setCurrentChat)
    dropDownMenu.pack()

    windowHeight = 200
    windowWidth = 300
    top.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(screenWidth - windowWidth) +
                 "+" + str(screenHeight - windowHeight))

    while True:
        top.update()

    break


driver.quit()
top.destroy()
