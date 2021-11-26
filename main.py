from lib.dewa import cari
from lib.anime import *
from lib.brainly import *
from lib.manga import *
from lib.resize import *
from lib.search import *
from urllib.parse import *
from urllib.request import *
from textpro import tp
from flask import *
from nulis import tulis
from werkzeug.exceptions import *
#from werkzeug.utils import *
from bs4 import BeautifulSoup as bs
from requests import get, post
import random
import os, math, json, random, re, html_text, pytesseract, base64, time, smtplib, html5lib

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='farhanss', password='nisul'))

ua_ig = 'Mozilla/5.0 (Linux; Android 10; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36'

app = Flask(__name__)
apiKey = 'FhansGanss'
apiKey_ocr = 'RiriCans'
app.config['MEDIA'] = 'tts'
app.secret_key = b'BB,^z\x90\x88?\xcf\xbb'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
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

@app.route('/api/textpro/listtheme')
def listtheme():
    return '<br>'.join('%s ~> %s' % (str(n+1), i) for n, i in enumerate(tp.theme))

# islamis
@app.route('/api/islami/jadwalsholat', methods=['GET','POST'])
def jad():
	sw = request.args.get('daerah')
	ud = f"http://docs-jojo.herokuapp.com/api/jadwalshalat?daerah={sw}"
	wr = get(ud).json()
	return wr

@app.route('/api/islami/tafsir', methods=['GET','POST'])
def tfs():
	query = request.args.get('q')
	url = f"http://docs-jojo.herokuapp.com/api/tafsir?q={query}"
	res = get(url).json()
	return res

#
@app.route('/api/nulis', methods=['GET','POST'])
def nuls():
    for i in tulis(request.args.get('q'), worker=10):
        i.show()

# pro
@app.route('/api/textpro', methods=['GET','POST'])
def textpro():
    if request.args.get('theme'):
        theme = request.args.get('theme')
        if theme.lower() in tp.theme:
            if theme.lower() == 'black_pink':
                text = request.args.get('text')
                result = tp.black_pink(text)
                return result
            else:
                return {
                    'error': 'Themenya gada'
                }
        else:
            return {
                'error': 'Themenya gada'
            }
    else:
        return {
            'msg': 'Masukkan parameter theme'
        }

def convert_size(size_bytes):
	if size_bytes == 0:
		return '0B'
	size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return '%s %s' % (s, size_name[i])

@app.route('/data-tts/<path:filename>', methods=['GET','POST'])
def sendTts(filename):
	return send_from_directory(app.config['MEDIA'], filename, as_attachment=True)

@app.route('/contack/<path:cus>', methods=['GET','POST'])
def contack(cus):
	if cus == "farhanss":
		return {'status': 200,'whatsapp': '6281247374916','telp': '6281393668101'}
	elif cus == "nisa":
		return {'status': 200,'whatsapp': 'privas','telp': 'privas'}
	elif cus == "ryan":
		return {'status': 200,'whatsapp': '6285240750713','telp': 'privas'}
	elif cus == "list":
		return {
			'status': 200,
			'creator': 'Farhanss',
			'contack': ['farhanss','nisa','ryan']
		}
	else:
		return {'status': False,'msg': 'open /contack/list'}

@app.route('/config', methods=['GET','POST'])
def config():
	return {
		'status': 200,
		'creator': 'Farhanss',
		'platform': {
			'host': 'herokuapp',
			'name': 'kalong-api',
			'project': {
				'start': '22 November 2021',
				'language': 'python',
				'module': 'flask',
				'text_editor': {
					'name': 'nano',
					'license': 'GNU',
					'version': '5.8',
					'terminal': 'termux'
				},
				'github': 'null'
			},
			'buildpack': 'heroku/python'
		},
		'source_code': {
			'github': 'FarhanssAja',
			'repository': 'kalong-api',
			'url': 'https://github.com/FarhanssAja/kalong-api'
		}
	}

# Games
@app.route('/api/games/tebakgambar', methods=['GET','POST'])
def tb():
	yo = "https://farhanss-smp.herokuapp.com/api/kuis/tebakgambar?apikey=FhansGanss"
	yy = get(yo).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': {
			'soal': yy['image'],
			'jawaban': yy['jawaban']
		}
	}

