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

class Dbehs:
    def __init__(self, id, url, email):
        self.id = id
        self.url = url
        self.email = email

    def __repr__(self):
        return f'<Data: {self.id}>'

users = []
users.append(User(email="hanscker3@gmail.com", username='farhanss', password='nisul', info='AUTHOR KLAPI'))
dbeh = []
dbeh.append(Dbehs(id="Tes", url="https://kalong-api.herokuapp.com/", email="@bot"))

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

def generateId(count):
    result_str = ''.join((random.choice('abcdefghijklmnopqrstuvwqyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(count)))
    return result_str

def createNew(emaild, urls):
    smd = generateId(5)
    try:
         om = [u for u in dbeh if u.id == smd][0]
         if om:
             tod = smd + generateId(3)
             dbeh.append(Dbehs(id=tod, url=urls, email=emaild))
             return f'https://kalong-api.herokuapp.com/p/{tod}'
    except IndexError:
         dbeh.append(Dbehs(id=smd, url=urls, email=emaild))
         return f'https://kalong-api.herokuapp.com/p/{smd}'

@app.before_request
def before_request():
    g.user = None
    g.dat = None

    if 'cayang' in session:
        td = [i for i in dbeh if i.id == session['cayang']][0]
        g.dat = td

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

@app.route('/p/<path: ts>', methods=['GET'])
def pget(ts):
        try:
              woe = [x for x in dbeh if x.id == ts][0]
              if woe:
                 session['cayang'] = woe.id
                 return redirect('/getlink')
        except IndexError:
                 return redirect('/new')

@app.route('/getlink', methods=['GET', 'POST'])
def getlinks():
        if not g.dat:
                return redirect('/new')
        else:return render_template('getlink.html')

@app.route('/docs', methods=['GET','POST'])
def api():
	if not g.user:
		return redirect('/login')
	else:return render_template('index.html')

@app.route('/nulis', methods=['GET'])
def nulis():
        g.images = "https://docs-klapi.herokuapp.com/api/nulis?q=NoText"
        return render_template('nulis2.html')

@app.route('/nulis', methods=['POST'])
def write():
        ff = request.form['query']
        if request.form['query'] == "":
             g.images = "https://docs-klapi.herokuapp.com/api/nulis?q=Text Kosong"
             return render_template('nulis2.html')
        else:
             g.images = f"https://docs-klapi.herokuapp.com/api/nulis?q={ff}"
             return render_template('nulis2.html')

@app.route('/new', methods=['GET'])
def aw_g():
        return render_template('create.html')

@app.route('/new', methods=['POST'])
def aw_p():
        session.pop('cayang', None)

        email = request.form['email']
        url = request.form['url']

        return redirect(createNew(email, url))

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
