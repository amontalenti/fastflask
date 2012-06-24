from flask import Flask, render_template, request
from fastco import (query_articles, search_articles, insert_article)

app = Flask(__name__)

@app.route('/')
def index():
    articles = query_articles()
    return render_template('list.jinja2.html', 
                           articles=articles)

@app.route('/search/<query>')
def search(query):
    articles = search_articles(query)
    return render_template('list.jinja2.html', 
                           query=query, 
                           articles=articles)

@app.route('/submit/', methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        return do_submit()
    else:
        return render_template('submit.jinja2.html')

def do_submit():
    title = request.args["title"]
    link = request.args["link"]
    pub_date = request.args["pub_date"]
    if pub_date is not None:
        pub_date = date_parser.parse(pub_date)
    article = Article(title=title, link=link, pub_date=pub_date)
    insert_article(article)
    return render_template("inserted.jinja2.html", article=article)

def run_devserver():
    app.run(debug=True)

if __name__ == "__main__":
    run_devserver()
