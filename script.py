# -*- coding: utf-8 -*-

from os import read
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from pyvirtualdisplay import Display
import selenium.webdriver.support.expected_conditions as ec
import time
import telegramBot
import json


# Import and read json file
with open("./credentials.json") as f:
    data = json.load(f)

# Initalize virtual display for pi
display = Display(visible=0, size=(800, 800))
display.start()
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()


# refresh the webpage
def refreshPage():
    driver.refresh()


# Switch the control to the Alert window
# use the accept() method to accept the alert
def alertHandler():
    time.sleep(1.5)
    alertAgent = driver.switch_to.alert
    alertAgent.accept()


# input NRIC, password and click on login
def loginPage():
    print("Keying in credentials")
    driver.find_element_by_xpath('//input[@id="txtNRIC"]').send_keys(data["username"])
    driver.find_element_by_xpath('//input[@id="txtPassword"]').send_keys(
        data["password"]
    )
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="loginbtn"]').click()


# Continue to send data to page despite page not secure warning
def continuePageNotSecure():
    time.sleep(2)
    driver.find_element_by_xpath('//button[@id="proceed-button"]').click()


# Select class 2b or 3a driving course, default is 2b
def courseSelection():
    print("[datetime.now()] Selecting course")
    time.sleep(2)
    driver.find_element_by_xpath('//input[@value="Submit"]').click()


# Select Pratical Training -> Booking tab from sidebar
def praticalTrainingBookingTab():
    print("[datetime.now()] Selecting booking tab")
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.NAME, "leftFrame"))
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td/table/tbody/tr[14]/td[3]/a"
    ).click()
    driver.switch_to.default_content()


# Select all month, all sessions and all days
def selectSessions(selectionRequired=True):
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    if selectionRequired == True:
        print("[datetime.now()] Selecting sessions")
        wait = WebDriverWait(driver, 5)
        wait.until(ec.element_to_be_clickable((By.NAME, "btnSearch")))
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[1]/input"
        ).click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[9]"
        ).click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td/table/tbody/tr[6]/td[2]/input"
        ).click()
        time.sleep(2)
    print("selecting session not required")
    driver.find_element_by_xpath('//input[@value="Search"]').click()
    try:
        alertHandler()
    except:
        print("[datetime.now()] No alert to dismiss")
    driver.switch_to.default_content()


# Goes through every row and every cell,
# and check if a radio button is present
def readAllRowCells():
    print("[datetime.now()] locating mainFrame..")
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    tableXPath = ""
    try:
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[10]/td/table/tbody"
        )
        tableXPath = (
            "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[10]/td/table/tbody"
        )
    except:
        pass
    try:
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[9]/td/table/tbody"
        )
        tableXPath = (
            "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[9]/td/table/tbody"
        )
    except:
        pass
    table = driver.find_element_by_xpath(tableXPath)

    print("[datetime.now()] found table")
    lessonList = {}
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "slot")))
    # iterate over all the rows
    for row in table.find_elements(By.TAG_NAME, "tr")[2:]:
        listOfAvailableSessions = []
        for index, obj in enumerate(row.find_elements(By.TAG_NAME, "td")):
            if index == 0:
                dateOfLesson = obj.text.split("\n")
            elif index == 1:
                pass
            else:
                # Check if session is selectable
                print(
                    "checking "
                    + dateOfLesson[0]
                    + " "
                    + dateOfLesson[1]
                    + "session "
                    + str(index - 1)
                )
                try:
                    if obj.find_element(By.TAG_NAME, "input"):
                        sessionNumber = index - 1
                        listOfAvailableSessions.append(sessionNumber)
                except:
                    pass
        print(listOfAvailableSessions)
        lessonList[dateOfLesson[0]] = listOfAvailableSessions
    driver.switch_to.default_content()
    return lessonList


# Construct message based to data available on the web,
# and send it out to the user via telegram
def analyseExtractedData(lessonList):
    dateToCheckTill = (
        datetime.today().date() + relativedelta(days=data["daysInAdvance"])
    )
    messageToBeSentFlag = False
    message = "Slots available:"
    for lessonListDatesKey in lessonList:
        dateOfSessions = datetime.strptime(lessonListDatesKey, "%d/%m/%Y").date()
        if dateOfSessions <= dateToCheckTill:
            # send notification to tele
            if lessonList[lessonListDatesKey] != []:
                message = AddDateDetailsToText(
                    message, dateOfSessions, dateOfSessions.strftime("%A")
                )
                messageToBeSentFlag = True
                for sessionNumber in lessonList[lessonListDatesKey]:
                    message = AddSessionDetailsToText(message, sessionNumber)
    message = AddWebsiteToText(message)
    if messageToBeSentFlag:
        telegramBot.sendMessage(message)

# Concatenate day and date of available sessions into the message
def AddDateDetailsToText(message, dateOfSession, dayOfSession):
    message += "\n\n" + dateOfSession.strftime("%d/%m/%Y") + " - " + dayOfSession
    return message

# Concatenate session number into the message
def AddSessionDetailsToText(message, sessionNumber):
    message += "\nSession " + str(sessionNumber) + ": " + sessionTimings(sessionNumber)
    return message

# Adds BBDC's link to end of the message for users' convenience
def AddWebsiteToText(message):
    message += "\n\nhttps://info.bbdc.sg/members-login/"
    return message

# keeps track of session timings in relation to session number
def sessionTimings(sessionNumber):
    if sessionNumber == 1:
        return "07:30 – 09:10"
    elif sessionNumber == 2:
        return "09:20 – 11:00"
    elif sessionNumber == 3:
        return "11:30 – 13:10"
    elif sessionNumber == 4:
        return "13:20 – 15:00"
    elif sessionNumber == 5:
        return "15:20 – 17:00"
    elif sessionNumber == 6:
        return "17:10 – 18:50"
    elif sessionNumber == 7:
        return "19:20 – 21:00"
    elif sessionNumber == 8:
        return "21:10 – 22:50"
    else:
        return "Error getting timing"

# Refreshes session availbility page
# Redirect to login portal page if current browser session has expired
def reloadSessionsAvailbility():
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    driver.find_element_by_xpath('//input[@name="btnBack"]').click()
    driver.switch_to.default_content()
    # Check if kicked out of session
    try:
        selectSessions(False)
        try:
            alertHandler()
        except:
            print("[datetime.now()] No alert to dismiss")
        analyseExtractedData(readAllRowCells())
    except:
        print("[datetime.now()] Session expired")
        telegramBot.sendMessage("Session expired, relogging in")
        driver.switch_to.default_content()
        driver.find_element_by_xpath(
            '//a[@href="https://info.bbdc.sg/members-login/"]'
        ).click()
        LogicalFullSteps()

# Logical steps taken from logging in till sending details to user 
def LogicalFullSteps():
    loginPage()
    continuePageNotSecure()
    courseSelection()
    praticalTrainingBookingTab()
    selectSessions()
    analyseExtractedData(readAllRowCells())


# Main Program
driver.get("https://info.bbdc.sg/members-login/")

# LogicalFullSteps()
# Idie of 3 minutes before attempting to get latest slot availbility
while True:
    print("Snoozing for 600 seconds")
    time.sleep(600)
    print("waking up from sleep")
    reloadSessionsAvailbility()

# alertHandler()
# analyseExtractedData(readAllRowCells())
