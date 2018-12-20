from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hufscoops.models import Log, Menu
import datetime
import json
import sqlite3
import time
from . import haksik_db_to
from . import library_crawl
from .gnuvill.find_members import gnuvill_find_members
#from .markov_chat.rep import make_reply
H_buttons= ['학식', '내일의 학식', '시간별 학식', '이미지 학식', '도서관', '캠퍼스 변경']
ex_ip = 'http://huformation.aaronroh.org:8001'

def keyboard(request):

    #'buttons': ['학식', '이미지 학식', '시간별 학식', '도서관', '캠퍼스 변경']
    return JsonResponse({
        'type': 'buttons',
        'buttons': H_buttons
    })


@csrf_exempt
def message(request):
    button_info = H_buttons
    glo_info = ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원']
    glo_tomorrow_info=['=후생관=', '=어문관=', '=기숙사 식당=', '=교직원 식당=', '=국제사회교육원=']
    seo_info=['인문관', '교수회관', '스카이 라운지']
    seo_tomorrow_info=['=인문관=', '=교수회관=', '=스카이 라운지=']
    user_type = 'NO'
    start_time = time.time()
    today = datetime.date.today()
    today_date = today.strftime('%m월 %d일')
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    content_name = received_json_data['content']

    create_log(content_name)
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

        """
            elif (content_name == "대화하기") and (content_type=="buttons"):
        
        마르코브체인 이용한 채팅학습

        
        return JsonResponse({
            'message': {
                'text': "훕포메이션과 채팅을 시작합니다\n말한 내용은 모두 학습합니다.\n종료를 원하시면 `종료`라고 적어주세요"
            },
            'keyboard': {
                'type': 'text'
            }

        })

    elif content_type=='text':
        return JsonResponse({
            'message': {
                'text': make_reply(content_name)
            },
            'keyboard': {
                'type': 'text'
            }

        })
    elif "종료" in content_name and content_type=='text':
        return JsonResponse({
            'message': {
                'text': '훕포메이션과의 채팅을 종료합니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_info
            }
        })
        """





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
        print("글로벌 유저\n")
    elif "서울" in data:
        user_type = 'seoul'
        print("서울 유저\n")
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
                    'buttons': glo_info
                }
            })
        elif user_type == 'seoul':
            return JsonResponse({
                'message': {
                    'text': '서울 캠퍼스의 학식'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': seo_info
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
            """
            buttons = ['4층 제1열람실(A): ' + str(lib_data['4-1A'] + '%'),
                    '4층 제1열람실(B): ' + str(lib_data['4-1B'] + '%'),
                    '4층 제2열람실(노트북): ' + str(lib_data['4-2'] + '%'),
                    '5층 제3열람실(A): ' + str(lib_data['5-3A'] + '%'),
                    '5층 제3열람실(B): ' + str(lib_data['5-3B'] + '%'), '5층 제4열람실: ' + str(lib_data['5-4'] + '%')
                        ]
            """

            buttons = ['열람실(A): ' + str(lib_data['room-A'] + "%"),
                       '열람실(B): ' + str(lib_data['room-B'] + "%"),
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

            """
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
            """

            if "열람실(A)" in content_name:
                name = "열람실(A) 현황: "
                lib_num = 1
                room_no = 1
            elif "열람실(B)" in content_name:
                name = "열람실(B) 현황: "
                lib_num = 2
                room_no = 2

            lib_data = library_crawl.seo_library(lib_num)
            end_time = time.time()
            print(end_time - start_time)
            print(lib_data)
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
            listing = haksik_db_to.db_send(content_name, 'today')
            text = str(listing[1]) + ' ' + content_name + '의 메뉴\n' + str(listing[0])
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

    elif '시간별 학식' in content_name:

        now = datetime.datetime.now()
        nowHour = now.strftime('%H')
        if int(nowHour) <= 10:
            cafeteria_time = '아침'
        elif int(nowHour) <= 15:
            cafeteria_time = '점심'
        else:
            cafeteria_time = '저녁'

        text = str(today_date) + ' ' + cafeteria_time + ' 메뉴\n' + str(haksik_db_to.db_time_send(user_type, cafeteria_time))

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

    elif content_name == '이미지 학식':
        today_d = today.strftime('%Y%m%d')
        today_newtype = today.strftime("%m월 %d일")
        if user_type == 'seoul':
            return JsonResponse({
                'message': {
                    'text': '훕포메이션의 ' + str(today_newtype) + '\n점심시간 메뉴판',
                    'photo': {
                        'url': 'http://' + ex_ip + '/static/img/' + 'seoul'+today_d+'.png',
                        'width': 350,
                        'height': 600
                    },
                },

                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })
        elif user_type == 'global':
            return JsonResponse({
                'message': {
                    'text': '훕포메이션의 ' + str(today_newtype) + '\n점심시간 메뉴판',
                    'photo': {
                        'url': 'http://' + ex_ip + '/static/img/' +'global'+today_d+'.png',
                        'width': 350,
                        'height': 600
                    },
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_info
                }
            })
        else:
            return JsonResponse({
                'message': {
                    'text': '최초 캠퍼스 설정 값이 없습니다\n캠퍼스를 골라주세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['서울', '글로벌']
                }
            })
    elif content_name == '내일의 학식':
        if user_type == 'global':
            return JsonResponse({
                'message': {
                    'text': '내일의 학식, 식당을 선택하세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': glo_tomorrow_info
                }
            })
        elif user_type == 'seoul':
            return JsonResponse({
                'message': {
                    'text': '내일의 학식, 식당을 선택하세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': seo_tomorrow_info
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
    elif content_name in ['=후생관=', '=어문관=', '=기숙사 식당=', '=교직원 식당=', '=국제사회교육원=', '=인문관=',
                          '=교수회관=', '=스카이 라운지=']:
        content_name = content_name.replace('=', '').replace('=', '')
        #=없애는 작업

        listing = haksik_db_to.db_send(content_name, 'tomorrow')
        text = str(listing[1]) + ' ' + content_name + '의 메뉴\n' + str(listing[0])
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

    elif content_name == "(~9/5)그누빌 SW동아리 모집":
        return JsonResponse({
            'message' : {
                'text': gnuvill_find_members()
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
def glo_post(request):
    cafeterias = ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원']
    return render(request, 'blog/templates/seo_haksik_table.html', {'cafeterias': cafeterias})

def seo_post(request):
    cafeterias = ['인문관', '교수회관', '스카이 라운지']
    return render(request, 'blog/templates/seo_haksik_table.html', {'cafeterias': cafeterias})

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
    return render(request, 'blog/seo_haksik_table.html', {})
"""
def create_menu_db_table(cafe_name, time, menu):
    Menu.objects.create(
        cafe_name=cafe_name,
        time=time,
        menu=menu,
        is_new=True
    )

def create_log(cafe_name):
    Log.objects.create(
        cafe_name = cafe_name,
    )


def flush_menu_db():
    menu_db = Menu.objects.all()
    menu_db.delete()

def analysis(request):

    context = {}
    context['date_pack'] = get_date_pack()
    context['total_request_data'] = get_total_request_data()
    context['seven_days_request_data'] = get_seven_days_request_data()
    context['request_data_by_cafe'] = get_request_data_by_cafe()
    context['weekday_request_data'] = get_weekday_request_data()
    context['hourly_request_data'] = get_hourly_request_data()
    context['request_by_time_data'] = get_time_request_data()

    return TemplateResponse(request, "index.html", context)


def get_today_date():

    return datetime.date.today()


def get_date_pack():
    days = 7
    today_date = get_today_date()
    date_pack = ['x']

    for i in reversed(range(days)):
        date = today_date - datetime.timedelta(days=i)
        date_pack.append(
            date.strftime('%Y-%m-%d')
        )

    return date_pack


def get_total_request_data():
    today_date = get_today_date()
    days_since_open = (today_date - datetime.date(2017, 9, 1)).days
    zero_data = ['요청횟수']
    total_request_data = ['요청횟수']

    for i in reversed(range(days_since_open)):
        total_request_data.append(
            Log.objects.filter(
                timestamp__range=[today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)]
            ).count()
        )
        zero_data.append(0)

    return dict(
        total_request_data=total_request_data,
        zero_data=zero_data,
    )


def get_seven_days_request_data():
    days = 7
    today_date = get_today_date()
    cnt_request = ['요청횟수']

    for i in reversed(range(days)):
        cnt_request.append(
            Log.objects.filter(
                timestamp__range = (today_date - datetime.timedelta(days=i),
                                    today_date + datetime.timedelta(days=1-i))
            ).count()
        )

    return cnt_request


def get_request_data_by_cafe():
    days = 7
    today_date = get_today_date()

    cnt_hooseng = ['후생관']
    cnt_umoon = ['어문관']
    cnt_dorm = ['기숙사 식당']
    cnt_hooseng_gyo = ['교직원 식당']
    cnt_gookje = ['국제사회교육원']
    cnt_inmoon = ['인문관']
    cnt_gyo = ['교수회관']
    cnt_sky = ['스카이 라운지']
    cnt_image=['이미지 학식']

    cnt_haksik = ['학식']
    cnt_tomorrow_haksik = ['내일의 학식']
    cnt_time_haksik = ['시간별 학식']
    cnt_lib = ['도서관']
    cnt_campus_change = ['캠퍼스 변경']

    for i in reversed(range(days)):
        cnt_hooseng.append(
            Log.objects.filter(
                cafe_name='후생관',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_umoon.append(
            Log.objects.filter(
                cafe_name='어문관',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_dorm.append(
            Log.objects.filter(
                cafe_name='기숙사 식당',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_hooseng_gyo.append(
            Log.objects.filter(
                cafe_name='교직원 식당',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_gookje.append(
            Log.objects.filter(
                cafe_name='국제사회교육원',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_inmoon.append(
            Log.objects.filter(
                cafe_name='인문관',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_gyo.append(
            Log.objects.filter(
                cafe_name='교수회관',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_sky.append(
            Log.objects.filter(
                cafe_name='스카이 라운지',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_haksik.append(
            Log.objects.filter(
                cafe_name='학식',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_tomorrow_haksik.append(
            Log.objects.filter(
                cafe_name='내일의 학식',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_time_haksik.append(
            Log.objects.filter(
                cafe_name='시간별 학식',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_lib.append(
            Log.objects.filter(
                cafe_name='도서관',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_campus_change.append(
            Log.objects.filter(
                cafe_name='캠퍼스 변경',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_campus_change.append(
            Log.objects.filter(
                cafe_name='이미지 학식',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )

    return dict(
        cnt_hooseng=cnt_hooseng,
        cnt_umoon=cnt_umoon,
        cnt_dorm=cnt_dorm,
        cnt_hooseng_gyo=cnt_hooseng_gyo,
        cnt_gookje=cnt_gookje,
        cnt_inmoon=cnt_inmoon,
        cnt_gyo=cnt_gyo,
        cnt_sky=cnt_sky,
        cnt_haksik = cnt_haksik,
        cnt_tomorrow_haksik = cnt_tomorrow_haksik,
        cnt_time_haksik = cnt_time_haksik,
        cnt_lib = cnt_lib,
        cnt_campus_change = cnt_campus_change,
        cnt_image=cnt_image,
    )


def get_weekday_request_data():
    weekday_request_data = ['요청횟수']
    for i in range(1,8):
        weekday_request_data.append(
            Log.objects.filter(
                timestamp__week_day=i
            ).count()
        )

    return weekday_request_data


def get_hourly_request_data():
    hourly_request_data = ['요청횟수']
    for i in range(24):
        hourly_request_data.append(
            Log.objects.filter(
                timestamp__hour=i
            ).count()
        )

    return hourly_request_data


def get_time_request_data():
    days=7
    today_date = get_today_date()
    cnt_lunch = ['중식']
    cnt_dinner = ['석식']

    for i in reversed(range(days)):
        cnt_lunch.append(
            Log.objects.filter(
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)),
                timestamp__hour__lt = 15
            ).count()
        )
        cnt_dinner.append(
            Log.objects.filter(
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)),
                timestamp__hour__gte=15
            ).count()
        )

    return dict(
        cnt_lunch=cnt_lunch,
        cnt_dinner=cnt_dinner
    )



