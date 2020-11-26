"""
connect riot api sever and
request challenger information

"""

import requests


def connect(api_key):
    target_url = "https://kr.api.riotgames.com/tft/league/v1/challenger?api_key=" + api_key
    request = requests.get(target_url)
    print("Challenger User info Request ", request.status_code)
    return request.json()


def extract(json_file, save_name):
    user_data = json_file['entries']
    path = "C:/tft_project/data/" + save_name
    file = open(path, "w")

    for data_dict in user_data:
        file.write(data_dict['summonerId'] + '\t' +
                   data_dict['summonerName'] + '\t' +
                   str(data_dict['leaguePoints']) + '\n')

    file.close()
