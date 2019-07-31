import requests
import requests_html
import sys
import re
import webbrowser
import urllib
from selenium import webdriver

def getPhoto(urlString):
	r = requests.get(urlString)
	pageSource = r.text.split("\n")
	for imageSource in pageSource:
		imageUrl = getImageMeta(imageSource)
		if(imageUrl):
			imageName = getImageName(imageUrl)
			urllib.request.urlretrieve(imageUrl,imageName+'.jpg')
			break

def getImageMeta(inputURL):
	m = re.search('^    <meta property="og:image" content="(.*)" />',inputURL)
	if(m):
		return m.group(1)

def getImageHrefList(inputURL):
	m = re.findall('<a href="/p/(.*?)/">',inputURL)
	if(m):
		return m
	else:
		print("Nope. Not found.")

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

def getAllImageFromPage(profileUrl):
	browser = webdriver.Chrome()
	browser.get(profileUrl)
	innerHTML = browser.execute_script("return document.body.innerHTML")
	browser.quit()
	singlePostUrlList = getImageHrefList(innerHTML)
	for singleUrl in singlePostUrlList:
		urlString = 'https://www.instagram.com/p/' + singleUrl + '/'
		getPhoto(urlString)

getAllImageFromPage(sys.argv[1])
