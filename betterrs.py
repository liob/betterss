from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)

import os, sys
from hashlib import md5
import ConfigParser
import urllib
from bs4 import BeautifulSoup

config = ConfigParser.RawConfigParser()
config.read('betterrs.cfg')

tmp_folder = config.get('GLOBAL', 'tmp_folder')
if not os.path.isdir(tmp_folder):
    sys.exit('tmp_folder: %s does not exist' % tmp_folder)

content_tags = ['description', 'summary', 'content', 'content:encoded']

feeds = []
for section in config.sections():
    if section == 'GLOBAL':
        continue
    feed = {}
    feed['name'] = section
    try:
        feed['url'] = config.get(section, 'feed')
        feeds.append(feed)
    except:
        pass

def getFeedByName(name):
    feedlst = [feed for feed in feeds if feed['name'] == name]
    if feed:
        return feedlst[0]
    else:
        return None

def getHTML(url):
    tmpfile = os.path.join(tmp_folder, md5(url).hexdigest())
    try:
        f = open(tmpfile, 'r')
        return f.read()
    except:
        html = urllib.urlopen(url).read()
        f = open(tmpfile, 'w')
        f.write(html)
        return html

def differentiate(html, clean=False):
    rdiv = {'counter': 0,
            'div': None}
    soup = BeautifulSoup(html)
    for div in soup.find_all('div'):
        counter = 0
        if div.string:
            counter += len(div.string)
        for p in div.find_all('p', recursive=False):
            counter += len(p.get_text(strip=True))
        if rdiv['counter'] < counter:
            rdiv['counter'] = counter
            rdiv['div'] = div
    if clean:
        for element in rdiv['div'].findAll():
            if element.name not in allowedTags:
                print "stripping: %s" % element.name
                element.extract()
    return rdiv['div']

@app.route('/')
def hello():
    return render_template('index.html', feeds=feeds)

@app.route('/feed/<feed_name>')
def deliver(feed_name):
    feed = getFeedByName(feed_name)
    feedTree = BeautifulSoup(
                    urllib.urlopen(feed['url']).read(), 'xml' )
    
    for item in feedTree.find_all(['item', 'entry']):
        # remove content from feed
        [x.extract() for x in item.find_all(content_tags)]
        html = getHTML(item.find('link').string)
        description = feedTree.new_tag('description')
        content = feedTree.new_tag('content')
        item.append(description)
        item.append(content)
        differentiated = differentiate(html)
        # remove title if in payload
        [x.extract() for x in differentiated.find_all(text=item.find('title').string)]
        description.append(unicode(differentiated))
        
    return unicode(feedTree.prettify())

if __name__ == '__main__':
    app.debug = True
    app.run()
