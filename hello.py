from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)

import ConfigParser
import urllib
from readability.readability import Document
import xml.etree.ElementTree as ET

config = ConfigParser.RawConfigParser()
config.read('betterrs.cfg')

content_tags = ['description', 'summary', 'content']#, 'content:encoded']

ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
ET.register_namespace('taxo', 'http://purl.org/rss/1.0/modules/taxonomy/')
ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')

feeds = []
for section in config.sections():
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

@app.route('/')
def hello():
    return render_template('index.html', feeds=feeds)

@app.route('/feed/<feed_name>')
def deliver(feed_name):
    feed = getFeedByName(feed_name)
    feedTree = ET.fromstring(
                    urllib.urlopen(feed['url']).read() )
    
    for item in feedTree.findall('channel/item'):
        for tag in content_tags:
           if item.find(tag) != None:
               item.remove(item.find(tag))
        html = urllib.urlopen(item.find('link').text).read()
        description = ET.SubElement(item, 'description')
        description.text = Document(html).summary()
    
    return ET.tostring(feedTree)

if __name__ == '__main__':
    app.debug = True
    app.run()
