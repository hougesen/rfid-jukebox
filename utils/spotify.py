import requests


def switch_playback(access_token: str) -> bool:
    print("/switch-playback")

    current_state = requests.get("https://api.spotify.com/v1/me/player", headers={
        "Authorization": f"Bearer {access_token}"
    })

    if current_state.status_code == 200 and current_state.json()["is_playing"] == True:
        print("if music is playing")
        return pause_music(access_token)
    else:
        print("else music is not playing")

        return start_music(access_token)


def start_music(access_token: str) -> bool:
    print("start_music")
    url = "https://api.spotify.com/v1/me/player/play"
    r = requests.put(url, headers={
        "Authorization": f"Bearer {access_token}"
    })
    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False


def pause_music(access_token: str) -> bool:
    print("pause_music")

    url = "https://api.spotify.com/v1/me/player/pause"
    r = requests.put(url, headers={
        "Authorization": f"Bearer {access_token}"
    })
    print("r", r)
    if r.status_code == 204:
        return True
    else:
        return False


def change_volume(access_token: str, volume_percentage: int) -> bool:
    print("change_volume", volume_percentage)
    url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percentage}"
    r = requests.put(url, headers={
        "Authorization": f"Bearer {access_token}"
    })

    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False


def next_song(access_token: str) -> bool:
    print("next_song")
    url = "https://api.spotify.com/v1/me/player/next"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {access_token}"
    })

    if r.status_code == 204:
        return True
    else:
        return False


def previous_song(access_token: str) -> bool:
    print("next_song")
    url = "https://api.spotify.com/v1/me/player/previous"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {access_token}"
    })

    if r.status_code == 204:
        return True
    else:
        return False


def change_playlist(access_token: str) -> bool:
    print("change_playlist")
    url = "https://api.spotify.com/v1/me/player/play"

    # Currently hardcoded as top 50 denmark
    data = {"context_uri": "spotify:playlist:37i9dQZEVXbL3J0k32lWnN"}

    r = requests.put(url, json=data, headers={
        "Authorization": f"Bearer {access_token}"
    })

    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False
