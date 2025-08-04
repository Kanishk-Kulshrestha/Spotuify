from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
from user_login import Login
import time
import threading


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
TOKEN = None

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded"
            }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def refresh_token_call(refresh_token):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
            "Authorization": "Basic " + auth_base64,
            "content-type" : "application/x-www-form-urlencoded"
            }

    data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
            }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    print(json_result)
    access_token  = json_result["access_token"]
    # refresh_token = json_result["refresh_token"]

    return access_token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)
    print(json_result)


def get_top_tracks(token, time_range="medium_term", limit="3", offset="0"):
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}&offset={offset}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_user_info(token):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


if __name__ == "__main__":
    app = Login()
    server_thread = threading.Thread(target = app.run, daemon=True)
    server_thread.start()
    app.event.wait()
    token = app.token
    print("TOKEN:", token)

    search_for_artist(token, "Ariana Grande")
    print("\n\n\n")

    get_user_info(token)