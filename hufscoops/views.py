from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bs4 import BeautifulSoup
import json, datetime, requests, time
import urllib.request
import sqlite3, os

def keyboard(request):

    return JsonResponse({
        'type': 'buttons',
        'buttons': ['학식', '도서관', '캠퍼스 변경']
    })


@csrf_exempt
def message(request):
    button_info = ['학식', '도서관', '캠퍼스 변경']
    user_type = 'NO'
    start_time = time.time()
    today = datetime.date.today()
    today_date = today.strftime('%m월 %d일')
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    content_name = received_json_data['content']
    # content 의 내용
    user_name = received_json_data['user_key']
    # user_key 의 내용
    print(user_name + '님이 ' + content_name + '을 눌렀습니다')

    con = sqlite3.connect("./DB/userdata.db")
    cur = con.cursor()

    # #cur.execute("CREATE TABLE user_data(Name TEXT, Campus TEXT);")
    if "캠퍼스 변경" in content_name:
        return JsonResponse({
            'message': {
                'text': '캠퍼스를 선택하세요'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['서울', '글로벌']
            }
        })

    elif content_name in ("서울", "글로벌"):
        print("작업중 1234")
        cur.execute("DELETE FROM user_data WHERE Name = (:name)", {"name": user_name})
        cur.execute("INSERT into user_data(Name, Campus) VALUES (?,?)", (user_name, content_name))
        con.commit()
        con.close()
        return JsonResponse({
            'message': {
                'text': content_name+'캠퍼스를 선택하였습니다'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_info
            }
        })

    cur.execute("SELECT Campus from user_data WHERE Name = (:name)", {"name": user_name})
    confirm = cur.fetchall()

    if len(confirm) == 0:
        return JsonResponse({
            'message': {
                'text': '캠퍼스를 선택하세요'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['서울', '글로벌']
            }
        })

    cur.execute("SELECT Campus from user_data WHERE Name = (:name)", {"name": user_name})
    data = cur.fetchone()

    if "글로벌" in data:
        user_type = 'global'
        print("\n\n글로벌 유저\n")
    elif "서울" in data:
        user_type = 'seoul'
        print("\n\n서울 유저\n")
        #else:

    #elif "캠퍼스 변경" in content_name:
    con.commit()
    con.close()

    if "NO" in user_type:
        return JsonResponse({
            'message': {
                'text': '최초 캠퍼스 설정 값이 없습니다\n캠퍼스를 골라주세요'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['서울', '글로벌']
            }
        })


    if content_name == '학식':
        if user_type == 'global':
            return JsonResponse({
                'message': {
                    'text': '글로벌 캠퍼스의 학식'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원']
                }
            })
        elif user_type == 'seoul':
            return JsonResponse({
                'message': {
                    'text': '서울 캠퍼스의 학식'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['인문관', '교수회관', '스카이 라운지']
                }
            })
        else:
            return JsonResponse({
                'message': {
                    'text': '학식 오류. 개발자에게 문의하세요'
                },
                'type': 'buttons',
                'buttons': button_info
            })

    elif content_name == '도서관':
        if user_type == 'seoul':
            lib_data = seo_library(content_name)
            buttons = ['4층 제1열람실(A): ' + str(lib_data['4-1A'] + '%'),
                    '4층 제1열람실(B): ' + str(lib_data['4-1B'] + '%'),
                    '4층 제2열람실(노트북): ' + str(lib_data['4-2'] + '%'),
                    '5층 제3열람실(A): ' + str(lib_data['5-3A'] + '%'),
                    '5층 제3열람실(B): ' + str(lib_data['5-3B'] + '%'), '5층 제4열람실: ' + str(lib_data['5-4'] + '%')
                        ]
            end_time = time.time()
            print(end_time - start_time)
            return JsonResponse({
                'message': {
                    'text': '열람실을 선택하세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': buttons
                }

            })
        elif user_type == 'global':
            lib_data = glo_library(content_name)
            buttons = ['3층 1열람실: ' + str(lib_data['3-1']) + '%',
                       '3층 2열람실: ' + str(lib_data['3-2']) + '%',
                       '4층 3열람실A: ' + str(lib_data['4-3A']) + '%',
                       '4층 3열람실B: ' + str(lib_data['4-3B']) + '%'
                       ]

            end_time = time.time()
            print(end_time - start_time)
            return JsonResponse({
                'message': {
                    'text': '열람실을 선택하세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': buttons
                }

            })


    elif '열람실' in content_name:
        if user_type == 'seoul':
            if '4층 제1열람실(A)' in content_name:
                name = "4층 제1열람실(A) 현황: "
                lib_num = 1
                room_no = 1
            elif '4층 제1열람실(B)' in content_name:
                name = "4층 제1열람실(B) 현황: "
                lib_num = 2
                room_no = 2
            elif '4층 제2열람실(노트북)' in content_name:
                name = '4층 제2열람실(노트북) 현황: '
                lib_num = 3
                room_no = 3
            elif '5층 제3열람실(A)' in content_name:
                name = '5층 제3열람실(A) 현황: '
                lib_num = 4
                room_no = 4
            elif '5층 제3열람실(B)' in content_name:
                name = '5층 제3열람실(B) 현황: '
                lib_num = 5
                room_no = 5
            elif '5층 제4열람실' in content_name:
                name = '5층 제4열람실 현황: '
                lib_num = 6
                room_no = 6

            lib_data = seo_library(lib_num)
            end_time = time.time()
            print(end_time - start_time)
            return JsonResponse({
                'message': {
                    'text': name + str(lib_data['%']) + '%' + '\n이용자 수: ' + str(lib_data['이용자']) +
                            '명\n남은 좌석 수: ' + str(lib_data['남은 좌석']),
                    'message_button': {
                        'label': '좌석보기',
                        'url': 'http://203.232.237.8/domian5/roomview5.asp?room_no=' + str(room_no)
                    }
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })

        elif user_type == 'global':
            if '3층 1열람실: ' in content_name:
                name = "3층 1열람실 현황: "
                lib_num = 1
                room_no = 8
            elif '3층 2열람실: ' in content_name:
                name = "3층 2열람실 현황: "
                lib_num = 2
                room_no = 9
            elif '4층 3열람실A: ' in content_name:
                name = "4층 3열람실A 현황: "
                lib_num = 3
                room_no = 10
            elif '4층 3열람실B: ' in content_name:
                name = "4층 3열람실B 현황: "
                lib_num = 4
                room_no = 11
            lib_data = glo_library(lib_num)

            end_time = time.time()
            print(end_time - start_time)
            return JsonResponse({
                'message': {
                    'text': name + str(lib_data['%']) + '%' + '\n이용자 수: ' + str(lib_data['이용자']) +
                            '명\n남은 좌석 수: ' + str(lib_data['남은 좌석']),
                    'message_button': {
                        'label': '좌석보기',
                        'url': 'http://203.232.237.8/domian5/roomview5.asp?room_no=' + str(room_no)
                    }
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })
        else:
            return JsonResponse({
                'message': {
                    'text': '도서관 오류. 개발자에게 문의하세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })

    elif content_name in ('인문관', '교수회관', '스카이 라운지'):
            text = str(today_date) + ' ' + content_name + '의 메뉴\n' + str(seo_crawl(content_name))
            end_time = time.time()
            print(end_time - start_time)
            return JsonResponse({
                'message': {
                    'text': text
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })

    elif content_name in ('후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원'):
        text = str(today_date) + ' ' + content_name + '의 메뉴\n' + str(glo_crawl(content_name))
        end_time = time.time()
        print(end_time - start_time)
        return JsonResponse({
            'message': {
                'text': text
                },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_info
            }
    })
    else:
        return JsonResponse({
            'message': {
                'text': "이걸 보고계시다면 오류입니다, 개발자에게 알려주세요"
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_info
            }
        })

def glo_crawl(cafeteria):
    start = time.time()
    today = datetime.date.today()
    today_d = today.strftime("%Y%m%d")

    if cafeteria == "후생관":
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%C8%C4%BB%FD%B0%FC+%C7%D0%BB%FD%BD%C4%B4%E7&caf_id=h203')
    elif cafeteria == "어문관":
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%BE%EE%B9%AE%B0%FC&caf_id=h204')
    elif cafeteria == "기숙사 식당":
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=HufsDorm+%BD%C4%B4%E7&caf_id=h205')
    elif cafeteria == "교직원 식당":
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%C8%C4%BB%FD%B0%FC+%B1%B3%C1%F7%BF%F8%BD%C4%B4%E7&caf_id=h202')
    elif cafeteria == "국제사회교육원":
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%B1%B9%C1%A6%BB%E7%C8%B8%B1%B3%C0%B0%BF%F8%BD%C4%B4%E7&caf_id=h201')

    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    my_titles = soup.select(
        'tr'
    )
    data = []
    cafe_menu = []

    for title in my_titles:
        data.append(title.text)

    for i in data:
        if len(data) == 1:
            cafe_menu.append(i)
            return "  오늘은 학식이 없어요!"
        else:
            if "\n" in i:
                if "방학 중" in i:
                    break
                elif '우리 식당은' in i:
                    break
                elif '농협' in i:
                    break
                else:
                    i = i.replace('\n', ' ').replace('&', '').replace('*', '').split()
                    cafe_menu.append(i)

    menu = ''
    menu_size = len(cafe_menu)

    for size in range(1, menu_size):
        time_size = len(cafe_menu[size])

        menu = menu + '\n----------------\n'

        for what in range(0, time_size):
            if what == (time_size-1):
                if cafeteria == "국제사회교육원":
                    menu = menu + cafe_menu[size][what] + '\n'
                else:
                    menu = menu + '\n   가격 : ' + cafe_menu[size][what]
            elif what == 0:
                menu = menu + cafe_menu[size][what] + '\n\n'
            else:
                menu = menu + cafe_menu[size][what] + '\n'

    stop = time.time()
    print(stop - start)
    return menu


def seo_crawl(cafeteria):
    start = time.time()
    today = datetime.date.today()
    today_d = today.strftime("%Y%m%d")

    if cafeteria == '인문관':
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%C0%CE%B9%AE%B0%FC%BD%C4%B4%E7&caf_id=h101')
    elif cafeteria == '교수회관':
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%B1%B3%BC%F6%C8%B8%B0%FC%BD%C4%B4%E7&caf_id=h102')
    elif cafeteria == '스카이 라운지':
        req = requests.get('https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=%BD%BA%C4%AB%C0%CC%B6%F3%BF%EE%C1%F6&caf_id=h103')

    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    my_titles = soup.select(
        'tr'
    )
    data = []
    cafe_menu = []

    for title in my_titles:
        data.append(title.text)

    for i in data:
        if len(data) == 1:
            cafe_menu.append(i)
            # return "오늘은 학식이 없어요!"
        else:
            if "\n" in i:
                i = i.replace('\n', ' ').replace('&', ' ').replace('*', ' ').split()

                if '메뉴는' in i[1]:
                    # 교수회관
                    break
                elif '닭강정-' in i[0]:
                    # 인문관
                    break
                elif '※' in i[0]:
                    # 스카이라운지
                    break
                cafe_menu.append(i)

    menu_size = len(cafe_menu)
    menu = ''

    for size in range(1, menu_size):
        time_size = len(cafe_menu[size])
        menu = menu + '\n----------------\n'

        for what in range(0, time_size):
            if what == 0:
                menu = menu + cafe_menu[size][what] + '\n\n'
            elif cafe_menu[size][what].isdigit() == 1:
                # Kcal앞 숫자의 경우에
                menu = menu + cafe_menu[size][what]
            else:
                menu = menu + cafe_menu[size][what] + '\n'
    return menu

def glo_library(name):
    req = urllib.request.urlopen('http://203.232.237.8/domian5/2/domian5.asp')
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
    req = urllib.request.urlopen('http://203.232.237.8/domian5/domian5.asp')
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
"""
@csrf_exempt
def friend_add(request):
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    print('친구 등록 하였습니다' + received_json_data)


@csrf_exempt
def friend_remove(request):
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    print('친구 삭제 하였습니다' + received_json_data)
"""






