#%%
import models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import shuffle
from bs4 import BeautifulSoup
import pandas as pd
from wget import download
from os import listdir

#%%
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
		self.not_now()

	def curtir(self,pages=10):
		bot = self.bot
		bot.get('https://www.instagram.com/?hl=pt-br')
		sleep(1)
		self.not_now()
		for i in range(pages):
			try:
				for x in bot.find_elements_by_class_name("_8-yf5 "):
					if x.get_attribute("aria-label") == "Curtir":
						if x.get_attribute("height") == '24':
							x.click()
							sleep(2)
				bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
				sleep(4)
			except Exception as e:
				print(e)
		
	def curtir_hashtag(self, hashtag, n=5, m=10):
		bot = self.bot
		links = models.get_shortcode(hashtag,n)
		shuffle(links)
		links = links[:m]
		for post in links:
			bot.get(post+'?hl=pt-br')
			sleep(2)
			for x in bot.find_elements_by_class_name("_8-yf5 "):
				sleep(.3)
				if x.get_attribute("aria-label") == "Curtir":
					if x.get_attribute("height") == '24':
						try:
							sleep(.5)
							x.click()
							sleep(1.4)
						except Exception as e:
							print(e)
						break

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
			bot.get('https://www.instagram.com/'+ user)
			sleep(.3)
			self.get_numbers(user,'get_follow')
		bot.get('https://www.instagram.com/'+ user +'/'+follow+'/')
		sleep(.3)
		self.not_now()
		if follow == 'followers':
			follow_link = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
			sleep(.3)
			content = bot.find_element_by_tag_name('body')
			content.send_keys(Keys.TAB)
			sleep(.3)
			content2 = bot.find_element_by_tag_name('body')
			content2.send_keys(Keys.TAB)
		else:
			follow_link = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
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

	def not_now(self):
		bot = self.bot
		try:
			bot.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
			print('not now')
		except:
			pass

	def follow_user(self, user):
		bot=self.bot
		bot.get('https://www.instagram.com/'+ user)
		sleep(.3)
		self.get_numbers(user,'follow')
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
		self.get_numbers(user,'unfollow')
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
				self.not_now()
				print(e)

	def get_numbers(self,user='',command=''):
		bot = self.bot
		sleep(.5)
		try:
			num_pubs = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[1]/*/span').text.replace('milhões','00000').replace('mil','00').replace('.','').replace(',','')
			num_followers = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/*/span').text.replace('milhões','00000').replace('mil','00').replace('.','').replace(',','')
			num_following = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/*/span').text.replace('milhões','00000').replace('mil','00').replace('.','').replace(',','')
			print(user,num_pubs,num_followers,num_following)
			bio = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[2]/h1').text.strip().replace(';',',')
			data = list([str(pd.datetime.now()),str(user),str(num_pubs),str(num_followers),str(num_following),str(command),str(bio)])
			with open('user_data.csv','a+') as f:
				f.write(';'.join(data) + '\n')
			return data
		except Exception as e:
			self.not_now()
			print('erro get_numbers',e)
			return 0,0,0,0


	def unfollow_not_followers(self,first=0,last=15):
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
				self.not_now()
				print('unfollow ',user)



#%%
print('iniciando')

if __name__ == "__main__":
	print('main')
	insta = Instagram()
	insta.login()
	sleep(3)
	try:
		insta.bot.find_element_by_xpath('//button[text()="Agora não"]').click()
		sleep(3)
		insta.bot.find_element_by_xpath('//button[text()="Agora não"]').click()
		sleep(3)
	except:
		pass
	insta.get_follow()
	insta.get_follow('following')
	#insta.unfollow_not_followers(last=15)
	#insta.follow_followers('cnaranha',20)
	insta.get_photos()
	insta.curtir(25)
	words = (['neo4j','hacker','engineering','technology','innovation','startup',
	'brasilrugby','datascience','machinelearning','tkditf','taekwondoitf',
	'riodejaneiro','climatechange','fluminensefc','ipanema','copacabana','running',
	'computerscience','arduino','iot','internetofthings','jovemnerd','python',
	'tbt','love','beautiful','fashion','love','rugby','fgv','ufrj','sustentavel',
	'sustentabilidade','sustainability','sustaintable','nofilter', 'phdlife'])
	shuffle(words)
	for word in words[:10]:
		print('\n word: '+word,flush=True)
		insta.curtir_hashtag(word,n=25,m=10)
		sleep(140)
	to_follow = ['assisvinicius','labnetnce','guanarugby','bravus_tkditf'] #,'cnaranha']
	for tf in to_follow:
		for f in ['followers','following']:
			print('get_follow ' + str(f) + ' ' + str(tf) )
			insta.get_follow(str(f), str(tf))


