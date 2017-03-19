import os
import time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, request
import random
import json
import urllib2

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'AlternativeTweetsLeaderboard.db')
    ))

@app.cli.command('init')
def init():
    print "Initializing..."
    init_db()
    init_tweets()
    if not hasattr(g, 'cur_id'):
        g.cur_id = 1
    print "Initialized the server"

def init_db():
    print "Initializing database"
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()

def init_tweets():
    print "Testing tweets"
    print random_real_tweet()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.teardown_appcontext
def reset_id(error):
    if hasattr(g, 'cur_id'):
        g.cur_id = 1

@app.route('/leaderboard', methods=['GET', 'POST'])
def update_leaderboard():
    get_db()
    if request.method == 'POST':
        g.sqlite_db.execute('''insert into scores (pub_date, username, score)
            values (?, ?, ?)''',
            (int(time.time()), request.form['username'], request.form['score']))
        g.sqlite_db.commit()
        return 'done'
    if request.method == 'GET':
        return render_template('leaderboard.html', entries=query_db("select * from scores order by score desc"))


def random_real_tweet():
    random_year = random.randint(2009,2017)

    # open the json file from that year
    tweets_json = urllib2.urlopen("./resources/condensed_(%d).json" % random_year)
    tweets = json.loads(tweets_json)

    random_tweet_index = random.randint(0, len(tweets))

    while tweets[random_tweet_index]["is_retweet"]:
        random_tweet_index = (random_tweet_index + 1) % (len(tweets) - 1)

    return tweets[random_tweet_index]["text"]
