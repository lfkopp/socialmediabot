import models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import shuffle

class Instagram:
    def __init__(self):
        self.bot = webdriver.Firefox()
    def login(self):
        bot = self.bot
        self.username,self.password = models.get_credentials('instagram')
        bot.get('https://www.instagram.com/accounts/login/?hl=pt-br')
        sleep(3)
        username = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        sleep(3)
        try:
            bot.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
            sleep(0.3)
        except:
            pass


    def curtir(self,pages=10):
        bot = self.bot
        bot.get('https://www.instagram.com/?hl=pt-br')
        curtida = 0
        while curtida < pages:
            print(curtida)
            sleep(4)
            try:
                bot.find_element_by_xpath('//article//section/span[1]/button/span[@aria-label="Curtir"]').click()
                curtida +=1
            except Exception as e:
                print(e)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')



    def curtir_hashtag(self, hashtag, n=5):
        bot = self.bot
        links = models.get_shortcode(hashtag,n)
        for post in links:
            sleep(3)
            try:
                bot.get(post+'?hl=pt-br')
                heart = bot.find_element_by_xpath('//article//section/span[1]/button/span[@aria-label="Curtir"]')
                sleep(2)
                heart.click()
                print('o',end='',flush=True)
            except:
                print('.',end='',flush=True)

insta = Instagram()
insta.login()

sleep(19)
insta.curtir(30)
sleep(240)
words = ['brasilrugby','datascience','machinelearning','tkditf','taekwondoitf','riodejaneiro','climatechange','fluminensefc','ipanema','copacabana','computerscience','arduino','iot','internetofthings','jovemnerd','python']
shuffle(words)
for word in words[:7]:
    print('\n word: '+word,flush=True)
    insta.curtir_hashtag(word,1)
    sleep(240)
