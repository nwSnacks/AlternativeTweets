import os
import time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, request

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'AlternativeTweetsLeaderboard.db')
    ))

@app.cli.command('init')
def init():
    init_db()
    init_tweets()
    if not hasattr(g, 'cur_id'):
        g.cur_id = 1
    print "Initialized the server"

def init_tweets():
    print "Testing init'ing tweets"

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()

#create command line command to init db
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initialized the database"

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
