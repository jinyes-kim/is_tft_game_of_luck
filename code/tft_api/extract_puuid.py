import requests


def connect(api_key, encrypted_id):
    target_url = "https://kr.api.riotgames.com/tft/summoner/v1/summoners/" \
                 + encrypted_id + "?api_key=" + api_key
    try:
        request = requests.get(target_url)
    except:
        print("ERROR: Can't request puuid" + encrypted_id)

    data = request.json()
    return [data['puuid'], data['id'], data['name']]


def get_puuid(api_key, id_list):
    puuid_list = []

    for encrypted_id in id_list:
        tmp_data = connect(api_key, encrypted_id)
        puuid_list.append(tmp_data)

    return puuid_list


def make_table(key):
    file = open("C:/tft_project/data/challenger_limited.txt", 'r')
    limited_list = []

    for data in file:
        tmp = data.split('\t')
        limited_list.append(tmp[0])

    puuid_list = get_puuid(key, limited_list[1:])
    file.close()

    file = open("C:/tft_project/data/challenger_puuid.txt", 'w')
    file.write("puuid\tID\tName\n")

    for data in puuid_list:
        file.write(data[0] + '\t' + data[1] + '\t' + data[2] + '\n')

    file.close()
