import requests


def connect(api_key, match_id):
    target_url = "https://asia.api.riotgames.com/tft/match/v1/matches/" + match_id + "?api_key=" + api_key
    request = requests.get(target_url)

    data = request.json()
    return data


def version_check(version):
    if version == '10.24':
        return True
    return False


def extract_game_info(json_file):
    participants = json_file['info']['participants']
    version = json_file['info']['game_version'][8:13]

    if version_check(version):
        return participants
    return None


def is_chosen(units_json):
    try:
        if units_json['chosen']:
            return True
    except:
        return False


def extract_essence(json_file):
    result_list = []
    for participant in json_file:
        placement = participant['placement']
        units_list = []
        items_list = []
        chosen = None
        for unit in participant['units']:
            if is_chosen(unit):
                chosen = unit['character_id'][5:]
                units_list.append(chosen)
            else:
                units_list.append(unit['character_id'][5:])

            items_list.extend(unit['items'])

        result_list.append([placement, chosen, units_list, items_list])

    return result_list
