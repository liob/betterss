betterss
========
betterss is a rss proxy. It tries to integrate linked articles
directly into the rss feed. My motivation is to create betterss is to 
read the whole article in my feed aggregator.

betterss supports rss and atom feeds.


Requirements:
-------------
* Python
* [Flask]
* [BeautifulSoup] 4


Installation:
-------------
* satisfy dependencies

        pip install flask
        pip install beautifulsoup4

* clone Git repo

        git clone https://github.com/liob/betterss.git

* configure betterss

        cp betterss-template.cfg betterss.cfg
        vi betterss.cfg

* test betterss

        python betterss.py

    - open http://127.0.0.1:5000 with a web browser


### WSGI
todo


[Flask]: http://flask.pocoo.org/
[BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/
