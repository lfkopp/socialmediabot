import models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import shuffle
from bs4 import BeautifulSoup
import pandas as pd
from wget import download
from os import listdir

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


    def followers(self):
        bot = self.bot
        bot.get('https://www.instagram.com/'+ self.username +'/followers/')
        follower_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a').click()
        sleep(.3)
        content = bot.find_element_by_tag_name('body')
        content.send_keys(Keys.TAB)
        sleep(.3)
        content2 = bot.find_element_by_tag_name('body')
        content2.send_keys(Keys.TAB)
        l = 0
        len_lista = 1
        while l<15:
            content2 = bot.find_element_by_tag_name('body')
            content2.send_keys(Keys.ARROW_DOWN)
            lista=content2.find_elements_by_tag_name('li')
            if len(lista) == len_lista:
                l += 1
            else:
                l = 0
                print(len(lista))
            len_lista = len(lista)
            sleep(.4)
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        try:
            df = pd.read_pickle('follower.pickle')
        except:
            df = pd.DataFrame([],columns=['time_first','time_last','username','name','status','img'])
        follow_last = []
        now = pd.datetime.now()
        for item in soup.findAll('li', {"class": "wo9IH"}):
            #print(item)
            f = dict()
            f['username'] = item.find('a').get('href').replace('/','')
            f['img'] = item.find('img').get('src')
            f['status'] = item.find('button').text
            f['name'] = item.find('div', {"class": "wFPL8"}).text.replace('\n',' ')
            f['time_first'] = now
            f['time_last'] = now
            print('follower',f)
            if f['username'] not in df['username'].values:
                df = df.append([f], ignore_index=True, sort=False)
            else:
                df.loc[df[df['username'] == f['username']].index,'time_last'] = now
        df.to_pickle('follower.pickle')
        df.to_csv('follower.csv')

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

    def get_photos(self):
        df = pd.read_pickle('follower.pickle')
        has_img =  [str(x[:-4]) for x in listdir('photos/')]
        for index, row in df.iterrows():
            if row['username'] not in has_img:
                download(row['img'],'photos/'+row['username']+'.png')
                print('downloading photo: ',row['username'])
                sleep(1.5)


if __name__ == "__main__":
    insta = Instagram()
    insta.login()
    insta.followers()
    insta.get_photos()
    sleep(19)
    insta.curtir(30)
    sleep(240)
    words = ['hacker','engineering','technology','innovation','startup','brasilrugby','datascience','machinelearning','tkditf','taekwondoitf','riodejaneiro','climatechange','fluminensefc','ipanema','copacabana','computerscience','arduino','iot','internetofthings','jovemnerd','python']
    shuffle(words)
    for word in words[:7]:
        print('\n word: '+word,flush=True)
        insta.curtir_hashtag(word,1)
        sleep(140)
