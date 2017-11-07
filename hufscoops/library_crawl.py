import urllib.request
from bs4 import BeautifulSoup


def glo_library(name):

    try:
        req = urllib.request.urlopen('http://203.232.237.8/domian5/2/domian5.asp')
    except:
        return 555

    soup = BeautifulSoup(req, 'lxml', from_encoding="utf-8")

    my_titles = soup.select(
        'tr'
    )
    data = []

    for title in my_titles:
        data.append(title.text)

    # data[3]은 3층 1열람실 내용
    # [3~7]까지의 (6)
    # #return (data[num+2].split()
    if name == "도서관":
        return {'3-1': data[3].split()[6], '3-2': data[4].split()[6], '4-3A': data[5].split()[6], '4-3B': data[6].split()[6]}
    else:
        # #print(data[name+2].split())
        return {'%': data[name+2].split()[6], '이용자': data[name+2].split()[4], '남은 좌석': data[name+2].split()[5]}


def seo_library(name):

    try:
        req = urllib.request.urlopen('http://203.232.237.8/domian5/domian5.asp')
    except:
        return 555

    soup = BeautifulSoup(req, 'lxml', from_encoding="utf-8")

    my_titles = soup.select(
        'tr'
    )
    data = []

    for title in my_titles:
        data.append(title.text)

    # #return data[num+2].split()
    if name == '도서관':
        return {'4-1A': data[3].split()[6], '4-1B': data[4].split()[6], '4-2': data[5].split()[6], '5-3A': data[6].split()[6],
                '5-3B': data[7].split()[6], '5-4': data[8].split()[6]}
    else:
        # #print(data[name+2].split())
        return {'%': data[name+2].split()[6], '이용자': data[name+2].split()[4], '남은 좌석': data[name+2].split()[5]}