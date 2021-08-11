import json
import threading
import time

import requests
import telebot

import BLL
import initlization


# sends message to user's telegram
def sendMessage(text, botID="", ChatID=""):
    if botID == "" and ChatID == "":
        bot = telebot.TeleBot(data["telegramCredentials"]["teleBotID"])
        bot.send_message(data["telegramCredentials"]["chatID"], text)
    elif botID != "" and ChatID != "":
        bot = telebot.TeleBot(botID)
        bot.send_message(ChatID, text)
    else:
        raise ValueError("Both botID and ChatID has to have a valid string")


# Make GET request to URL and parse HTTP response to JSON
def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    parsedJSON = json.loads(content)
    return parsedJSON


# Get last chat message sent from user
def getChatId(botID):
    try:
        BLL.printMessage("Attempting to connect to your device..")
        URL = "https://api.telegram.org/bot{}/getUpdates".format(botID)
        updates = getUrl(URL)
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        # text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return chat_id
    except:
        BLL.printMessage(
            "Unable to connect to your device. Be Sure to start the bot with '/start'."
        )
        BLL.printMessage("Retrying in 15 seconds")
        time.sleep(15)
        return None


def validateBotID(botID):
    # r = requests.get("https://api.telegram.org/bot"+ botID +"/getme")
    URL = "https://api.telegram.org/bot{}/getMe".format(botID)
    if getUrl(URL)["ok"] == True:
        return True
    else:
        return False
    # chatID = getChatId(URL)
    # send_message(URL, "text", chatID)


thread = threading.Thread(target=initlization.generateJSON())
thread.start()


# Reads json file
with open("./credentials.json") as f:
    data = json.load(f)

bot = telebot.TeleBot(data["telegramCredentials"]["teleBotID"])
