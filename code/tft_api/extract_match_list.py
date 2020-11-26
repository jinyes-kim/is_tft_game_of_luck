import requests


def connect(api_key, count, puuid):
    target_url = "https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/"\
                 + puuid + "/ids?count=" + str(count) + "&api_key=" + api_key
    request = requests.get(target_url)
    print("Match ID Request: ", request.status_code)
    return request.json()

