import urllib.request
from bs4 import BeautifulSoup

get_percent = lambda x : int(int(x.split()[-2])/int(x.split()[-3]) * 100)

def glo_library(name):

    try:
        req = urllib.request.urlopen('http://library.hufs.ac.kr:8091/mobile_new/lib_studyroom_state.asp')
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
        return {'3-1': get_percent(data[3]), 
        '3-2': get_percent(data[4]), '4-3A': get_percent(data[5]), '4-3B': get_percent(data[6])
        }
    else:
        name += 2
        #print(data[3].split())
        percent = get_percent(data[name])
        # #print(data[name+2].split())
        return {'%': percent, '이용자': data[name].split()[-2], '남은 좌석': data[name].split()[-1] }


def seo_library(name):

    try:
        req = urllib.request.urlopen('http://library.hufs.ac.kr:8091/mobile_new/lib_studyroom_state.asp')
    except:
        return 555

    soup = BeautifulSoup(req, 'lxml', from_encoding="utf-8")

    my_titles = soup.select(
        'tr'
    )
    data = []

    for title in my_titles:
        data.append(title.text)
    #print(data)
    # #return data[num+2].split()

    # 서울캠 도서관 임시도서관 열람실

    #print(data[1].split())
    if name == "도서관":
        return {'room-A' : get_percent(data[1]),
                'room-B' : get_percent(data[2]),
                }
    else:
        percent = get_percent(data[name])
        return {'%': percent, '이용자': data[name].split()[-2], '남은 좌석': data[name].split()[-1] }
        # print(data[name+2].split())


    """
    # 서울캠퍼스 도서관 공사 중
    
    if name == '도서관':
        return {'4-1A': data[3].split()[6], '4-1B': data[4].split()[6], '4-2': data[5].split()[6], '5-3A': data[6].split()[6],
                '5-3B': data[7].split()[6], '5-4': data[8].split()[6]}
    else:
        # #print(data[name+2].split())
        return {'%': data[name+2].split()[6], '이용자': data[name+2].split()[4], '남은 좌석': data[name+2].split()[5]}
    """


if __name__ == "__main__":
    print(seo_library(2))
    print(glo_library(1))
    print(glo_library(2))