import json
import sys
import time
from datetime import datetime

import selenium.webdriver.support.expected_conditions as ec
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import telegramBot


# read json file
def readJSON():
    with open("./credentials.json") as f:
        data = json.load(f)
    return data


# refresh the webpage
def refreshPage(driver):
    driver.refresh()


# Switch the control to the Alert window
# use the accept() method to accept the alert
def alertHandler(driver):
    time.sleep(1.5)
    alertAgent = driver.switch_to.alert
    alertAgent.accept()


# input NRIC, password and click on login
def loginPage(driver):
    print(
        "["
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + "] "
        + "Keying in credentials"
    )
    driver.find_element_by_xpath('//input[@id="txtNRIC"]').send_keys(
        readJSON()["loginCredentials"]["username"]
    )
    driver.find_element_by_xpath('//input[@id="txtPassword"]').send_keys(
        readJSON()["loginCredentials"]["password"]
    )
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="loginbtn"]').click()


# Continue to send data to page despite page not secure warning
def continuePageNotSecure(driver):
    time.sleep(2)
    driver.find_element_by_xpath('//button[@id="proceed-button"]').click()


# Select class 2b or 3a driving course, default is 2b
def courseSelection(driver):
    print(
        "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "Selecting course"
    )
    time.sleep(2)
    driver.find_element_by_xpath('//input[@value="Submit"]').click()


# Select Pratical Training -> Booking tab from sidebar
def practicalTrainingBookingTab(driver):
    try:
        driver.find_element(By.NAME, "leftFrame")
    except:
        print("Unable to select practical booking tab")
        print("Is course selection page currently present?")
        print("If so change courseSelectionRequired value to 'true' in credentials.json")
        sys.exit(1)
    print(
        "["
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + "] "
        + "Selecting booking tab"
    )
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.NAME, "leftFrame"))
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td/table/tbody/tr[14]/td[3]/a"
    ).click()
    driver.switch_to.default_content()


# Select all month, all sessions and all days
def selectSessions(driver, selectionRequired=True):
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    if selectionRequired == True:
        print(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Selecting sessions"
        )
        wait = WebDriverWait(driver, 5)
        wait.until(ec.element_to_be_clickable((By.NAME, "btnSearch")))
        time.sleep(1)
        driver.find_element(By.NAME, "allMonth").click()
        time.sleep(1)
        driver.find_element(By.NAME, "allSes").click()
        time.sleep(1)
        driver.find_element(By.NAME, "allDay").click()
        time.sleep(2)
    else:
        print(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Selecting session not required"
        )
    driver.find_element(By.NAME, "btnSearch").click()
    try:
        alertHandler(driver)
    except:
        print(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "No alert to dismiss"
        )
    driver.switch_to.default_content()


# Goes through every row and every cell,
# and check if a radio button is present
def readAllRowCells(driver):
    print(
        "["
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + "] "
        + "Locating mainFrame.."
    )
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

    print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "Found table")
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
                    "["
                    + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    + "] "
                    + "Checking "
                    + dateOfLesson[0]
                    + " "
                    + dateOfLesson[1]
                    + " session "
                    + str(index - 1)
                )
                try:
                    if obj.find_element(By.TAG_NAME, "input"):
                        sessionNumber = index - 1
                        listOfAvailableSessions.append(sessionNumber)
                except:
                    pass
        print(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + str(listOfAvailableSessions)
            + " sessions available"
        )
        lessonList[dateOfLesson[0]] = listOfAvailableSessions
    driver.switch_to.default_content()
    return lessonList


# Construct message based to data available on the web,
# and send it out to the user via telegram
def analyseExtractedData(lessonList):
    dateToCheckTill = datetime.today().date() + relativedelta(
        days=readJSON()["generalSettings"]["checkNumberOfDaysInAdvance"]
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
def reloadSessionsAvailbility(driver):
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    driver.find_element_by_xpath('//input[@name="btnBack"]').click()
    driver.switch_to.default_content()
    # Check if kicked out of session
    try:
        selectSessions(driver, False)
        try:
            alertHandler(driver)
        except:
            print(
                "["
                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + "] "
                + "No alert to dismiss"
            )
        analyseExtractedData(readAllRowCells(driver))
    except:
        print(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Current session expired, relogging in"
        )
        telegramBot.sendMessage("Session expired, relogging in")
        driver.switch_to.default_content()
        driver.find_element_by_xpath(
            '//a[@href="https://info.bbdc.sg/members-login/"]'
        ).click()
        LogicalFullSteps()


# Logical steps taken from logging in till sending details to user
def LogicalFullSteps(driver):
    loginPage(driver)
    continuePageNotSecure(driver)
    if readJSON()["generalSettings"]["courseSelectionRequired"] == True:
        courseSelection(driver)
    practicalTrainingBookingTab(driver)
    selectSessions(driver)
    analyseExtractedData(readAllRowCells(driver))
