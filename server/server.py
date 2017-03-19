import os
import time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, request
import random
import json
from HTMLParser import HTMLParser

app = Flask(__name__)

filtered_tweets = []
html_parser = HTMLParser()

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
    print "Initializing tweets"
    raw_tweets_text = open("raw_tweets_text.txt", "w")
    for i in range(2011, 2018):
        with open("resources/condensed_%d.json" % i) as raw_tweets_json:
            raw_tweets = json.load(raw_tweets_json)
            for tweet in raw_tweets:
                if not (tweet["is_retweet"] or tweet["text"][0] == "@"):
                    raw_tweets_text.write(
                        html_parser.unescape(tweet["text"].encode("ascii", "ignore")).replace(".@", " @") + " ")
                    filtered_tweets.append(tweet)
    raw_tweets_text.close()
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

'''
The returned tweet will be a JSON object in this format format
{
    "tweet":"some tweet text"
    "true_or_false":"true"
}
'''
@app.route('/question', methods=['GET'])
def get_tweet():
    if random.randint(0, 1) == 1:
        return random_real_tweet()
    else:
        return #TODO: return a fake tweet

def random_real_tweet():
    random_tweet_index = random.randint(0, len(filtered_tweets) - 1)
    data = {}
    data["tweet"] = html_parser.unescape(
        filtered_tweets[random_tweet_index]["text"].encode("ascii", "ignore")).replace('\"', "")
    data["true_or_false"] = "true"
    json_data = json.dumps(data)
    return json_data
