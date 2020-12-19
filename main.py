from tft_api.Challenger import Challenger
import requests
import json
from pprint import pprint

lambda_api_url = ""
api_key = ""

challenger = Challenger(key=api_key, rank=5, game_version='10.25')
check = challenger.connect_encrypted_id()

if check:
    challenger.preprocess_encrypted_id()
    challenger.connect_puuid()
    challenger.connect_match_id(1)
    challenger.connect_match_history()
    challenger.extract_match_info()
    data = challenger.match_information
else:
    print("Error - Request Fail")

request = requests.post(lambda_api_url, data=json.dumps(data, indent=4))
print(request.json())



