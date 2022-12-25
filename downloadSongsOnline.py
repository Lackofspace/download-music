import os
import sys
import requests
from bs4 import BeautifulSoup


def downloadSong(songName):
    link = 'https://ru.hitmotop.com/search?q='
    full_request = requests.get(f'{link}{songName}')
    soup = BeautifulSoup(full_request.text, 'lxml')
    songs = soup.find('ul', class_='tracks__list').find_all('div', class_='track__info-r') 

    resultList = []

    for song in songs:
        songLink = song.find('a', class_='track__download-btn').get('href')
        songRequest = requests.get(songLink)
        if songRequest.status_code == 200:
            resultList.append(songLink)
            with open(f'{songName}.mp3', 'wb') as f:
                f.write(songRequest.content)        
            break


try:
    countSongs = int(input('Сколько песен хотите скачать?\n'))
except ValueError:
    sys.exit('Ошибка ввода.\nЗавершение программы...')
print('Введите данные для нахождения песни (название, исполнитель...)')

if countSongs == 0:
    sys.exit('Выход из программы...')

for counter in range(countSongs):
    data = '+'.join(input(f'\n{counter+1} песня: ').split(' '))
    if len(data) == 0:
        continue
    
    try:
        downloadSong(data)
    except AttributeError:
        print('Песня не найдена')

print(f'\nСкачанные песни находятся в директории:\n{os.getcwd()}\n')
os.system('pause')
