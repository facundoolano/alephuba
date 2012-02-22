'''
Wrapper for the wupload API. Uses the requests api.
'''
import requests
import json
import StringIO


API_URL = 'http://api.wupload.com/upload?method={method}&u={email}&p={passwd}&format=json'

r = requests.get(API_URL.format(method='getUploadUrl', email=USER_EMAIL,
                                 passwd=PASSWORD))
response = json.loads(r.text)['FSApi_Upload']['getUploadUrl']['response']

filesize, url = response['max-filesize'], response['url']

sio = StringIO.StringIO(requests.get('http://apuntes.foros-fiuba.com.ar/apuntes/63/01/201-Corrosi%C3%B3n.html').content)

print json.loads(requests.post(url, files={'files' : sio}).text)