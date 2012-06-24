from fastco import get_db, clear_articles, insert_article
import json
import sys

def load_data():
    data = json.load(open("data.json"))
    count = len(data)
    print "Found {count} fresh article entries to load".format(count=count)
    db = get_db()
    count = db.articles.count()
    print "Clearing {count} stale entries from collection".format(count=count)
    clear_articles()
    for article in data:
        db.articles.insert(article, safe=True)
    count = db.articles.count()
    print "{count} fresh article entries now in collection!".format(count=count)

def prompt():
    print "This will clear the existing article DB and load it from data.json!"
    print "Are you sure you want to continue? [y/N]",
    resp = raw_input()
    if resp.strip() == "y":
        load_data()
    else:
        print "Aborting."
        sys.exit(1)

if __name__ == "__main__":
    prompt()
