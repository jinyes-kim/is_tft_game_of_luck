"""
인풋 데이터 포맷 수정 -> 어떻게 데이터를 적재할 것인가?

"""

import requests
from pprint import pprint


class Challenger:
    def __init__(self, key, rank, game_version):
        self.api_key = key
        self.rank = rank
        self.game_version = game_version
        self.all_user_json = None
        self.preprocessed_user_list = []
        self.puuid_list = []
        self.match_set = set()
        self.match_history_list = []
        self.match_information = []

    def connect_encrypted_id(self):
        target_url = "https://kr.api.riotgames.com/tft/league/v1/challenger?api_key=" + self.api_key
        try:
            request = requests.get(target_url)
            print("\n<Extract Report - encrypted ID>\n - status {}\n\n".format(request.status_code))
            self.all_user_json = request.json()
            return True
        except Exception as error:
            print("ERROR - Can't request encrypted_id {}".format(error))

        return False

    def preprocess_encrypted_id(self):
        user_data = self.all_user_json['entries']

        for data_dict in user_data:
            self.preprocessed_user_list.append(
                [data_dict['summonerId'],
                 data_dict['summonerName'],
                 data_dict['leaguePoints']]
            )

        # sort by Rank points
        self.preprocessed_user_list.sort(key=lambda x: x[2], reverse=True)
        self.preprocessed_user_list = self.preprocessed_user_list[:self.rank]

    def connect_puuid(self):
        success_count = 0
        fail_count = 0

        for encrypted_id in self.preprocessed_user_list:
            api_url = "https://kr.api.riotgames.com/tft/summoner/v1/summoners/" \
                         + encrypted_id[0] + "?api_key=" + self.api_key
            try:
                request = requests.get(api_url)
                self.puuid_list.append(request.json()['puuid'])
                success_count += 1
            except Exception as error:
                print("<Error - Can't request {}'s puuid {}".format(encrypted_id[1], error))
                fail_count += 1

        print("\n\n<Extract Report - puuid>\n - Complete {}\n - Fail {}\n\n".format(success_count, fail_count))

    def connect_match_id(self, count):
        self.match_set = set()
        path = "C:/tft_project/data/match_history.txt"

        try:
            history_file = open(path, 'r')
            history_list = [history[:-1] for history in history_file]
        except Exception as error:
            print("! Initialize Match history {}".format(error))
            history_file = open(path, 'w')
            history_list = []

        history_file.close()
        duplication = 0

        for puuid in self.puuid_list:
            target_url = "https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/"\
                         + puuid + "/ids?count=" + str(count) + "&api_key=" + self.api_key
            try:
                request = requests.get(target_url)
            except Exception as error:
                print("<Error - Can't request match ID {}".format(error))
                continue

            for match in request.json():
                if match not in history_list:
                    self.match_set.add(match)
                else:
                    duplication += 1

        history_file = open(path, 'a')
        for match in list(self.match_set):
            history_file.write(match + '\n')

        history_file.close()

        print("\n\n<Extract Report - Match ID list>\n - Add {}\n - Duplication {}\n\n".format(
            len(self.match_set), duplication))

    def connect_match_history(self):
        for match_id in self.match_set:
            api_url = "https://asia.api.riotgames.com/tft/match/v1/matches/" + match_id + "?api_key=" + self.api_key
            try:
                request = requests.get(api_url)
            except Exception as error:
                print("<Error - Can't request match history {}".format(error))
                continue

            self.match_history_list.append(request.json())

    # this function for per element
    def extract_match_info(self):
        result_list = []
        for match_info in self.match_history_list:
            version = match_info['info']['game_version'][8:13]
            if version != self.game_version:
                continue

            for participant in match_info['info']['participants']:
                json_dict = {}
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

                json_dict['placement'] = placement
                json_dict['chosen'] = chosen
                json_dict['units'] = units_list
                json_dict['items'] = items_list
                result_list.append(json_dict)

        self.match_information = result_list


def is_chosen(units_info_json):
    try:
        if units_info_json['chosen']:
            return True
    except:
        return False
