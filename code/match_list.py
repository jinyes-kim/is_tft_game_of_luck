from tft_api import extract_match_list

key = ""

puuid_list = []
match_list = []

file = open("C:/tft_project/data/challenger_info.txt", 'r')

for data in file:
    tmp = data.split('\t')
    if tmp[0] == 'puuid':
        continue

    puuid_list.append(tmp[0])


for puuid in puuid_list:
    try:
        match_data = extract_match_list.connect(key, 3, puuid)
    except:
        continue

    match_list.extend(match_data)

match_list = list(set(match_list))
file.close()
print("Total Match length: ", len(match_list))

file = open("C:/tft_project/data/challenger_match_list.txt", 'w')

for match in match_list:
    file.write(match + '\n')

file.close()
