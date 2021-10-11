import os
import sys
import time
from datetime import datetime

import selenium.webdriver.support.expected_conditions as ec
import yaml
from dateutil.relativedelta import relativedelta
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import BLL
import telegramBot


# Print statements with date and time tag
def printMessage(message):
    print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message)


# Read preferences file
def readPreferences():
    with open(os.path.join("settings", "preferences.yaml"), encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# Read credentials file
def readCredentials():
    with open(os.path.join("settings", "credentials.yaml"), encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# Read session pratical lesson sessions file
def readLessonSessions():
    with open(os.path.join("practicalLessonSessions.yaml"), encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# Refresh the webpage
def refreshPage(driver):
    driver.refresh()


# Switch the control to the Alert window
# Use the accept() method to accept the alert
def alertHandler(driver):
    time.sleep(1.5)
    alertAgent = driver.switch_to.alert
    alertAgent.accept()


# Input NRIC, password and click on login
def loginPage(driver):
    BLL.printMessage("Keying in credentials")
    driver.find_element_by_xpath('//input[@id="txtNRIC"]').send_keys(
        readCredentials()["Login credentials"]["Login ID"]
    )
    driver.find_element_by_xpath('//input[@id="txtPassword"]').send_keys(
        readCredentials()["Login credentials"]["Password"]
    )
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="loginbtn"]').click()


# Continue to send data to page despite page not secure warning
def continuePageNotSecure(driver):
    time.sleep(2)
    driver.find_element_by_xpath('//button[@id="proceed-button"]').click()


# Select class 2b or 3a driving course, default is 2b
def courseSelection(driver):
    BLL.printMessage("Selecting course")
    time.sleep(2)
    try:
        courses = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr[1]/td/form/table/tbody/tr[3]/td/descendant::input")
        for course in range(len(courses)):
            courseSelected = driver.find_element_by_xpath(
        "/html/body/table[2]/tbody/tr[1]/td/form/table/tbody/tr[3]/td/input[" + str(course + 1) + "]")
            if "2B" in courseSelected.get_attribute("value"):
                courseSelected.click()
                break
        time.sleep(2)
        driver.find_element_by_xpath('//input[@value="Submit"]').click()
    except:
        BLL.printMessage("No course to select")
        pass


# Select Pratical Training -> Booking tab from sidebar
def practicalTrainingBookingTab(driver):
    BLL.printMessage("Selecting booking tab")
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.NAME, "leftFrame"))
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td/table/tbody/tr[14]/td[3]/a"
    ).click()
    driver.switch_to.default_content()


# Go to practical booking tab and count the number of subjects present
def countNumberOfAvailableSubjects(driver):
    practicalTrainingBookingTab(driver)
    time.sleep(3)
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    subjectCount = driver.find_elements_by_xpath(
        "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td[2]/descendant::input"
    )
    printMessage("Number of subjects currently present: " + str(len(subjectCount)))
    driver.switch_to.default_content()
    return len(subjectCount)


# Get the name of the currently selected subject name
def readSubjectSelected(driver, selectedSubject):
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    subjectName = driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td[2]/input["
        + str(selectedSubject)
        + "]"
    ).get_attribute("value")
    driver.switch_to.default_content()
    return subjectName


# Select all month, all sessions and all days
def selectSessions(driver, subjectSelection):
    subjectName = readSubjectSelected(driver, subjectSelection)
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td[2]/input["
        + str(subjectSelection)
        + "]"
    ).click()
    if driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td[2]/input["
        + str(subjectSelection)
        + "]"
    ).is_selected():
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
        BLL.printMessage("Selecting sessions")
        wait = WebDriverWait(driver, 5)
        wait.until(ec.element_to_be_clickable((By.NAME, "btnSearch")))
        time.sleep(1)
        driver.find_element(By.NAME, "allMonth").click()
        time.sleep(1)
        driver.find_element(By.NAME, "allSes").click()
        time.sleep(1)
        driver.find_element(By.NAME, "allDay").click()
        time.sleep(2)
        try:
            driver.find_element(By.NAME, "btnSearch").click()
        except StaleElementReferenceException as Exception:
            BLL.printMessage(
                "StaleElementReferenceException while trying to click on search button,finding element again."
            )
            time.sleep(2)
            driver.find_element(By.NAME, "btnSearch").click()
        try:
            alertHandler(driver)
        except:
            BLL.printMessage("No alert to dismiss")
        driver.switch_to.default_content()
        return True, subjectName
    else:
        driver.switch_to.default_content()
        return False, subjectName


