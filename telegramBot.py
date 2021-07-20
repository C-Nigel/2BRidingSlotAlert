import json
import telebot

# Reads json file
with open("./credentials.json") as f:
    data = json.load(f)

bot = telebot.TeleBot(data["telegramCredentials"]["teleBotID"])

# sends message to user's telegram
def sendMessage(text):
    bot = telebot.TeleBot(data["telegramCredentials"]["teleBotID"])
    bot.send_message(data["telegramCredentials"]["chatID"], text)
