#LinkedBot.py
import argparse, os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import models
import random
#from pyvirtualdisplay import Display


def getPeopleLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if '/in/' in url:
				links.append(url)
	return links

def getJobLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if '/jobs' in url:
				links.append(url)
	return links

def getID(url):
	pUrl = urlparse(url)
	vai = str('https://www.linkedin.com'+str(pUrl))
	print(vai)
	return vai


def ViewBot(browser):
	visited = {}
	pList = []
	count = 0

	while True:
		#sleep to make sure everything loads, add random to make us look human.
		time.sleep(random.uniform(2.7,3.9))
		page = BeautifulSoup(browser.page_source, "lxml")
		people = getPeopleLinks(page)
		if people:
			for person in people:
				person = 'https://www.linkedin.com'+person
				if person not in visited:
					pList.append(person)
					visited[person] = 1
		if pList: #if there is people to look at look at them
			person = pList.pop(0)
			browser.get(person)
			count += 1
		else: #otherwise find people via the job pages
			browser.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")


			page = BeautifulSoup(browser.page_source, "lxml")
			people = getPeopleLinks(page)
			if people:
				for person in people:
					person = 'https://www.linkedin.com'+person
					if person not in visited:
						pList.append(person)
						visited[person] = 1
						connect = person+'connections/'
						browser.get(connect)
						page = BeautifulSoup(browser.page_source, "lxml")
						people = getPeopleLinks(page)
						if people:
							for person in people:
								person = 'https://www.linkedin.com'+person
								if person not in visited:
									pList.append(person)
									visited[person] = 1

			jobs = getJobLinks(page)
			if jobs:
				job = random.choice(jobs)
				root = 'http://www.linkedin.com'
				roots = 'https://www.linkedin.com'
				if root not in job or roots not in job:
					job = 'https://www.linkedin.com'+job
				browser.get(job)
			else:
				print("I'm Lost Exiting")
				break

		#Output (Make option for this)
		print(" - "+browser.title+" Visited!  ("+str(count)+"/"+str(len(pList))+")")
		with open("linkedin.txt", "a", encoding="utf-8") as text_file:
			text_file.write(str(person) + '\n')

def Main():
    print("iniciando...")
    # parser = argparse.ArgumentParser()
    # parser.add_argument("email", help="linkedin email")
    # parser.add_argument("password", help="linkedin password")
    # args = parser.parse_args()
    # print(args)
    #display.start()
    email,password = models.get_credentials('linkedin')
    browser = webdriver.Firefox()
    browser.get("https://linkedin.com/uas/login")
    emailElement = browser.find_element_by_id("username")
    print(emailElement)
    emailElement.send_keys(email)
    passElement = browser.find_element_by_id("password")
    passElement.send_keys(password)
    passElement.submit()
    os.system('cls')
    print("[+] Success! Logged In, Bot Starting!")
    ViewBot(browser)
    browser.close()

if __name__ == '__main__':
    Main()
