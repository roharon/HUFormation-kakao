import datetime
import json
import sqlite3
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import haksik_db_to
from . import library_crawl


# from bs4 import BeautifulSoup


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
    content_type = received_json_data['type']
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
            lib_data = library_crawl.seo_library(content_name)

            if lib_data == 555:
                return JsonResponse({
                    'message': {
                        'text': "도서관 좌석을 불러 올 수 없습니다.\n다시 이용해주세요",
                    },
                    'keyboard': {
                        'type': 'buttons',
                        'buttons': button_info
                    }
                })

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
            lib_data = library_crawl.glo_library(content_name)

            if lib_data == 555:
                return JsonResponse({
                    'message': {
                        'text': "도서관 좌석을 불러 올 수 없습니다.\n다시 이용해주세요",
                    },
                    'keyboard': {
                        'type': 'buttons',
                        'buttons': button_info
                    }
                })

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

            lib_data = library_crawl.seo_library(lib_num)
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
            lib_data = library_crawl.glo_library(lib_num)

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

    elif content_name in ('인문관', '교수회관', '스카이 라운지', '후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원'):
            text = str(today_date) + ' ' + content_name + '의 메뉴\n' + str(haksik_db_to.db_send(content_name))
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
        mess = "이걸 보고계시다면 오류입니다, 개발자에게 알려주세요"
        if content_type == 'photo':
            mess = "사진은 기능이 없어요, 버튼을 눌러주세요!"
        elif content_type == 'video':
            mess = "영상은 기능이 없어요, 버튼을 눌러주세요!"
        elif content_type == 'audio':
            mess = "녹음파일은 기능이 없어요, 버튼을 눌러주세요!"

        return JsonResponse({
            'message': {
                'text': mess
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_info
            }
        })



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

"""
def glo_post_haksik(request):
    posts = glo_c
    return render(request, 'blog/haksik_table.html', {})
"""




