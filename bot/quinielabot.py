# $ pip install pyopenssl ndg-httpsclient pyasn1
import json
import requests
import time
from quinielapremios import Quiniela

TOKEN = "544037925:AAH_ff6VSjLTPToOCxX9Q0jWw5gTkWnkjNQ"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
ABOUT = "ABOUT"

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def about():
    return json.dumps({"Name": "QuinielaBot", "Author": "Maximiliano Bordon", "version": "1.0"})


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def convey_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if cmp(text.upper(), ABOUT) == 0:
                response = about()
            else:
                response = Quiniela.getpremios('', text)
            send_message(response, chat)
        except Exception as e:
            print(e)

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            convey_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
