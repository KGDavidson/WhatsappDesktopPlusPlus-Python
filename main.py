import driver
import gui

'''
QR Code Screen

Chats screen
'''

#g = gui.GUI()

def main():
    driver.init()
    driver.getQRCode()
    #g.QRCodeScanned(driver.waitForQRScan())
    # Driver waits for update
    # When qr code scanned, gui is updated
    pass

if __name__ == "__main__":
    main()