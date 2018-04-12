import os
import time
from sqlite3 import dbapi2 as sqlite3
from flask import abort ,Flask, g, request, render_template, redirect, url_for
import random
import json
import markov
import html

app = Flask(__name__)
# this may not be necessary
app.config['PROPAGATE_EXCEPTIONS'] = True

# declare global objects
filtered_tweets = []
cwd = os.path.dirname(os.path.realpath(__file__))
markov_obj = markov.Markov(cwd + "/raw_tweets_text.txt")

# set path to database
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'AlternativeTweetsLeaderboard.db')
))


# initialize the server
# @app.cli.command('init')
def init():
    print("Initializing...")
    init_db()
    init_tweets()
    init_fake_tweets()
    print("Initialized the server")


# initialize the database
def init_db():
    print("Initializing database")
    db = connect_db()
    with app.open_resource(cwd + '/schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()
    db.close()


# get the database connection for this context
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db


# make a database connection
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# close the database connection for this context
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# initialize Trump tweet corpus in cache
def init_tweets():
    print("Initializing tweets")
    raw_tweets_text = open(cwd + "/raw_tweets_text.txt", "w")
    for i in range(2011, 2018):
        with open(cwd + "/static/condensed_%d.json" % i) as raw_tweets_json:
            raw_tweets = json.load(raw_tweets_json)
            for tweet in raw_tweets:
                if not (tweet["is_retweet"]
                        or tweet["text"][0] == "@"
                        or "Thank you" in tweet["text"]
                        or "@realDonaldTrump" in tweet["text"]):
                    raw_tweets_text.write(
                        html.unescape(tweet["text"]).replace(".@", " @") + " ")
                    filtered_tweets.append(tweet)
    raw_tweets_text.close()


# initialize Markov chain generator
def init_fake_tweets():
    global markov_obj
    markov_obj = markov.Markov(cwd + "/raw_tweets_text.txt")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        db = get_db()
        db.execute('''insert into scores (pub_date, username, score)
            values (?, ?, ?)''',
                   (int(time.time()),
                    request.args.get("username"),
                    request.args.get("score")))
        db.commit()
        return redirect(url_for('leaderboard'))
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('select username,'
                         'score from scores order by score desc limit 10')
        entries = cur.fetchall()
        return render_template('leaderboard.html', entries=entries)
    abort(404)


@app.route('/question', methods=['GET'])
def get_tweet():
    if random.randint(0, 1) == 1:
        return random_real_tweet()
    else:
        return random_fake_tweet()


# return a random real tweet taken from Trump's corpus
# json format as follows:
# {
#    "tweet": "example text here",
#    "true_or_false: "true
# }
def random_real_tweet():
    raw_tweets_text = open(cwd + "/raw_tweets_text.txt", "w")
    for i in range(2011, 2018):
        with open(cwd + "/static/condensed_%d.json" % i) as raw_tweets_json:
            raw_tweets = json.load(raw_tweets_json)
            for tweet in raw_tweets:
                if not (tweet["is_retweet"]
                        or tweet["text"][0] == "@"
                        or "Thank you" in tweet["text"]
                        or "@realDonaldTrump" in tweet["text"]):
                    raw_tweets_text.write(html.unescape(tweet["text"])
                                          .replace(".@", " @") + " ")
                    filtered_tweets.append(tweet)
    raw_tweets_text.close()

    random_tweet_index = random.randint(0, len(filtered_tweets) - 1)
    data = {}
    data["tweet"] = html.unescape(filtered_tweets[random_tweet_index]["text"])\
        .replace('\"', "")
    data["true_or_false"] = "true"
    json_data = json.dumps(data)
    return json_data


# return a random fake tweet generated by the Markov chain
# json format as follows:
# {
#    "tweet": "example text here",
#    "true_or_false: "false"
# }
def random_fake_tweet():
    data = {}
    data["tweet"] = markov_obj.genTweet()
    data["true_or_false"] = "false"
    json_data = json.dumps(data)
    return json_data


init()
