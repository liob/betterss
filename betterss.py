from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)

import os, sys
from hashlib import md5
import ConfigParser
import urllib
from bs4 import BeautifulSoup

config = ConfigParser.RawConfigParser()
config.read('betterss.cfg')

tmp_folder = config.get('GLOBAL', 'tmp_folder')
if not os.path.isdir(tmp_folder):
    sys.exit('tmp_folder: %s does not exist' % tmp_folder)

try:
    debug = config.getboolean('GLOBAL', 'debug')
    if debug:
        app.debug = True
except ConfigParser.NoOptionError:
    debug = False

content_tags = ['description', 'summary', 'content', 'encoded']
allowed_tags = ['br', 'p', 'a', 'img', 'li', 'em', 'ul', 'span',
                'h1', 'h2', 'h3', 'h4', 'h5',
                'div', 'strong', 'i',
                'table', 'td', 'tr']

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
    try:
        feed['clean'] = config.getboolean(section, 'clean')
    except ConfigParser.NoOptionError:
        feed['clean'] = True

def getFeedByName(name):
    feedlst = [feed for feed in feeds if feed['name'] == name]
    if feed:
        return feedlst[0]
    else:
        return None

def getHTML(url):
    if debug:
        print 'getting url: %s' % url
    return urllib.urlopen(url).read()

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
            if element.name not in allowed_tags:
                if debug:
                    print "stripping: %s" % element.name
                element.extract()
    return rdiv['div']

def cachedDifferentiate(url, clean=False):
    tmpfile = os.path.join(tmp_folder, md5(url).hexdigest())
    try:
        f = open(tmpfile, 'r')
        return BeautifulSoup(f, 'xml' )
    except:
        html = getHTML(url)
        differentiated = differentiate(html, clean)
        f = open(tmpfile, 'w')
        f.write(unicode(differentiated).encode("utf8"))
        return differentiated

@app.route('/')
def index():
    return render_template('index.html', feeds=feeds)

@app.route('/feed/<feed_name>')
def deliver(feed_name):
    feed = getFeedByName(feed_name)
    feedTree = BeautifulSoup( getHTML(feed['url']), 'xml' )
    type = False
    
    for item in feedTree.find_all(['item', 'entry']):
        if item.name == 'item':
            type = 'rss'
        if item.name == 'entry':
            type = 'atom'
        # remove content from feed
        [x.extract() for x in item.find_all(content_tags)]
        
        article_link = item.find('link').string
        if not article_link:
            article_link = item.find('link').get('href')
        if article_link:
            differentiated = cachedDifferentiate(article_link, feed['clean'])
            # remove title if in payload
            [x.extract() for x in differentiated.find_all(text=item.find('title').string)]
        else:
            raise Exception('article link not found in feed %s: %s' % (feed_name, feed['url']))
        
        if type == 'rss':
            description = feedTree.new_tag('description')
            item.append(description)
            description.append(unicode(differentiated))
        
        if type == 'atom':
            content = feedTree.new_tag('content')
            item.append(content)
            content.append(unicode(differentiated))
            
    if type == 'atom':
        feedTree.find('feed').attrs['xmlns'] = 'http://www.w3.org/2005/Atom'
    return unicode(feedTree)

if __name__ == '__main__':
    app.debug = True
    app.run()
