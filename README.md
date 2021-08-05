# BBDC (Bukit Batok Driving Centre)
## Class 2B pratical slot availbility alert via telegram

### features:
- Application is suitable for Windows and Linux
- Fully automated login
- Customizable number of days in advance you would like the bot to check
- Cusomizable delay period between each check
- Option to skip course selection page if necessary
- Sends you list of available slots to you based on preferences
- Automatic relogin when session expires

### Setup:

#### For Windows
1) Install required libraries
    - pip install selenium
    - pip install webdriver-manager
    - pip install python-dateutil
    - pip install pyTelegramBotAPI
    - pip install PyVirtualDisplay
    - pip install xvfbwrapper
2) Run start.py 
3) Follow the prompts to fill in your particulars and bot details (refer to wiki for more info)

#### For Linux
1) Install required libraries
    - pip install selenium
    - pip install webdriver-manager
    - pip install python-dateutil
    - pip install pyTelegramBotAPI
    - pip install PyVirtualDisplay
    - pip install xvfbwrapper
3) Install required system libraries
    - sudo apt-get install chromium-chromedriver
    - sudo apt-get install xvfb
3) Run start.py 
4) Follow the prompts to fill in your particulars and bot details (refer to wiki for more info)