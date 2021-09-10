import os
from datetime import datetime

import yaml

import BLL
import telegramBot


# Creates a new settings.yaml file with contents if file does not exist
def generateSettingsTemplate():
    if not os.path.exists(os.path.join("settings", "preferences.yaml")):
        settingsTemplate = {
            "Preferences": {
                "Course selection required": False,
                "Check number of days in advance": 7,
                "Refresh time interval": 600,
                "Notify on session expired": True,
                "Include session's availbility in alert": {
                    1: True,
                    2: True,
                    3: True,
                    4: True,
                    5: True,
                    6: True,
                    7: True,
                    8: True,
                },
            },
        }

        courseSelectionRequirement = input(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Does course selection page show after logging in? [Y/n]: "
        )
        if courseSelectionRequirement.lower() == "y":
            settingsTemplate["Preferences"]["Course selection required"] = True
        elif courseSelectionRequirement.lower() == "n":
            settingsTemplate["Preferences"]["Course selection required"] = False
        else:
            BLL.printMessage("Course selection page setting has been set to False")
            settingsTemplate["Preferences"]["Course selection required"] = False

        if not os.path.exists(os.path.join("settings")):
            os.mkdir(os.path.join("settings"))
        with open(
            os.path.join("settings", "preferences.yaml"), "w", encoding="utf-8"
        ) as File:
            yaml.dump(settingsTemplate, File)


# Creates a new credentials.yaml file with user inputs if file does not exist
def generateCredentialsTemplate():
    if not os.path.exists(os.path.join("settings", "credentials.yaml")):
        credentialsTemplate = {
            "Login credentials": {"Login ID": None, "Password": None},
            "Telegram credentials": {"telegram bot ID": None, "Chat ID": None},
        }

        credentialsTemplate["Login credentials"]["Login ID"] = input(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Enter your BBDC login ID: "
        )
        credentialsTemplate["Login credentials"]["Password"] = input(
            "["
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "] "
            + "Enter your BBDC password: "
        )

        while True:
            botID = input(
                "["
                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + "] "
                + "Enter your telegram bot ID (Case Sensitive): "
            )
            botIDIsValid = telegramBot.validateBotID(botID)
            if botIDIsValid == True:
                credentialsTemplate["Telegram credentials"]["telegram bot ID"] = botID
                while True:
                    chatID = telegramBot.getChatId(botID)
                    if chatID != None:
                        break
                credentialsTemplate["Telegram credentials"]["Chat ID"] = chatID
                telegramBot.sendMessage("Device successfully connected", botID, chatID)
                BLL.printMessage("Device successfully connected")
                break
            else:
                BLL.printMessage("Bot ID provided is not valid")

        if not os.path.exists(os.path.join("settings")):
            os.mkdir(os.path.join("settings"))
        with open(
            os.path.join("settings", "credentials.yaml"), "w", encoding="utf-8"
        ) as File:
            yaml.dump(credentialsTemplate, File)
