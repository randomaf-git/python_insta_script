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
def getImageHrefList(inputURL):
	m = re.findall('<a href="/p/(.*?)/">',inputURL)
	if(m):
		return m
	else:
		print("Nope. Not found.")
#Function to determine how long to scroll and getting photo post url
def getImageDuration(duration,browser):
	timeout = time.time() + duration
	innerHTML = browser.execute_script("return document.body.innerHTML")
	postUrlList = getImageHrefList(innerHTML)
	while True:
		scrollPage(browser)
		innerHTML = browser.execute_script("return document.body.innerHTML")
		morePostUrlList = getImageHrefList(innerHTML)
		for postUrl in morePostUrlList:
			if postUrl not in postUrlList:
				postUrlList.append(postUrl)
		if time.time()>timeout:
			break
	return postUrlList
#Get the image meta content property for a single post
def getImageMeta(inputURL):
	m = re.search('^    <meta property="og:image" content="(.*)" />',inputURL)
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
				print(imageName)
				return imageName
			i = i-1
		return "local-filename.jpg"
	return "local-filename.jpg"
#Save the photo from a single post
def getPhoto(urlString):
	r = requests.get(urlString)
	pageSource = r.text.split("\n")
	for imageSource in pageSource:
		imageUrl = getImageMeta(imageSource)
		if(imageUrl):
			imageName = getImageName(imageUrl)
			urllib.request.urlretrieve(imageUrl,imageName+'.jpg')
			break

def getAllImageFromPage(profileUrl):
	options = Options()
	options.headless = True
	browser = webdriver.Chrome(chrome_options=options)
	browser.get(profileUrl)
	singlePostUrlList = getImageDuration(15,browser)
	browser.quit()
	print("getAllImageFromPage: Getting", len(singlePostUrlList), "amount of post")
	for singleUrl in singlePostUrlList:
		urlString = 'https://www.instagram.com/p/' + singleUrl + '/'
		getPhoto(urlString)




getAllImageFromPage(sys.argv[1])
