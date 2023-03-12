import csv

from bs4 import BeautifulSoup
import requests
import os.path

path = 'albums.csv'
check_file = os.path.isfile(path)
HEADER = ['date', 'artist', 'album', 'link']

if not check_file:
    with open(path, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)

linkstart = 'https://metalstorm.net'
url = 'https://metalstorm.net/events/new_releases.php?upcoming=1'

response = requests.get(url=url)
main_page = response.text
soup = BeautifulSoup(main_page, 'html.parser')

p = soup.find_all(name='table', class_='table table-compact table-striped')
for month in p:
    for i in month.find_all('tr'):
        date = i.find('td', class_='dark').getText()
        date = date.replace(' ', '')
        date = date.replace('  ', '')
        name = i.find('a').getText()
        name = name.replace('​', '')
        info = name.split(' - ')
        link = i.find('a', href=True)['href']
        if len(info) > 2:
            row = [date + '.2023', info[0], info[1]+info[2], linkstart + link]
        else:
            row = [date + '.2023', info[0], info[1], linkstart + link]
        with open(path, 'a', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)