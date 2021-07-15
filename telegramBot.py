import json
import telebot

# Reads json file
with open("./credentials.json") as f:
    data = json.load(f)

# sends message to user's telegram
def sendMessage(text):
    bot = telebot.TeleBot(data["teleBotID"])
    bot.send_message(data["chatID"], text)
