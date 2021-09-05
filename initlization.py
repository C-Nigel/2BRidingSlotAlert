from datetime import datetime
import json
import os

# import BLL
import telegramBot


def generateJSON():
    if os.path.exists("./credentials.json"):
        pass
    else:
        f = open("./credentials.json", "w+")
        f.write(
            """ {
                "loginCredentials": {
                    "username": "",
                    "password": ""
                },
                "telegramCredentials": {
                    "teleBotID": "",
                    "chatID": ""
                },
                "generalSettings": {
                    "courseSelectionRequired": false,
                    "checkNumberOfDaysInAdvance": 7,
                    "refreshTimeIntervalInSeconds": 600
                }
            } """
        )
        f.close()

        with open("credentials.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["loginCredentials"]["username"] = input("Enter your BBDC login ID: ")
        data["loginCredentials"]["password"] = input("Enter your BBDC password: ")
        while True:
            botID = input("Enter your telegram bot ID (Case Sensitive): ")
            botIDIsValid = telegramBot.validateBotID(botID)
            if botIDIsValid == True:
                data["telegramCredentials"]["teleBotID"] = botID
                while True:
                    chatID = telegramBot.getChatId(botID)
                    if chatID != None:
                        break
                data["telegramCredentials"]["chatID"] = chatID
                telegramBot.sendMessage("Device successfully connected", botID, chatID)
                break
            else:
                print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "Bot ID provided is not valid")
        courseSelectionRequirement = input(
            "Does course selection page show after logging in? [Y/n] "
        )
        if courseSelectionRequirement.lower() == "y":
            data["generalSettings"]["courseSelectionRequired"] = True
        else:
            data["generalSettings"]["courseSelectionRequired"] = False

        with open("credentials.json", "w") as jsonFile:
            json.dump(data, jsonFile)