# Goes through every row and every cell,
# and check if a radio button is present
def readAllRowCells(driver):
    BLL.printMessage("Locating mainFrame..")
    driver.switch_to.frame(driver.find_element(By.NAME, "mainFrame"))
    lessonList = {}
    tableXPath = ""
    count = 0
    while True:
        try:
            driver.find_element_by_xpath(
                "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr["
                + str(count)
                + "]/td/table/tbody"
            )
            tableXPath = (
                "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr["
                + str(count)
                + "]/td/table/tbody"
            )
            break
        except:
            if count == 100:
                break
            count += 1
    if tableXPath != "":
        table = driver.find_element_by_xpath(tableXPath)
        BLL.printMessage("Found table")
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.NAME, "slot"))
        )
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
                    BLL.printMessage(
                        "Checking "
                        + dateOfLesson[0]
                        + " "
                        + dateOfLesson[1]
                        + " session "
                        + str(index - 1)
                    )
                    try:
                        if obj.find_element(By.TAG_NAME, "input"):
                            sessionNumber = index - 1
                            if (
                                sessionNumber
                                in BLL.readPreferences()["Preferences"][
                                    "Include session's availbility in alert"
                                ]
                                and BLL.readPreferences()["Preferences"][
                                    "Include session's availbility in alert"
                                ][sessionNumber]
                                == True
                            ):
                                listOfAvailableSessions.append(sessionNumber)
                    except:
                        pass
            BLL.printMessage(str(listOfAvailableSessions) + " sessions available")
            lessonList[dateOfLesson[0]] = listOfAvailableSessions
    else:
        printMessage("No table found")
    driver.switch_to.default_content()
    return lessonList


# Construct message based to data available on the web,
# and send it out to the user via telegram
def analyseExtractedData(lessonList, subjectName):
    if len(lessonList) != 0:
        dateToCheckTill = datetime.today().date() + relativedelta(
            days=readPreferences()["Preferences"]["Check number of days in advance"]
        )
        messageToBeSentFlag = False
        message = "Subject No.: " + subjectName + "\n\n\nSlots available:"
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
                        message = AddSessionDetailsToText(
                            message, dateOfSessions, sessionNumber
                        )
        message = AddWebsiteToText(message)
        if messageToBeSentFlag:
            telegramBot.sendMessage(message)


# Concatenate day and date of available sessions into the message
def AddDateDetailsToText(message, dateOfSession, dayOfSession):
    message += "\n\n" + dateOfSession.strftime("%d/%m/%Y") + " - " + dayOfSession
    return message


# Concatenate session number into the message
def AddSessionDetailsToText(message, dateOfSessions, sessionNumber):
    message += "\nSession " + str(sessionNumber) + ": " + sessionTimings(sessionNumber)
    if isPeakSession(dateOfSessions, sessionNumber):
        message += "*"
    return message


# Adds BBDC's link to end of the message for users' convenience
def AddWebsiteToText(message):
    message += "\n\n*Peak Periods\n\nhttps://info.bbdc.sg/members-login/"
    return message


# keeps track of session timings in relation to session number
def sessionTimings(sessionNumber):
    if sessionNumber in readLessonSessions()["Session Timings"]:
        return readLessonSessions()["Session Timings"][sessionNumber]
    else:
        return "Error retrieving timing"


# Check if a particular session falls into peak period
def isPeakSession(date, sessionNumber):
    isPeak = False
    dayOfWeek = date.weekday()
    if dayOfWeek < 5:
        if (
            BLL.readLessonSessions()["Peak hour sessions"]["Weekdays"][sessionNumber]
            == "Peak"
        ):
            isPeak = True
    else:
        if (
            BLL.readLessonSessions()["Peak hour sessions"]["Weekends"][sessionNumber]
            == "Peak"
        ):
            isPeak = True
    return isPeak


# Refreshes session availbility page
# Redirect to login portal page if current browser session has expired
def reloadSessionsAvailbility(driver):
    # Check if kicked out of session
    try:
        subjectsAvailable = countNumberOfAvailableSubjects(driver)
        if subjectsAvailable == 0:
            raise Exception()
        for i in range(subjectsAvailable):
            practicalTrainingBookingTab(driver)
            selectedSubject = selectSessions(driver, i + 1)
            if selectedSubject[0] == True:
                analyseExtractedData(readAllRowCells(driver), selectedSubject[1])
            else:
                printMessage("Unable to select subject " + str(selectedSubject[1]))
                printMessage("Skipping check for subject " + str(selectedSubject[1]))

    except:
        if BLL.readPreferences()["Preferences"]["Notify on session expired"] == True:
            telegramBot.sendMessage("Session expired, relogging in")
        BLL.printMessage("Current session expired, relogging in")
        driver.switch_to.default_content()
        time.sleep(3)
        driver.get("https://info.bbdc.sg/members-login/")
        time.sleep(3)
        LogicalFullSteps(driver)
        time.sleep(3)


# Logical steps taken from logging in till sending details to user
def LogicalFullSteps(driver):
    loginPage(driver)
    try:
        alertHandler(driver)
        refreshPage(driver)
        LogicalFullSteps(driver)
        return
    except:
        pass
    continuePageNotSecure(driver)
    courseSelection(driver)
    # practicalTrainingBookingTab(driver)
    subjectsAvailable = countNumberOfAvailableSubjects(driver)
    for i in range(subjectsAvailable):
        practicalTrainingBookingTab(driver)
        selectedSubject = selectSessions(driver, i + 1)
        if selectedSubject[0] == True:
            analyseExtractedData(readAllRowCells(driver), selectedSubject[1])
        else:
            printMessage("Unable to select subject " + str(selectedSubject[1]))
            printMessage("Skipping check for subject " + str(selectedSubject[1]))
