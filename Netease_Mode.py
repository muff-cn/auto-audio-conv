import requests


def info_get(music_id):
    resp = requests.get(
        f'https://music.163.com/api/song/detail/?id={music_id}&ids=%5B{music_id}%5D'
    )
    info_dict = resp.json()
    # print(info_dict)
    name = info_dict['songs'][0]['name']
    artists = info_dict['songs'][0]['artists'][0]['name']
    # result = f'{artists} - {name}'
    # print(res)
    return artists, name


# id: 1901371647  陈奕迅 - 孤勇者
if __name__ == '__main__':
    example = '1901371647'
    print(' - '.join(info_get(example)))
