import models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Instagram:
    def __init__(self):
        self.bot = webdriver.Firefox()
    def login(self):
        bot = self.bot
        self.username,self.password = models.get_credentials('instagram')
        bot.get('https://www.instagram.com/accounts/login/')
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
        bot.get('https://www.instagram.com')
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
                bot.get(post)
                heart = bot.find_element_by_xpath('//article//section/span[1]/button/span[@aria-label="Curtir"]')
                sleep(2)
                heart.click()
                print('o',end='')
            except:
                print('.',end='')

insta = Instagram()
insta.login()

#insta.curtir(10)
#insta.curtir_hashtag('bitcoin',1)
# insta.curtir_hashtag('tkditf',1)
#insta.curtir_hashtag('internetofthings',1)
insta.curtir_hashtag('brasilrugby',1)


'''    def curtir(self,pages=0):
        bot = self.bot
        bot.get('https://www.instagram.com/')
        for i in range(0,pages):
            print(i)
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(3)
        for i in range(10):
            posts = bot.find_elements_by_class_name('fr66n')
            for post in posts:
                to_click = post.find_element_by_class_name('glyphsSpriteHeart__outline__24__grey_9')
                to_click.click()
                sleep(4)
'''
