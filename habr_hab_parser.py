# Script Name	: habr_hab_parser.py
# Author		: Dmitry Vertiev
# Created		: 2017
# Last Modified	: 2017
# Version		: 0.1
#
# Description	: Simple script to grab posts list from habrhabr habs.

import urllib.request
from bs4 import BeautifulSoup
import re
import json
import datetime as dt

HABR = 'https://habrahabr.ru/hub/'
HAB_NAME = 'python'
date = str(dt.datetime.now().strftime("%Y-%m-%d_%H_%M"))
print(date)
FILE = 'habr_' + HAB_NAME + '_' + date + '_dump.json'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

posts = []
def parse(html):

    tables = soup.find_all('div', class_='post post_teaser shortcuts_item')
    with open(FILE, 'a+', encoding='utf-8') as outfile:
        for row in tables:
            
            json.dump({
            'id': row.get('id'),
            'date': row.span.text.strip(),
            'title': row.a.text,
            'link': row.a.get('href').strip(),
            'author': row.find_all('a')[-2].text.strip()
        }, outfile, indent=4, ensure_ascii=False)

def get_count(html):
    linklist = []
    soup = BeautifulSoup(html, "html.parser")
    pag = soup.find_all('a', class_='toggle-menu__item-link toggle-menu__item-link_pagination toggle-menu__item-link_bordered')
    ll = pag[0].get('href').split('/')
    for i in range(1,int(re.findall(r'[\d+]+', ll[-2])[0])+1):
        link = 'https://habrahabr.ru/' + str(ll[1]) + '/' + str(ll[2]) + '/' + str(re.findall(r'\D+', ll[-2])[0]) + str(i)
        linklist.append(link)
    return linklist

def main():
    pages_list =  get_count(get_html(HABR + HAB_NAME))
    print(pages_list)
    for page in pages_list:
        print('Parsing {:03.2f} %'.format( int(re.findall(r'\d+',page)[0]) / int(len(pages_list)) * 100))
        parse(get_html(page))

if __name__ == '__main__':
    main()


