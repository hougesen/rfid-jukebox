import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import Optional
from dotenv import dotenv_values
import utils.spotify
from utils.generateRandomString import generateRandomString

config = dotenv_values(".env")

app = FastAPI()

redirect_uri: str = "http://localhost:8000/spotify/callback"
client_id: Optional[str] = config["SPOTIFY_CLIENT_ID"]
client_secret: Optional[str] = config["SPOTIFY_CLIENT_ID"]
state: str = generateRandomString(20)

# TODO: store data in sqlite
access_token: str = config["SPOTIFY_ACCESS_TOKEN"] or ""
current_volume: Optional[int] = None

if client_id is None:
    print("Missing Spotify client id")

if client_secret is None:
    print("Missing Spotify client secret")


@app.get("/")
def index():
    return {"Hello fam"}


@app.get("/login")
def login():
    scope: str = "%20".join([
        "user-read-private",
        "user-read-email",
        "user-read-playback-state",
        "user-modify-playback-state",
        "streaming",
        "user-read-currently-playing"
    ])

    return RedirectResponse(f"https://accounts.spotify.com/authorize?response_type=token&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state}")


# TODO: refresh token automatically
@app.get("/spotify/callback")
def spotify_callback(access_token: Optional[str] = None, token_type: Optional[str] = None, expires_in: Optional[int] = None, state: Optional[str] = None, error: Optional[str] = None):
    print("spotify_callback")
    print("access_token", access_token)
    print("token_type", token_type)
    print("expires_in", expires_in)
    print("state", state)
    print("error", error)


@app.put("/switch-playback")
def switch_playback():
    print("/switch-playback")

    current_state = requests.get("https://api.spotify.com/v1/me/player", headers={
        "Authorization": f"Bearer {access_token}"
    })

    if current_state.status_code == 200 and current_state.json()["is_playing"] == True:
        print("if music is playing")
        utils.spotify.pause_music(access_token)
        return {"msg": "music is playing"}
    else:
        print("else music is not playing")

        utils.spotify.start_music(access_token)
        return {"msg": "music is not playing"}

    # return {current_state: current_state}


@app.put("/change-volume/{volume_percentage}")
def change_volume(volume_percentage: int):
    result = utils.spotify.change_volume(access_token, volume_percentage)
    if result:
        return {"msg": "volume changed successfully"}
    else:
        return {"msg": "something went wrong"}


@app.put("/skip")
def next_song():
    print("next_song")
    utils.spotify.next_song(access_token)


@app.put("/previous")
def previous_song():
    print("next_song")
    utils.spotify.previous_song(access_token)
