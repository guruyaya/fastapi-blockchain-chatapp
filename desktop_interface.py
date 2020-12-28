from multiprocessing import Process
from main_fast import app
import argparse
import uvicorn
import time
import threading
import json
import requests
import itertools
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class BCStart(Screen):
    def on_enter(self, *args):
        if self.manager.proc != None:
            self.manager.proc.kill()

        if self.manager.task != None:
            Clock.unschedule(self.manager.task)

class ChatControl(Screen):
    def on_enter(self, *args):
        parser = argparse.ArgumentParser()

        parser.add_argument("-p", "--port", help="Set the port to run blockchain", default=8000, type=int)
        parser.add_argument("--host", help="Set the host to run blockchain", default="127.0.0.1")

        args = parser.parse_args()
        bc_server = BCServer(args)
        self.manager.proc = Process(target=bc_server.start, args=(), daemon=True)
        self.manager.proc.start()

        self.manager.task = Clock.schedule_interval(self.update_chat, 1)

    def update_chat(self, dt):
        r = requests.get('http://127.0.0.1:8000/chain')
        chain = json.loads(r.text)['chain']
        chats = [ (outer['timestamp'], inner) 
                    for outer in chain 
                        for inner in outer['transactions'] ]
        fill_text = ''
        for ts, chatline in chats[-1::-1]:
            fill_text += datetime.fromtimestamp(ts).strftime("%m/%d/%Y, %H:%M:%S - ")
            fill_text += '{: <16}: {}\n'.format(chatline['author'], chatline['content'])
        
        self.chat.text = fill_text

class Manager(ScreenManager):
    proc = None
    task = None

    bc_start = ObjectProperty(None)
    chat_control = ObjectProperty(None)

class ScreensApp(App):
    m = None

    def build(self):
        self.m = Manager(transition=NoTransition())
        return self.m
    
    def send_your_message_to_blockchain(self):
        chat_control = self.m.chat_control
        send_chat = chat_control.send_chat
        send_chat.text = "Sending..."
        send_chat.disabled = True

        data = {'author': chat_control.your_name.text,
            'content':  chat_control.your_text.text}
        r = requests.post("http://localhost:8000/new_transaction", json=data, headers={'Content-type':'application/json'})
        if (r.status_code == 200):
            send_chat.text = "Processing..."
            r = requests.get("http://localhost:8000/mine")
        send_chat.text = "Send"
        send_chat.disabled = False

    def update_chat(self):
        r = requests.get("http://localhost:8000/chain")
        print (r)

class BCServer:
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
    
    def start(self):
        uvicorn.run(app, host=self.host, port=self.port)

if __name__ == '__main__':
    if __name__ == '__main__':
        ScreensApp().run()

