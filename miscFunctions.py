from datetime import datetime

def printMessage(message):
    print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message)