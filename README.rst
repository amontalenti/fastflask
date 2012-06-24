fastflask
---------

An example of using the Flask web framework for Python to build a web
application prototype.

This is the example application that goes with my `"Build a web app fast" blog
post`_ and my `fast-python-slides`_.

.. _"Build a web app fast" blog post: http://www.pixelmonkey.org/2012/06/14/web-app
.. _fast-python-slides: https://github.com/amontalenti/fast-python-slides

Rationale
---------

I am increasingly finding myself surrounding by people who want to learn how to
prototype web applications fast.

I wrote a blog post giving some pointers to Python, JavaScript, and HTML/CSS
resources for getting started. I also pointed readers toward the "big three"
Python web frameworks: Django, Tornado, and Flask. I suggested that for getting
started and rapidly prototyping an application, Flask was the way to go.

I also made some suggestions about UI frameworks (jQuery, Bootstrap) and some
suggestions about database (MongoDB to start off, upgrade as necessary).

This project is basically me turning all of those recommendations into a sample
project that you can clone and get started with quickly. I plan to use it as a
teaching tool -- in other words, this is how small a modern web application can
be if you pick some lightweight technologies.

What does it do?
----------------

In order for this app to pass the "real-world" sniff test, I wanted to make
sure it displayed some meaningful, web-friendly data, did it in a nice way
(e.g. using hyperlinks and URLs appropriately), had a decent user interface,
and operated with a persistent database in a read/write basis.

So, the example app is called the "Fast Article Viewer", and it's built by an
imaginary company called "FastCo". All the article viewer does right now is list 
articles that are in the database as HTML links, also showing the publication
date of those articles.

It also lets you submit new articles, which are validated and then displayed
along the others. Finally, it lets you search and display articles based on
their publication date.

Technical Design
----------------

The layout of the project is very straightforward. The core logic of FastCo's
backend is implemented in the Python module, ``fastco.py``. Some of this is
database-independent logic, such as the ``Article`` class and its associated
methods. There are also a few utility functions that make it easy to query the
MongoDB and retrieve ``Article`` instances from it. Finally, there is important
business logic such as the validation rules for valid article submissions.

The Flask web application is entirely contained in ``app.py``. I have tried to make 
this module focus entirely on the tasks of handling web requests. Thus, code related 
to the DB, business logic, and the model are imported via the ``fastco`` module.

I chose this problem space because the model is simple yet realistic: at
`Parse.ly`_, we deal with an only-slightly-more complex model every day.

.. _Parse.ly: http://parse.ly

I chose to include publication date since showing real-world code using
Python's ``datetime``, ``dateutil``, and ``pytz`` modules is instructive. I
seeded some test data (in JSON format) from some publishers who post their
content freely online, and included a utility script (``loaddata.py``) that can
help with bulk loading this data for testing purposes and clearing out your
existing DB.

The "write" part is the article submission interface, which is similar to
Reddit or Hacker News. It lets you submit a title, link, and pub_date for an
article, and this article gets stored in the database. There is some light
validation of the submission -- the link is validated using ``urllib2.urlopen``
and the publication date is parsed with ``dateutil`` to make sure it's correct.

To illustrate the notion of template re-use, there is a "plain" article listing
endpoint, an endpoint that lists articles since a certain number of days ago,
and a search interface. These are all implemented naively but are "good enough"
that you could see where the production implementations would end up. More
importantly, they are all implemented using the same template,
``list.jinja2.html``.

As a result of this, there are only two Jinja templates total -- one for the
listing interface and one for the submission form. The submission template
(``submit.jinja2.html``) is also re-used for both plain submission form display
and the one that reports errors to the user. Both templates demonstrate
template inheritance; the latter template also demonstrates re-use within a
single template via macros.

Both the article listing interface and the form are styled using Bootstrap.
Most of the Bootstrap boilerplate is in a base Jinja template, thus leaving the
actual templates to be very free of noise. All of the styling is achieved via 
pure HTML and CSS.

This is not a "model" web app
-----------------------------

This web app has quite a few mistakes in it. For example, there is a JSON
endpoint to illustrate the notion of adding an API to your application, but it
renders the JSON document from the full DB serialized in-memory. Obviously this
would crash with a big DB. I wasn't aiming to create the "model" web
application here. When I work through this app with my students, I'm going to
cover a lot of interesting things this app does wrong, specifically related to
things like handling big DBs, security issues, and even some code design
issues.

However, this app is nice and small: the web layer is about 100 lines of code,
the backend and model is about 100 lines, and there is a little more than a 100
lines of template code. A web app that does something meaningful in <500 lines
of code (without cheating "too much") using real-world technologies you could
go to production with -- that is is what I'm trying to demonstrate. Not the
perfect or most secure or most scalable web app.

Running
-------

To setup the project, create a virtualenv and then ``pip install -r reqs.txt``
into it.

To run, execute ``python app.py`` and the Flask development server will come up.

Run ``python loaddata.py`` to load some sample article data into your MongoDB.

If you want to run unit tests, install development dependencies with ``pip
install -r dev-reqs.txt`` and then run ``nosetests``.

Settings
--------

Due to the technologies chosen and the conventions used, there are relatively few settings for this project. They are all listed in ``settings.py`` and described here:

MONGO_HOST, MONGO_PORT
    These are your Mongo database settings. The ones listed here are the
    defaults for most systems.

MONGO_DATABASE
    This is the Mongo database that will be automatically created upon first
    use and will contain a single collection, ``"articles"``, with all the data
    being queried and inserted by this project. Defaults to ``"fastco"``.

STATIC
    This is the static directory location. Defaults to ``"/static"`` which is
    what the Flask development web server uses, but this will likely need to be
    customized for a production deployment with e.g. nginx and uwsgi.

MIN
    This is the "minified JavaScript/CSS" extension that is used for loading
    optimized forms of these assets. It is set to the empty string ``""`` by
    default, set to ``".min"`` and the minified versions will be used.

You can customize this ``settings.py`` setup easily by changing the main file
to have your production settings and changing ``localsettings.py``, a file you
add to your own install, to have your development settings. The latter is
automatically imported and any set configuration variables will override the
former.
