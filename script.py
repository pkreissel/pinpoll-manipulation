import requests
import json
import hashlib as hs
import time as t
from tqdm import tqdm
import random
import math
#If you want rotate TOR-adresses:
#from stem.control import Controller
#from stem import Signal


for i in tqdm(range(1,1000)):

    #Optional- Get new TOR Connection for each request - but then you should increase the delay at the end to reduce load on the TOR network
    # with Controller.from_port(port = 9051) as controller:
    #     controller.authenticate() #You should set a password and enter it here
    #     controller.signal(Signal.NEWNYM)

    session = requests.session()
    #For TOR-Connection
    #session.proxies['https'] = 'socks5h://localhost:9050'

    #Simulate new User and get cookies
    try:
        result = session.post("https://api.tools.pinpoll.com/v2/pollview", json = {"poll_id":90574,"referrer":"https://tools.pinpoll.com/embed/90574","previewMode":False})
    except:
        continue

    #Set Cookies and Headers - I was too lazy to check which of them are necessary.
    headers = {
        'authority': 'direct.pinpoll.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://tools.pinpoll.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://tools.pinpoll.com/embed/90574',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'visitor=' + result.cookies.values()[0],
    }

    #Vote with random fingerprint - probably the code here is more complicated than necessary
    rand = math.floor(random.random()*2**128)
    data = '{"poll_id":90574,"answer_id":365870,"fingerprint":"' + hs.md5(str(rand).encode('utf-8')).hexdigest() + '","require_user_opt_in":false}'
    response = session.post('https://direct.pinpoll.com/v2/vote', headers=headers, data=data)
    try:
        print(json.loads(response.text)["result"][0]["votes"])
    except Exception as e:
        print(response.text)
    t.sleep(3) #Don't set this to zero, we dont want to DDOS the server.