@app.route('/api/games/caklontong', methods=['GET','POST'])
def cl():
	yi = "https://farhanss-smp.herokuapp.com/api/kuis/caklontong?apikey=FhansGanss"
	yq = get(yi).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': {
			'soal': yq['soal'],
			'jawaban': yq['jawaban'],
			'detail': yq['detail']
		}
	}

@app.route('/api/games/tebak-unsur-kimia', methods=['GET','POST'])
def tuk():
	qy = "http://docs-jojo.herokuapp.com/api/tebak-unsur-kimia"
	ol = get(qy).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': {
			'nama': ol['nama'],
			'lambang': ol['lambang']
		}
	}

@app.route('/api/games/tebakbendera', methods=['GET','POST'])
def tbs():
	we = "http://docs-jojo.herokuapp.com/api/tebak-bendera"
	res = get(we).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': {
			'img': res['img'],
			'emoji': res['emoji'],
			'nama': res['name']
		}
	}

#  Randm
@app.route('/api/spam/spamcall', methods=['GET','POST'])
def spamcall():
    if request.args.get('number'):
        no = request.args.get('number')
        if str(no).startswith('8'):
            hasil = ''
            kyaa = post('https://id.jagreward.com/member/verify-mobile/%s' % no).json()
            print(kyaa['message'])
            if 'Anda akan menerima' in kyaa['message']:
                hasil += 'Sukses Call number : 62%s' % no
            else:
                hasil += 'Gagal Call number : 62%s' % no
            return {
                'status': 200,
                'creator':'Farhanss',
                'logs': hasil
            }
        else:
            return {
                'status': False,
		'creator': 'Farhanss',
                'msg': 'Masukan Nomor berawalan 8'
            }
    else:
        return {
            'status': False,
            'creator': 'Farhanss',
            'msg': 'Masukan parameter number'
        }

@app.route('/api/edukasi/wiki', methods=['GET','POST'])
def wikipedia():
	if request.args.get('search'):
		try:
			kya = request.args.get('search')
			cih = f'https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={kya}'
			heuh = get(cih).json()
			heuh_ = heuh['query']['pages']
			hueh = re.findall(r'(\d+)', str(heuh_))
			result = heuh_[hueh[0]]['extract']
			return {
				'status': 200,
				'creator':'Farhanss',
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'creator': 'Farhanss',
				'msg': 'Tidak dapat menemukan kata yang anda maksud'
			}
	else:
		return {
			'status': False,
			'creator': 'Farhanss',
			'msg': 'Masukkan parameter search'
		}


@app.route('/api/edukasi/kbbi', methods=['GET','POST'])
def kbbz():
	if request.args.get('kata'):
		try:
			query = request.args.get('kata')
			url = get('https://mnazria.herokuapp.com/api/kbbi?search={}'.format(query)).json()['result']
			return {
				'status': 200,
				'creator':'Farhanss',
				'result': url
			}
		except:
			return {
				'status': False,
				'creator': 'Farhanss',
				'msg': 'Kata tidak ditemukan dalam api kbbi'
			}
	else:
		return {
			'status': False,
			'creator': 'Farhanss',
			'msg': 'Masukkan parameter kata'
		}

@app.route('/api/edukasi/translate/<path:lang>', methods=['GET','POST'])
def tr(lang):
	teks = request.args.get('teks')
	t = request.args.get('from')
	url = f"http://docs-jojo.herokuapp.com/api/translate?text={teks}&from={t}&to={lang}"
	ud = get(url).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': {
			'language': lang,
			'original_language': t,
			'hasil': ud['translated_text']
		}
	}

# download
@app.route('/api/downloader/ytsearch', methods=['GET','POST'])
def yts():
	de = request.args.get('search')
	urd = f"http://docs-jojo.herokuapp.com/api/yt-search?q={de}"
	dru = get(urd).json()
	return {
		'status': 200,
		'creator': 'Farhanss',
		'result': dru['result']['result']
	}

