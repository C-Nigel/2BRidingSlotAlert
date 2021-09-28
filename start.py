# -*- coding: utf-8 -*-
import platform
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import BLL
import initlization
import telegramBot


# Initalize virtual display for headless pi
# visible = 1 to show display, otherwise 0 to hide
def startDisplay():
    display = Display(visible=0, size=(800, 800))
    display.start()


# Initalize a new driver
def startDriver(initalizeDisplay=False):
    if platform.system() == "Windows":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif platform.system() == "Linux":
        if initalizeDisplay:
            startDisplay()
        driver = webdriver.Chrome()

    driver.get("https://info.bbdc.sg/members-login/")

    return driver


if __name__ == "__main__":
    # Main Program
    # Setup credentials and preferences YAML files
    initlization.generateCredentialsTemplate()
    initlization.generateSettingsTemplate()

    driver = startDriver(True)

    goToLoginPage = True
    while True:
        try:
            if goToLoginPage:
                BLL.LogicalFullSteps(driver)
                goToLoginPage = False
            BLL.printMessage(
                "Snoozing for "
                + str(BLL.readPreferences()["Preferences"]["Refresh time interval"])
                + " seconds"
            )
            time.sleep(BLL.readPreferences()["Preferences"]["Refresh time interval"])
            BLL.printMessage("Waking up from sleep")
            BLL.reloadSessionsAvailbility(driver)
        except Exception as e:
            telegramBot.sendMessage(
                "An error has occurred. Application is restarting.."
            )
            telegramBot.sendMessage(e)
            BLL.printMessage(repr(e))
            driver.get("https://info.bbdc.sg/members-login/")
            goToLoginPage = True
            time.sleep(5)
