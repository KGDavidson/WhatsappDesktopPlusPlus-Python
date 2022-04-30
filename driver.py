import time
import base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def setViewportSize(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def waitFor(className, type=By.CLASS_NAME):
    while not driver.find_elements(type, className):
        time.sleep(1)

#options = Options()
#options.add_argument("--app=https://web.whatsapp.com/")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Firefox(firefox_binary=FirefoxBinary(r"C:\Users\kreat\Downloads\FirefoxPortable\App\Firefox\firefox.exe"), executable_path="geckodriver.exe")

setViewportSize(driver, 820, 470)
driver.execute_script("return [window.innerWidth, window.innerHeight];")

def init():
    driver.get("https://web.whatsapp.com/")

def getQRCode():
    waitFor("canvas", By.CSS_SELECTOR)

    canvas = driver.find_element_by_css_selector("canvas")
    canvasBase64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

    canvasPNG = base64.b64decode(canvasBase64)

    return canvasPNG

def waitForQRScan():
    try:
        driver.waitFor("pane-side", By.ID)
    except:
        return False
    return True

def close():
    driver.close()