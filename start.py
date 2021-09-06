# -*- coding: utf-8 -*-

import platform
import sys
import time
from datetime import datetime

from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import BLL
import miscFunctions
import telegramBot


if __name__ == "__main__":
    # Main Program
    if platform.system() == "Windows":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif platform.system() == "Linux":
        # Initalize virtual display for headless pi
        display = Display(visible=0, size=(800, 800))
        display.start()
        driver = webdriver.Chrome()

    driver.get("https://info.bbdc.sg/members-login/")

    BLL.LogicalFullSteps(driver)
    # # Idie of number of seconds defined in credentials.json before attempting to get latest slot availbility
    while True:
        try:
            miscFunctions.printMessage(
                "Snoozing for "
                + str(BLL.readJSON()["generalSettings"]["refreshTimeIntervalInSeconds"])
                + " seconds"
            )
            time.sleep(BLL.readJSON()["generalSettings"]["refreshTimeIntervalInSeconds"])
            miscFunctions.printMessage("Waking up from sleep")
            BLL.reloadSessionsAvailbility(driver)
        except Exception as e:
            telegramBot.sendMessage("An error has occurred. Application is exiting..")
            telegramBot.sendMessage(e)
            miscFunctions.printMessage(e)
            sys.exit(1)