@app.route('/api/downloader/cocofun', methods=['GET','POST'])
def ccf():
	wm = request.args.get('wm')
	q = request.args.get('url')
	if wm == "false":
		url = f"http://docs-jojo.herokuapp.com/api/cocofun-nowm?url={q}"
		res = get(url).json()
		return {
			'status': 200,
			'creator': 'Farhanss',
			'result': {
				'id': res['id'],
				'url': res['download']
			}
		}
	elif wm == "true":
		url = f"http://docs-jojo.herokuapp.com/api/cocofun-wm?url={q}"
		res = get(url).json()
		return {
			'status': 200,
			'creator': 'Farhanss',
			'result': {
				'id': res['id'],
				'url': res['download']
			}
		}
	else:
		return {
			'status': False,
			'msg': 'wm = true / false'
		}

@app.route('/api/downloader/tiktok', methods=['GET','POST'])
def tik():
	to = request.args.get('wm')
	qw = request.args.get('url')
	if to == "false":
		uri = f"http://docs-jojo.herokuapp.com/api/tiktok_nowm?url={qw}"
		sw = get(uri).json()
		return {
			'status': 200,
			'creator': 'Farhanss',
			'result': {
				'author': sw['from'],
				'caption': sw['caption'],
				'url': sw['download']
			}
		}
	elif to == "true":
		ubi = f"http://docs-jojo.herokuapp.com/api/tiktok_wm?url={qw}"
		qwd = get(ubi).json()
		return {
			'status': 200,
			'creator': 'Farhanss',
			'result': {
				'author': qwd['from'],
				'caption': qwd['caption'],
				'url': qwd['download']
			}
		}
	else:
		usi = f"http://docs-jojo.herokuapp.com/api/tiktok_audio?url={qw}"
		ww = get(usi).json()
		return {
			'status': 200,
			'creator': 'Farhanss',
			'result': {
				'author': ww['from'],
				'caption': ww['caption'],
				'url': ww['download']
			}
		}

