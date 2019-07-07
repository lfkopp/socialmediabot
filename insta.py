import models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Instagram:
    def __init__(self):
        self.username,self.password = models.get_credentials('instagram')
        self.bot = webdriver.Firefox()
    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        sleep(3)
        username = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

insta = Instagram()
insta.login()
