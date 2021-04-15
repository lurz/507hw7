#######################
#### Renzhong Lu   ####
#### lurz          ####
#######################

from flask import Flask
import flask
import requests
import json
import secrets

API_KEY = secrets.API_KEY
app = Flask(__name__)


@app.route('/')
def index():
    '''Return index page

    Parameters
    ----------
    None

    Returns
    -------
    flask template
    '''
    return flask.render_template("index.html")


@app.route('/name/<username>')
def name(username=None):
    '''Return name page

    Parameters
    ----------
    username : string
        name to show at top

    Returns
    -------
    flask template
    '''
    return flask.render_template("name.html", name=username)


def fetch():
    '''Fetch top stories from nyt API.

    Parameters
    ----------
    None

    Returns
    -------
    dict:
        data from nyt API
    '''
    params = {'api-key': API_KEY}
    response = requests.get(
        'https://api.nytimes.com/svc/topstories/v2/technology.json',
        params=params)
    return json.loads(response.text)


@app.route('/headlines/<username>')
def headlines(username=None):
    '''Return headline page

    Parameters
    ----------
    username : string
        name to show at top

    Returns
    -------
    flask template
    '''
    data = fetch()

    context = {}
    context['name'] = username
    context['headlines'] = []
    max_range = 5 if data['num_results'] > 5 else data['num_results']
    for i in range(0, max_range):
        context['headlines'].append(data['results'][i]['title'])

    return flask.render_template("headlines.html", **context)


@app.route('/links/<username>')
def links(username=None):
    '''Return headline page with links

    Parameters
    ----------
    username : string
        name to show at top

    Returns
    -------
    flask template
    '''
    data = fetch()

    context = {}
    context['name'] = username
    context['headlines'] = []
    max_range = 5 if data['num_results'] > 5 else data['num_results']
    for i in range(0, max_range):
        context['headlines'].append(
            {'title': data['results'][i]['title'], 'url': data['results'][i]['url']})

    return flask.render_template("links.html", **context)


@app.route('/images/<username>')
def images(username=None):
    '''Return headline page with images

    Parameters
    ----------
    username : string
        name to show at top

    Returns
    -------
    flask template
    '''
    data = fetch()

    context = {}
    context['name'] = username
    context['headlines'] = []
    max_range = 5 if data['num_results'] > 5 else data['num_results']
    for i in range(0, max_range):
        context['headlines'].append(
            {
                'title': data['results'][i]['title'],
                'url': data['results'][i]['url'],
                'img': data['results'][i]["multimedia"][1]['url']})

    return flask.render_template("images.html", **context)


if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)