@app.route('/api/downloader/ytv', methods=['GET','POST'])
def ytv():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			ytv = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(ytv['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-23].text
			id = re.findall('var k__id = "(.*?)"', ytv['result'])
			thumb = bs(ytv['result'], 'html.parser').find('img')['src']
			title = bs(ytv['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp4','fquality':'360p'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'creator':'Farhanss',
				'result': {
					'title': title,
					'thumb': thumb,
					'link': dl_link,
					'resolution': '360p',
					'filesize': filesize,
					'ext': 'mp4'
				}
			}
		except Exception as e:
			print('Error : %s ' % e)
			return {
				'status': False,
				'creator': 'Farhanss',
				'msg': 'Server y2mate eror'
			}
	else:
		return {
			'status': False,
			'creator': 'Farhanss',
			'msg': 'Masukkan parameter url'
		}

@app.route('/api/downloader/yta', methods=['GET','POST'])
def yta():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			yta = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(yta['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-10].text
			id = re.findall('var k__id = "(.*?)"', yta['result'])
			thumb = bs(yta['result'], 'html.parser').find('img')['src']
			title = bs(yta['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp3','fquality':'128'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'creator':'Farhanss',
				'result': {
					'title': title,
					'thumb': thumb,
					'filesize': filesize,
					'result': dl_link,
					'ext': 'mp3'
				}
			}
		except Exception as e:
			print('Error : %s' % e)
			return {
				'status': False,
				'creator': 'Farhanss',
				'msg': 'Server y2mate eror'
			}
	else:
		return {
			'status': False,
			'creator': 'Farhanss',
			'msg': 'Masukkan parameter url'
		}



@app.route('/api/downloader/facebook', methods=['GET','POST'])
def zfb():
	if request.args.get('url'):
		try:
			query = request.args.get('url')
			link = f'https://mnazria.herokuapp.com/api/fbdownloadervideo?url={query}'
			fb = get(link).json()
			print(fb)
			return {
				'status': 200,
				'creator':'Farhanss',
				'result':{
					'kualitasHD': fb['resultHD'],
					'kualitasSD': fb['resultSD']
				}
			}
		except:
			return {
				'status': False,
				'creator': 'Farhanss',
				'msg': 'Server Nisync eror'
			}
	else:
		return {
			'status': False,
			'creator': 'Farhanss',
			'msg': 'Masukkan parameter url'
		}

# wibu
@app.route('/api/wibu/cry', methods=['GET','POST'])
def crynime():
	try:
		cryz = get('https://waifu.pics/api/sfw/cry').json()
		ncry = cryz['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': ncry
		}
	except:
		cryz = get('https://waifu.pics/api/sfw/cry').json()
		ncry = cryz['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': cryz
		}

@app.route('/api/wibu/kiss', methods=['GET','POST'])
def kissnime():
	try:
		rkiss = get('https://waifu.pics/api/sfw/kiss').json()
		nkiss = rkiss['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nkiss
		}
	except:
		rkiss = get('https://waifu.pics/api/sfw/kiss').json()
		nkiss = rkiss['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nkiss
		}

@app.route('/api/wibu/hug', methods=['GET','POST'])
def hugnime():
	try:
		hugz = get('https://waifu.pics/api/sfw/hug').json()
		nhug = hugz['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nhug
		}
	except:
		hugz = get('https://waifu.pics/api/sfw/hug').json()
		nhug = hugz['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nhug
		}

@app.route('/api/wibu/randomanime', methods=['GET','POST'])
def randomanime():
	try:
		rnime = ['waifu','neko','shinobu','megumin']
		nnimee = get('https://waifu.pics/api/sfw/%s' % random.choice(rnime)).json()
		nimee = nnimee['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nimee
		}
	except:
		rnime = ['waifu','neko','shinobu','megumin']
		nnimee = get('https://waifu.pics/api/sfw/%s' % random.choice(rnime)).json()
		nimee = nnimee['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nimee
		}

@app.route('/api/wibu/randomloli', methods=['GET','POST'])
def randomloli():
	try:
		hehe = ['kawaii','neko']
		loli = get('https://api.lolis.life/%s' % random.choice(hehe)).json()['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': loli
		}
	except:
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': loli
		}

@app.route('/api/wibu/memes', methods=['GET','POST'])
def rmemes():
	try:
		hehe = ['kawaii','neko']
		loli = get('https://api.lolis.life/%s' % random.choice(hehe)).json()['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': loli
		}
	except:
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': loli
		}

@app.route('/api/wibu/blowjob', methods=['GET','POST'])
def blowjob():
	try:
		nblow = get('https://waifu.pics/api/nsfw/blowjob').json()
		bblow = nblow['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': bblow
		}
	except:
		nblow = get('https://waifu.pics/api/nsfw/blowjob').json()
		bblow = nblow['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': bblow
		}

@app.route('/api/wibu/hentai', methods=['GET','POST'])
def hentaii():
	try:
		nblow = get('https://waifu.pics/api/nsfw/waifu').json()
		bblow = nblow['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': bblow
		}
	except:
		nblow = get('https://waifu.pics/api/nsfw/waifu').json()
		bblow = nblow['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': bblow
		}

@app.route('/api/wibu/nekos', methods=['GET','POST'])
def nsfwneko():
	try:
		nneko = get('https://waifu.pics/api/nsfw/neko').json()
		nekko = nneko['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nekko
		}
	except:
		nneko = get('https://waifu.pics/api/nsfw/neko').json()
		nekko = nneko['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': nekko
		}

@app.route('/api/wibu/trap', methods=['GET','POST'])
def trapnime():
	try:
		trap = get('https://waifu.pics/api/nsfw/trap').json()
		ntrap = trap['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': ntrap
		}
	except:
		trap = get('https://waifu.pics/api/nsfw/trap').json()
		ntrap = trap['url']
		return {
			'status': 200,
			'creator':'Farhanss',
			'result': ntrap
		}

@app.route('/docs', methods=['GET','POST'])
def api():
	return redirect('https://kalong-api.herokuapp.com/docs')

@app.route('/', methods=['GET','POST'])
def far():
	return redirect('https://kalong-api.herokuapp.com/')

@app.errorhandler(404)
def error(e):
	return render_template('eror.html'), 404
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
