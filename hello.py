from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)

import ConfigParser
import urllib
from readability.readability import Document

config = ConfigParser.RawConfigParser()
config.read('betterrs.cfg')

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
    feed['content'] = urllib.urlopen(feed['url']).read()
    return feed['content']

if __name__ == '__main__':
    app.debug = True
    app.run()
