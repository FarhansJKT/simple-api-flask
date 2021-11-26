# FREE REST API DOCUMENTATION

How to get Json Response 
in your rest api

Python Example :
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
