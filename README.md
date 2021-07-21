# BBDC (Bukit Batok Driving Centre)
## Class 2B pratical slot availbility alert via telegram

### features:
- Application is Unix and Windows ready
- Fully automated login
- Customizable number of days in advance you would like the bot to check
- Cusomizable delay period between each check
- Option to skip course selection page if necessary
- Sends you list of available slots to you based on preferences
- Automatic relogin when session expires

### Setup:
1) Install required libraries (List is below)
2) Run start.py 
3) Follow the prompts to fill in your particulars and bot details (refer to wiki for more info)

### libraries required: (Windows and Linux)
- pip install selenium
- pip install webdriver-manager
- pip install python-dateutil
- pip install pyTelegramBotAPI
- pip install PyVirtualDisplay
- pip install xvfbwrapper

#### additional requirement for linux environment:
- sudo apt-get install chromium-chromedriver
- sudo apt-get install xvfb
