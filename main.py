from lib.dewa import cari
from lib.anime import *
from lib.brainly import *
from lib.manga import *
from lib.resize import *
from lib.search import *
from lib.nulis import *
from urllib.parse import *
from urllib.request import *
from textpro import tp
from flask import *
from werkzeug.exceptions import *
#from werkzeug.utils import *
from bs4 import BeautifulSoup as bs
from requests import get, post
import random
import os, math, json, random, re, html_text, pytesseract, base64, time, smtplib, html5lib

class User:
    def __init__(self, email, username, password, info):
        self.email = email
        self.username = username
        self.password = password
        self.info = info

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(email="hanscker3@gmail.com", username='farhanss', password='nisul', info='AUTHOR KLAPI'))


ua_ig = 'Mozilla/5.0 (Linux; Android 10; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36'

app = Flask(__name__)
apiKey = 'FhansGanss'
apiKey_ocr = 'RiriCans'
app.config['MEDIA'] = 'tts'
app.secret_key = b'BB,^z\x90\x88?\xcf\xbb'

def validate(name):
	try:
		dat = [u for u in users if u.email == name][0]
		return True
	except IndexEror:
		return False

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.email == session['user_id']][0]
        g.user = user

@app.errorhandler(RequestURITooLarge)
def TobzZ(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

def tp(text):
    return text.rstrip('\n').lstrip('\n')

@app.route('/docs', methods=['GET','POST'])
def api():
	if not g.user:
		return redirect('/login')
	else:return render_template('index.html')

@app.route('/nulis', methods=['GET'])
def nulis():
        if not g.user:
                return redirect('/login')
        else:
                g.images = "https://docs-klapi.herokuapp.com/api/nulis?q=NoText"
                return render_template('nulis2.html')

@app.route('/nulis', methods=['POST'])
def write():
        ff = request.form['query']
        if request.form['query'] == "":
             g.images = "https://docs-klapi.herokuapp.com/api/nulis?q=Text Kosong"
        else:
             g.images = f"https://docs-klapi.herokuapp.com/api/nulis?q={ff}"

@app.route('/login', methods=['GET'])
def loging():
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginp():
	session.pop('user_id', None)

	email = request.form['email']
	password = request.form['password']

	try:
		dat = [x for x in users if x.email == email][0]
		if dat and dat.password == password:
			session['user_id'] = dat.email
			return redirect('/docs')

	except IndexError:
		return redirect('/register')

@app.route('/register', methods=['GET'])
def registerg():
	return render_template('register.html')

@app.route('/register', methods=['POST'])
def registerp():
	email = request.form['email']
	password = request.form['password']
	cpassword = request.form['repassword']
	username = request.form['username']
	info = request.form['info']
	we = f"{email}"
	tw = f"{password}"
	oy = f"{info}"
	pq = f"{username}"
	try:
		dat = [u for u in users if u.email == email][0]
		if dat:
			return redirect('/login?log=Email-Sudah-Terdaftar')
	except IndexError:
		if password == cpassword:
			users.append(User(email=we, username=pq, password=tw, info=oy))
			return redirect('/login')
		else:
			return redirect('/register?log=Password-valid')

@app.route('/', methods=['GET','POST'])
def far():
	return render_template('dasboard.html')

@app.errorhandler(404)
def error(e):
	return render_template('eror.html'), 404
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
