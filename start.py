# -*- coding: utf-8 -*-

import platform
import sys
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import BLL
import initlization
import telegramBot

if __name__ == "__main__":
    # Main Program
    # Setup credentials and preferences YAML files
    initlization.generateCredentialsTemplate()
    initlization.generateSettingsTemplate()

    if platform.system() == "Windows":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif platform.system() == "Linux":
        # Initalize virtual display for headless pi
        display = Display(visible=0, size=(800, 800))
        display.start()
        driver = webdriver.Chrome()

    driver.get("https://info.bbdc.sg/members-login/")

    BLL.LogicalFullSteps(driver)
    # # Idie of number of seconds defined in preferences.yaml before attempting to get latest slot availbility
    while True:
        try:
            BLL.printMessage(
                "Snoozing for "
                + str(BLL.readPreferences()["Preferences"]["Refresh time interval"])
                + " seconds"
            )
            time.sleep(BLL.readPreferences()["Preferences"]["Refresh time interval"])
            BLL.printMessage("Waking up from sleep")
            BLL.reloadSessionsAvailbility(driver)
        except Exception as e:
            telegramBot.sendMessage("An error has occurred. Application is retarting..")
            telegramBot.sendMessage(e)
            BLL.printMessage(repr(e))
            driver.quit()
            driver = None
            if platform.system() == "Windows":
                driver = webdriver.Chrome(ChromeDriverManager().install())
            elif platform.system() == "Linux":
                driver = webdriver.Chrome()
            driver.get("https://info.bbdc.sg/members-login/")
            BLL.LogicalFullSteps(driver)
