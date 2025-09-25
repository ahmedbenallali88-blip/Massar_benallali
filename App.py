from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, json
from config import LANGUAGES, get_translation

app = Flask(__name__)
app.secret_key = 'massar_secret'

def get_db():
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        session['user'] = user
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user: return redirect('/')
    db = get_db()
    points = db.execute('SELECT * FROM points WHERE user=?', (user,)).fetchall()
    lang = session.get('lang', 'ar')
    t = get_translation(lang)
    return render_template('dashboard.html', user=user, points=points, t=t)

@app.route('/student/<name>')
def student(name):
    db = get_db()
    points = db.execute('SELECT * FROM points WHERE user=?', (name,)).fetchall()
    lang = session.get('lang', 'ar')
    t = get_translation(lang)
    return render_template('student.html', user=name, points=points, t=t)

@app.route('/setlang/<lang>')
def setlang(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
