from user_login import Login
import web_api
import token_handler as th
import time
import threading
import os
from dotenv import load_dotenv
import json
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def Oauth():
    app = Login()
    server_thread = threading.Thread(target = app.run, daemon=True)
    server_thread.start()
    app.event.wait()
    access_token = app.access_token
    refresh_token =  app.refresh_token
    
    th.set_tokens(access_token, str(time.time()+3500), refresh_token)    
    return access_token

if __name__ == "__main__":
    access_token, expiry = th.get_access_token()
    if expiry == None:
        expiry = 0
    expiry = float(expiry)

    print(access_token)
    print("\n", expiry)
    if access_token == None:
        access_token = Oauth()
        
    elif expiry < time.time():
        refresh_token = th.get_refresh_token()
        access_token = web_api.refresh_token_call(refresh_token)
        th.set_tokens(access_token, str(time.time() + 3600), refresh_token)

    
    data = web_api.get_user_info(access_token)
    pretty = json.dumps(data, indent=4)
    #print(pretty)
        
    data = web_api.get_top_tracks(access_token, "short_term", 1, 0)
    pretty = json.dumps(data, indent=4)
    print(pretty)
        
