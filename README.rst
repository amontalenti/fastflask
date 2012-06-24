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
be if you pick some lightweigh technologies.

What does it do?
----------------

In order for this app to pass the "real-world" sniff test, I wanted to make
sure it displayed some meaningful, web-friendly data, did it in a nice way
(e.g. using hyperlinks and URLs appropriately), had a decent user interface,
and operated with a persistent database in a read/write basis.

So, the example app is called the "Fast Article Viewer", and its built by an
imaginary company called "FastCo". All the article viewer does right now is list 
articles that are in the database as HTML links, also showing the publication
date of those articles.

It also lets you submit new articles, which are validated and then displayed
along the others. Finally, it lets you search and display articles based on
their publication date.

Technical Design
----------------

I chose this because the model is simple: we are simply modeling web articles.
I chose to include publication date since showing real-world code using
Python's datetime, dateutil, and pytz is instructive. I seeded some test data
(in JSON format) from some publishers who post their content freely online, and
included a utility script (``loaddata.py``) that can help with bulk loading
this data for testing purposes and clearing out your existing DB.

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
listing interface and one for the submission form. The submission template is
also re-used for both plain submission form display and the one that reports
errors to the user.

Both the article listing interface and the form are styled using Bootstrap.
Most of the Bootstrap boilerplate is in a base Jinja template, thus leaving the
actual templates to be very free of noise.

Settings
--------

Due to the technologies chosen and the conventions used, there are relatively few settings for this project. They are all listed in ``settings.py`` and described here:

MONGO_HOST, MONGO_PORT
    These are your Mongo database settings. The ones listed here are the
    defaults for most systems.

MONGO_DATABASE
    This is the Mongo database that will be automatically created upon first
    use and will contain a single collection, ``articles``, with all the data
    being queried and inserted by this project. Defaults to ``fastco``.

STATIC
    This is the static directory location. Defaults to ``/static`` which is
    what the Flask development web server uses, but this will likely need to be
    customized for a production deployment with e.g. nginx and uwsgi.

MIN
    This is the "minified JavaScript/CSS" extension that is used for loading
    optimized forms of these assets. It is set to the empty string ``""`` by
    default, set to ``.min`` and the minified versions will be used.

