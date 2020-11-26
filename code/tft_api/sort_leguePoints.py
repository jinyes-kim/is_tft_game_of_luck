"""
open user data file and
sorting data by league point

"""


def sort_point(file_name):
    path = "C:/tft_project/data/" + file_name
    file = open(path, 'r')
    user_list = []

    for data in file:
        tmp = data.split('\t')
        user_list.append([tmp[0], tmp[1], int(tmp[2].strip())])

    user_list.sort(key=lambda x: x[2], reverse=True)
    file.close()
    return user_list


def limit_ranking(user_list, limit, save_name):
    path = "C:/tft_project/data/" + save_name
    file = open(path, 'w')

    file.write('ID\tName\tScore\n')
    for data in user_list[:limit]:
        file.write(data[0] + '\t' + data[1] + '\t' + str(data[2]) + '\n')

    file.close()

