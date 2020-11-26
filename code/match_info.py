from tft_api import extract_match
from pprint import pprint

key = ""
file = open("C:/tft_project/data/challenger_match_list.txt", 'r')
match_id_list = []

for data in file:
    match_id_list.append(data.strip())

file.close()

match_history_list = []

count = 0
for match_id in match_id_list:
    json_file = extract_match.connect(key, match_id)
    raw_data = extract_match.extract_game_info(json_file) # 참가자 데이터 리턴
    if raw_data:
        count += 1
        pp_data = extract_match.extract_essence(raw_data)
        match_history_list.extend(pp_data)


pprint(match_history_list)
