from datetime import datetime
from pymongo import Connection
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

class Article(object):
    def __init__(self, title, link, pub_date=None):
        self.title = title
        self.link = link
        self.pub_date = pub_date

    @property
    def html_link(self):
        link_fragment = """<a href="{link}">{title}</a>"""
        return link_fragment.format(**vars(self))

    @property
    def days_old(self):
        if self.pub_date is not None:
            return (datetime.now() - self.pub_date).days
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

def query_articles():
    db = get_db()
    for article in db.articles.find({}):
        yield Article(**article)

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
