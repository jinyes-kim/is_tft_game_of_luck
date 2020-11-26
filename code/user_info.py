from tft_api import extract_challenger
from tft_api import sort_leguePoints
from tft_api import extract_puuid

key = ""

# request user info
json_file = extract_challenger.connect(key)
extract_challenger.extract(json_file, "challenger_source.txt")

# preprocessing
user_list = sort_leguePoints.sort_point('challenger_source.txt')
sort_leguePoints.limit_ranking(user_list, 5, 'challenger_limited.txt')#ranking top 10


# get puuid
extract_puuid.make_table(key)


# join point table and puuid table
point_table = open("C:/tft_project/data/challenger_limited.txt", 'r')
puuid_table = open("C:/tft_project/data/challenger_puuid.txt", 'r')

point_table_list = []
puuid_table_list = []

for data in point_table:
    tmp = data.split('\t')
    if tmp[0] == 'ID':
        continue

    point_table_list.append([tmp[0], tmp[1], str(tmp[2].strip())])

for data in puuid_table:
    tmp = data.split('\t')
    if tmp[0] == 'puuid':
        continue

    puuid_table_list.append([tmp[0], tmp[1], tmp[2].strip()])

for x in puuid_table_list:
    for y in point_table_list:
        if x[1] == y[0]:
            x.append(y[2])
            continue

point_table.close()
puuid_table.close()

file = open('C:/tft_project/data/challenger_info.txt', 'w')
file.write('puuid\tID\tName\tPoint\n')

for data in puuid_table_list:
    new_data = "{}\t{}\t{}\t{}".format(data[0], data[1], data[2], str(data[3])).strip()
    file.write(new_data + '\n')

file.close()


