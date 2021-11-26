# FREE REST API DOCUMENTATION

Welcome to my Rest api 🔥
kami menyediakan berbagai macam api json
yang slalu update menjadi yang terbaik
```bash
> Author   : Farhanss SmPD.ID
> Template : Farhan & web
> App      : Python Flask
> Build    : -
```

You don't have apikey? My api no use apikey
free rest api for you

How to get Json Response 
in your api
```
$ Python Flask Example :
```
```python
from falsk import *
import json
app = Falsk(__name__)

@app.route('/api/tebakgambar', methods=['GET','POST'])
def tebakgambar():
    url = get('https://docs-klapi.herokuapp.com/api/games/tebakgambar').Json()
    res_image = url['result']['soal']
    res_answer = url['result']['jawaban']
    return {
       'status': True,
       'creator': 'yourname',
       'result': {
            'image': res_image,
            'answer': res_answer
       }
    }
```
```
$ Nodejs Expressjs Example:
```
```javascript
const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');

router.get('/api/tebakgambar', (req, res) => {
   fetch('https://docs-klapi.herokuapp.com/api/games/tebakgambar')
   .then(response => response.json())
   .then(data => {
       res.json({
             status: 200,
             creator: 'yourname',
             api: 'kalong-api',
             result: {
                  image: data.result.soal,
                  answer: data.result.jawaban
             }
       })
    })
})
```
