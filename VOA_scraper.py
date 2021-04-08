# Web scraper for VOA News - learningenglish.voanews.com
# "Learning English texts, MP3s and videos are in the public domain. You are allowed to reprint them for educational and commercial purposes, with credit to learningenglish.voanews.com"

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup

import json

pages = 1 # how many pages deep into each topic to go (usually about 6 articles per page)
          # this will append ?p=1 ?p=2 ?p=3 etc. to the urls when fetching articles

topicUrls = [
	{'url': "https://learningenglish.voanews.com/z/1579", 'topic': 'Science & Technology'},
	{'url': "https://learningenglish.voanews.com/z/986", 'topic': 'Arts & Culture'},
	{'url': "https://learningenglish.voanews.com/z/955", 'topic': 'Health & Lifestyle'}
]

# add more URLs based on how many pages I specify:
if pages > 1:
	for i in range(pages):
		for i in range(len(topicUrls)):
			print( "Got URL " + str(i+1) + " / " + str(pages))
			newUrl = {}
			newUrl['url'] = topicUrls[i]['url'] + "?p=" + str(i+1)
			newUrl['topic'] = topicUrls[i]['topic']  # (same topic)
			topicUrls.append(newUrl)


progress = 0


def getArticleLinks(url):

    # error handling:
   
    try:
        html = urlopen(url['url'])

    except HTTPError as e:   #error sent by the server (page not found, etc.)
        print(e)
        return "--nothing--"          # 'None' is a python object type

    except URLError as e:    #more serious, couldn't even reach server
        print('The server could not be found')
        return "--nothing--"

    # actual scraping:

    else:

        try:
            bs = BeautifulSoup(html.read(), 'html.parser')

            allArticleLinks = bs.find('ul',{'id':'articleItems'}).find_all('li')

            textArticleLinks = []

            # GET THE LINKS:

            for element in allArticleLinks:  # Filter out the audio-only articles, by finding those with no audio icon
            	if element.find('span',{'class':'ico'}) == None:  

            		link = {
            			'title': element.a['title'],
            			'url': 'https://learningenglish.voanews.com' + element.a['href'],
            			'topic': url['topic']
            		}

            		textArticleLinks.append(link)
            		

            return textArticleLinks

        except AttributeError as e:
            print("Attribute error")
            return "--nothing--"


def getText(link):  # this "link" object argument will be updated with the text and then returned back

    # error handling:
    try:
        html = urlopen(link['url'])

    except HTTPError as e:   #error sent by the server (page not found, etc.)
        print(e)
        return "--nothing--"          # 'None' is a python object type

    except URLError as e:    #more serious, couldn't even reach server
        print('The server could not be found')
        return "--nothing--"

    # actual scraping:

    else:
        try:
            bs = BeautifulSoup(html.read(), 'html.parser')
            paragraphs = bs.find('div',{'id':'article-content'}).div.find_all('p')

            paragraphs = paragraphs[1:]  # trim off the first sentence, which usually is just "No media source currently available"

            link['text'] = ''

            for p in paragraphs:
            	if '___________' in p.get_text():    # stop once it reaches the end where the vocab list is (there's a nice line separating this, so)
            		break
            	else:
            		link['text'] += p.get_text() + " "  # Doesn't make a new text string, just adds the text to the link object that already has a title, url, and topic
            
            global progress
            global allLinks
            progress += 1
            print(str(progress) + " / " + str(len(allLinks)) + " articles scraped")

            return link   # returns the "link" object back

        except AttributeError as e:
            print("Attribute error")
            return "--nothing--"



def makeFile(data, outputFile):

	with open(outputFile, 'w') as f:
		json.dump(data, f)
		print("Wrote " + str(len(data)) + " articles to " + outputFile)




#1. GET THE LINKS

allLinks = []

for url in topicUrls:
	topicLinks = getArticleLinks(url)
	for link in topicLinks:
		allLinks.append(link)

#2. GET THE TEXT
textObjects = [getText(link) for link in allLinks]

#3. SEND TO FILE:
makeFile(textObjects, "data2.json")






            
    

    


