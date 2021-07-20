bbdc (Bukit Batok Driving Centre)

Class 2B pratical slot availbility alert via telegram

libraries required:
- pip install selenium
- pip install webdriver-manager
- pip install python-dateutil
- pip install pyTelegramBotAPI
- pip install PyVirtualDisplay
- pip install xvfbwrapper

additional steps for linux environment:
sudo apt-get chromium-chromedriver
sudo apt-get install xvfb

features:
- Fully automated login
- Customizable number of days in advance you would like the bot to check
- Cusomizable deley period between each check
- Option to skip course selection page if necessary
- Sends you list of available slots to you based on preferences

Setup:
1) Make a copy of credentials sample.json and rename it to credentaials.json
2) fill in your particulars and bot details (refer to wiki for more info)
3) run script.py