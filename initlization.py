import json
import os


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
        data["telegramCredentials"]["teleBotID"] = input("Enter your telegram bot ID: ")
        data["telegramCredentials"]["chatID"] = input("Enter your telegram chat ID: ")
        courseSelectionRequirement = input(
            "Does course selection page show after logging in?[Y/n] "
        )
        if courseSelectionRequirement == "y" or courseSelectionRequirement == "Y":
            data["generalSettings"]["courseSelectionRequired"] = True
        else:
            data["generalSettings"]["courseSelectionRequired"] = False

        with open("credentials.json", "w") as jsonFile:
            json.dump(data, jsonFile)
