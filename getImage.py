import requests
import requests_html
import time
import sys
import re
import webbrowser
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#Function to scroll the browser to the bottom of the page
def scrollPage(browser):
	pauseTime = 1
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(pauseTime)

#Get all the loaded image Href list on a profile page
def getPostHrefList(inputURL):
	m = re.findall('<a href="/p/(.*?)/">',inputURL)
	if(m):
		return m
	else:
		print("Nope. Not found.")

#Function to determine how long to scroll and getting photo post url
def getPostDuration(duration,browser):
	timeout = time.time() + duration
	innerHTML = browser.execute_script("return document.body.innerHTML")
	postUrlList = getPostHrefList(innerHTML)
	while True:
		scrollPage(browser)
		innerHTML = browser.execute_script("return document.body.innerHTML")
		morePostUrlList = getPostHrefList(innerHTML)
		for postUrl in morePostUrlList:
			if postUrl not in postUrlList:
				postUrlList.append(postUrl)
		if time.time()>timeout:
			break
	return postUrlList

#Get the image meta content property for a single post
def getImageMeta(pageSource):
	m = re.search('^    <meta property="og:image" content="(.*)" />',pageSource)
	if(m):
		return m.group(1)

#Get the video meta content property for a single post
def getVideoMeta(pageSource):
	m = re.search('^    <meta property="og:video" content="(.*)" />',pageSource)
	if(m):
		return m.group(1)

#Get the image name for a single post
def getImageName(imageMeta):
	m = re.search('//(.*).jpg',imageMeta)
	if(m):
		imageName = m.group(1)
		i = len(imageName)-1
		while(i>=0):
			if(imageName[i]=='/'):
				imageName = imageName[i+1:len(imageName)]
				imageName = imageName + '.jpg'
				print(imageName)
				return imageName
			i = i-1
		return "local-filename.jpg"
	return "local-filename.jpg"

#Get the video name for a single post
def getVideoName(videoMeta):
	m = re.search('//(.*).mp4',videoMeta)
	if(m):
		videoName = m.group(1)
		i = len(videoName)-1
		while(i>=0):
			if(videoName[i]=='/'):
				videoName = videoName[i+1:len(videoName)]
				videoName = videoName+'.mp4'
				print(videoName)
				return videoName
			i = i-1
		return "local-filename.mp4"
	return "local-filename.mp4"

#Save the content from a single post
def getPost(urlString):
	r = requests.get(urlString)
	pageSource = r.text.split("\n")
	for postSource in pageSource:
		postUrl = getVideoMeta(postSource)
		if(postUrl):
			videoName = getVideoName(postUrl)
			urllib.request.urlretrieve(postUrl,videoName)
			break
		else:
			postUrl = getImageMeta(postSource)
			if(postUrl):
				imageName = getImageName(postSource)
				urllib.request.urlretrieve(postUrl,imageName)

def loginInstagram(browser):
	username="mmrnt.17"
	password="qweasd123"
	browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
	browser.find_element_by_name('username').send_keys(username)
	browser.find_element_by_name('password').send_keys(password)
	browser.find_element_by_xpath('//button[@type="submit"]').click()
	time.sleep(5) #Wait for login to finish
	return browser

def getAllPostFromPage(profileUrl, skipPost=0):
	options = Options()
	options.headless = True
	browser = webdriver.Chrome(chrome_options=options)
	#browser = loginInstagram(browser)
	browser.get(profileUrl)
	singlePostUrlList = getPostDuration(5,browser)
	print("getAllPostFromPage: Getting", len(singlePostUrlList), "amount of post")
	print("getAllPostFromPage: Skipping", skipPost, "amount of post")
	i = 1
	for singleUrl in singlePostUrlList:
		if i > skipPost:
			urlString = 'https://www.instagram.com/p/' + singleUrl + '/'
			getPost(urlString)
		i = i + 1

if len(sys.argv) == 3:
		profilePage = sys.argv[1]
		skipPost = sys.argv[2]
		getAllPostFromPage(profilePage,skipPost)
elif len(sys.argv) == 2:
		profilePage = sys.argv[1]
		getAllPostFromPage(profilePage)
