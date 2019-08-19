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
            #print(curtida)
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

    def get_photos(self):
        follower = pd.read_pickle('followers.pickle')
        following = pd.read_pickle('following.pickle')
        people = follower.append(following, ignore_index=True)
        people.drop_duplicates('username',inplace=True)
        has_img =  [str(x[:-4]) for x in listdir('photos/')]
        for index, row in people.iterrows():
            if row['username'] not in has_img:
                download(row['img'],'photos/'+row['username']+'.png')
                print('downloading photo: ',row['username'])
                sleep(1.5)

    def get_follow(self, follow='followers', user=''):
        bot=self.bot
        if user == '':
            pickle_file = follow+'.pickle'
            csv_file = follow+'.csv'
            user = self.username
        else:
            pickle_file = follow+'/'+str(user)+'.pickle'
            csv_file = follow+'/'+str(user)+'.csv'
        bot.get('https://www.instagram.com/'+ user +'/'+follow+'/')
        sleep(.3)
        if follow == 'followers':
            follow_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a').click()
            sleep(.3)
            content = bot.find_element_by_tag_name('body')
            content.send_keys(Keys.TAB)
            sleep(.3)
            content2 = bot.find_element_by_tag_name('body')
            content2.send_keys(Keys.TAB)
        else:
            follow_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a').click()
            sleep(.3)
            content = bot.find_element_by_tag_name('body')
            content.send_keys(Keys.TAB)
            sleep(.3)
            content6 = bot.find_element_by_tag_name('body')
            content6.send_keys(Keys.TAB)
            content3 = bot.find_element_by_tag_name('body')
            content3.send_keys(Keys.TAB)
            content4 = bot.find_element_by_tag_name('body')
            content4.send_keys(Keys.TAB)
            content5 = bot.find_element_by_tag_name('body')
            content5.send_keys(Keys.TAB)
            content2 = bot.find_element_by_tag_name('body')
            content2.send_keys(Keys.TAB)
        l = 0
        len_lista = 1
        while l<35:
            sleep(.5)
            content2 = bot.find_element_by_tag_name('body')
            content2.send_keys(Keys.PAGE_DOWN)
            lista=content2.find_elements_by_tag_name('li')
            if len(lista) == len_lista:
                l += 1
                sleep(1)
            else:
                l =0
                print('.',end='',flush=True)
            len_lista = len(lista)
            sleep(.2)
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        try:
            df = pd.read_pickle(pickle_file)
        except:
            df = pd.DataFrame([],columns=['time_first','time_last','username','name','status','img'])
        follow_last = []
        now = pd.datetime.now()
        for item in soup.findAll('li', {"class": "wo9IH"}):
            try:
                f = dict()
                f['username'] = item.find('a').get('href').replace('/','')
                f['img'] = item.find('img').get('src')
                f['status'] = item.find('button').text
                f['name'] = item.find('div', {"class": "wFPL8"}).text.replace('\n',' ')
                f['time_first'] = now
                f['time_last'] = now
                if f['username'] not in df['username'].values:
                    df = df.append([f], ignore_index=True, sort=False)
                else:
                    df.loc[df[df['username'] == f['username']].index,'time_last'] = now
            except:
                print('erro')
        df.to_pickle(pickle_file)
        df.to_csv(csv_file)

    def follow_user(self, user):
        bot=self.bot
        bot.get('https://www.instagram.com/'+ user)
        sleep(.3)
        try:
            follow_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
            if "Seguir" in follow_link.text:
                sleep(.3)
                follow_link.click()

        except:
            follow_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/button')
            if "Seguir" in follow_link.text:
                sleep(.3)
                follow_link.click()
        sleep(1)
        print("Following ", user)


    def unfollow_user(self, user):
        bot=self.bot
        bot.get('https://www.instagram.com/'+ user)
        sleep(.3)
        unfollow_link = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        if "Seguindo" in unfollow_link.text:
            unfollow_link.click()
            sleep(.3)
            unfollow_confirm = bot.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
            sleep(.3)
            unfollow_confirm.click()
            sleep(3)
            print("Unfollowing ", user)
        else:
            print("erro ",unfollow_link.text,user)

    def follow_followers(self,user,num=30):
        bot=self.bot
        user_db = pd.read_pickle('followers/'+user+'.pickle')
        following = pd.read_pickle('following.pickle')
        followers = pd.read_pickle('followers.pickle')
        people = following['username'].append(followers['username']).drop_duplicates().values
        users = user_db.username.values
        users_clean = [x for x in users if x not in people]
        shuffle(users_clean)
        for u in users_clean[:num]:
            try:
                self.follow_user(u)
                sleep(3)
            except Exception as e:
                print(e)

    def unfollow_not_followers(self,first=0,last=50):
        bot=self.bot
        following = pd.read_pickle('following.pickle')
        follower = pd.read_pickle('followers.pickle')
        following = following.sort_values('time_first')
        following_not_follower = [x for x in following[following['time_last'] == max(following['time_last'])]['username'].values if x  not in follower['username'].values ]
        for user in following_not_follower[first:last]:
            try:
                self.unfollow_user(user)
                sleep(.3)
            except:
                print('unfollow ',user)

if __name__ == "__main__":
    insta = Instagram()
    insta.login()
    insta.get_follow()
    insta.get_follow('following')
    insta.unfollow_not_followers(last=20)
    insta.follow_followers('cnaranha',20)
    insta.get_photos()
    insta.curtir(15)
    words = (['hacker','engineering','technology','innovation','startup',
    'brasilrugby','datascience','machinelearning','tkditf','taekwondoitf',
    'riodejaneiro','climatechange','fluminensefc','ipanema','copacabana',
    'computerscience','arduino','iot','internetofthings','jovemnerd','python',
    'tbt','love','beautiful','fashion','love','rugby','fgv','ufrj','sustentavel',
    'sustentabilidade','sustainability','sustaintable','nofilter'])
    shuffle(words)
    for word in words[:5]:
        print('\n word: '+word,flush=True)
        insta.curtir_hashtag(word,1)
        sleep(140)
    exit()
    to_follow = ['','labnetnce','guanarugby','bravustkitf','cnaranha']
    for tf in to_follow:
        for f in ['followers','following']:
            break
            print('get_follow ' + str(f) + ' ' + str(tf) )
            insta.get_follow(str(f), str(tf))
