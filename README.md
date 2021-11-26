# FREE REST API DOCUMENTATION

How to get Json Response 
in your api

Python Flask Example :
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

Nodejs Expressjs Example:
```javascript
const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');

router.get('/api/tebakgambar', (req, res) => {
   fetch('https://docs-klapi.herokuapp.com/api/games/tebakgambar')
   .then(res =>
}
```
