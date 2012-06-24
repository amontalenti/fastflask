from datetime import datetime
from dateutil import parser as date_parser
from pytz import UTC
from pymongo import Connection
from urllib2 import urlopen, URLError
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from jinja2 import Markup

class Article(object):
    def __init__(self, title, link, pub_date, _id=None):
        self.title = title
        self.link = link
        self.pub_date = pub_date
        if _id is not None:
            # just helps with MongoDB
            self._id = None

    @property
    def html_link(self):
        link_fragment = u"""<a href="{link}">{title}</a>"""
        return Markup(link_fragment.format(**vars(self)))

    @property
    def days_old(self):
        if self.pub_date is not None:
            pub_date = date_parser.parse(self.pub_date)
            return (datetime.now(UTC) - pub_date).days
        else:
            return None

    @property
    def readable_days_old(self):
        days_old = self.days_old
        if days_old is None:
            return ""
        if days_old == 1:
            return "1 day old"
        else:
            fmt = "{days_old} days old"
            return fmt.format(days_old=days_old)

_CONN = None
def get_mongo_connection():
    global _CONN
    if _CONN is None:
        _CONN = Connection(host=MONGO_HOST, port=MONGO_PORT)
    return _CONN

def get_db():
    return get_mongo_connection()[MONGO_DATABASE]

def query_articles(days_ago=None):
    db = get_db()
    for article in db.articles.find({}):
        article = Article(**article)
        if days_ago is not None:
            if article.days_old > days_ago:
                # skip this article, doesn't match date filter
                continue
        yield article

def search_articles(query):
    db = get_db()
    for article in db.articles.find({"title": {"$regex": query}}):
        yield Article(**article)

def insert_article(article):
    db = get_db()
    db.articles.insert(vars(article))

def clear_articles():
    db = get_db()
    db.articles.remove()

class InvalidSubmission(Exception):
    def __init__(self, errors=None):
        self.errors = errors

def validate_submission(params):
    errors = {}
    def err(id, msg):
        errors[id] = msg
    title = params["title"]
    title = title.strip()
    if len(title) < 2:
        err("title", "title must be > 2 characters")
    if len(title) > 150:
        err("title", "title may not be > 150 characters")
    link = params["link"]
    link = link.strip()
    try:
        opened = urlopen(link)
        link = opened.geturl()
    except (URLError, ValueError):
        err("link", "link could not be reached")
    # return normalized URL after following redirects
    pub_date = params["pub_date"]
    pub_date = pub_date.strip()
    if len(pub_date) == 0:
        err("pub_date", "publication date cannot be blank")
    else:
        try:
            pub_date = date_parser.parse(pub_date)
            pub_date = pub_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            err("pub_date", "publication date could not parse")
    # if any errors, raise exception
    if len(errors) > 0:
        raise InvalidSubmission(errors=errors)
    # if no errors, return Article instance
    article = Article(title=title, link=link, pub_date=pub_date)
    return article
