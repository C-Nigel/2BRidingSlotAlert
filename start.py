# -*- coding: utf-8 -*-

import platform
import time
from datetime import datetime

from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import BLL

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
    BLL.printMessage(
        "Snoozing for "
        + str(BLL.readJSON()["generalSettings"]["refreshTimeIntervalInSeconds"])
        + " seconds"
    )
    time.sleep(BLL.readJSON()["generalSettings"]["refreshTimeIntervalInSeconds"])
    BLL.printMessage(" Waking up from sleep")
    BLL.reloadSessionsAvailbility(driver)
