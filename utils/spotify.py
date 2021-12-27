import requests


def switch_playback(access_token: str) -> bool:
    print("/switch-playback")

    current_state = requests.get(
        "https://api.spotify.com/v1/me/player",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if current_state.status_code == 200 and current_state.json()["is_playing"] == True:
        print("if music is playing")
        return pause_music(access_token)
    else:
        print("else music is not playing")

        return start_music(access_token)


def start_music(access_token: str) -> bool:
    print("start_music")

    r = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False


def pause_music(access_token: str) -> bool:
    print("pause_music")

    r = requests.put(
        "https://api.spotify.com/v1/me/player/pause",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print("r", r)
    if r.status_code == 204:
        return True
    else:
        return False


def change_volume(access_token: str, volume_percentage: int) -> bool:
    print("change_volume", volume_percentage)

    r = requests.put(
        f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percentage}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False


def next_song(access_token: str) -> bool:
    print("next_song")

    r = requests.post(
        "https://api.spotify.com/v1/me/player/next",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if r.status_code == 204:
        return True
    else:
        return False


def previous_song(access_token: str) -> bool:
    print("next_song")

    r = requests.post(
        "https://api.spotify.com/v1/me/player/previous",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if r.status_code == 204:
        return True
    else:
        return False


def change_playlist(access_token: str) -> bool:
    print("change_playlist")

    # Currently hardcoded as top 50 denmark
    r = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        json={"context_uri": "spotify:playlist:37i9dQZEVXbL3J0k32lWnN"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    print("r", r)

    if r.status_code == 204:
        return True
    else:
        return False
