betterrs
========
betterrs is a rss proxy. It tries to integrate linked articles
directly into the rss feed. My motivation is to create betterrs is to 
read the whole article in my feed aggregator.

betterrs supports rss and atom feeds.


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

        git clone https://github.com/liob/betterrs.git

* configure betterrs

        cp betterrs-template.cfg betterrs.cfg
        vi betterrs.cfg

* test betterrs

        python betterrs.py

    - open http://127.0.0.1:5000 with a web browser


### WSGI
todo


[Flask]: http://flask.pocoo.org/
[BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/
