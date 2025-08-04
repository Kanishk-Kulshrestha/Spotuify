import keyring

def set_tokens(access_token, time, refresh_token):
    keyring.set_password("spotify_app", "access_token", access_token)
    keyring.set_password("spotify_app", "expiry", time)
    keyring.set_password("spotify_app", "refresh_token", refresh_token)
    

def get_access_token():
    access_token = keyring.get_password("spotify_app", "access_token")
    expiry       = keyring.get_password("spotify_app", "expiry")
    return access_token, expiry

def get_refresh_token():
    return keyring.get_password("spotify_app", "refresh_token")


def reset():
    keyring.delete_password("spotify_app", "access_token")
    keyring.delete_password("spotify_app", "expiry")
    keyring.delete_password("spotify_app", "refresh_token")

if __name__ == "__main__":
    reset()
