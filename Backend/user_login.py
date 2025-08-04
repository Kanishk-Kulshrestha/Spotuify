from flask import Flask, redirect, request
from dotenv import load_dotenv
import os
import string
import random
import urllib
import base64
from requests import post
import json
import threading
import webbrowser
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8888/callback"


class Login:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.event = threading.Event()

    def random_str(self, length):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def setup_routes(self):

        @self.app.route("/login")
        def login():
            state = self.random_str(16)
            scope = "user-read-private user-read-email user-top-read"

            params = {
                    "response_type": "code",
                    "client_id": client_id,
                    "scope": scope,
                    "redirect_uri": redirect_uri,
                    "state": state,
                    }

            auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
            return redirect(auth_url)


        @self.app.route("/callback")
        def callback():
            code  = request.args.get("code")
            state = request.args.get("state")

            auth_string = client_id + ":" + client_secret
            auth_bytes = auth_string.encode("utf-8")
            auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

            url = "https://accounts.spotify.com/api/token"
            data = {
                    "code" : code,
                    "redirect_uri" : redirect_uri,
                    "grant_type" : "authorization_code"
                    }
            headers = {
                        "Authorization" : "Basic " + auth_base64,
                        "Content-Type" : "application/x-www-form-urlencoded"
                    }


            result = post(url, headers=headers, data=data)
            json_result = json.loads(result.content)
            self.access_token = json_result["access_token"]
            self.refresh_token = json_result["refresh_token"]
            self.event.set()
            return json_result


    def run(self):
        self.app.run(port=8888)





# if __name__ == "__main__":
#     app = Login()
#     thread = threading.Thread(target = app.run, daemon=True)
#     thread.start()

#     app.event.wait()
