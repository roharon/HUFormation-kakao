from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json, datetime
from django.http import JsonResponse
import requests
import urllib.request
from bs4 import BeautifulSoup


def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원', '도서관 좌석']
    })


@csrf_exempt
def message(request):
    today = datetime.date.today()
    today_date = today.strftime('%m월 %d일')
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    cafeteria_name = received_json_data['content']

    if cafeteria_name == '도서관 좌석':
        return JsonResponse({
            'message': {
                'text': '개발중인 기능입니다'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['3층 1열람실: ' + str(library_crawl(1)) + '%', '3층 2열람실: ' + str(library_crawl(2)) + '%', '4층 3열람실A: ' + str(library_crawl(3)) + '%',
                            '4층 3열람실B: ' + str(library_crawl(4)) + '%', '메인으로 가기']
            }

        })

    elif cafeteria_name == '메인으로 가기':
        return JsonResponse({
            'message': {
                'text': '메인으로 이동합니다'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원', '도서관 좌석']
            }
        })

    elif (cafeteria_name == '3층 1열람실: ' + str(library_crawl(1)) + '%' or cafeteria_name == '3층 2열람실: ' + str(library_crawl(2)) + '%'
          or cafeteria_name == '4층 3열람실A: ' + str(library_crawl(3)) + '%' or cafeteria_name == '4층 3열람실B: ' + str(library_crawl(4)) + '%'):

        if cafeteria_name == '3층 1열람실: ' + str(library_crawl(1)) + '%':
            name = "3층 1열람실 현황: "
            lib_num = 1
            room_no = 8
        elif cafeteria_name == '3층 2열람실: ' + str(library_crawl(2)) + '%':
            name = "3층 2열람실 현황: "
            lib_num = 2
            room_no = 9
        elif cafeteria_name == '4층 3열람실A: ' + str(library_crawl(3)) + '%':
            name = "4층 3열람실A 현황: "
            lib_num = 3
            room_no = 10
        elif cafeteria_name == '4층 3열람실B: ' + str(library_crawl(4)) + '%':
            name = "4층 3열람실B 현황: "
            lib_num = 4
            room_no = 11

        return JsonResponse({
            'message': {
                'text': name + str(library_crawl(lib_num)) + '%' + '\n\nhttp://203.232.237.8/domian5/2/roomview5.asp?room_no=' + str(room_no),
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원', '도서관 좌석']
            }
        })

    else:
        return JsonResponse({
            'message': {
                'text': str(today_date) + ' ' + cafeteria_name + '의 메뉴' + '\n' + str(crawl(cafeteria_name))
                },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원', '도서관 좌석']
            }
    })


def crawl(cafeteria):

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
    soup = BeautifulSoup(html, 'html.parser')
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
            return "오늘은 학식이 없어요!"
            #print('len이 1')
        else:
            if "\n" in i:
                if "방학 중" in i:
                    break
                else:
                    cafe_menu.append(i)
                    #print("len이 2")

    return cafe_menu[1]
    #print(cafe_menu)


def library_crawl(num):
    req = urllib.request.urlopen('http://203.232.237.8/domian5/2/domian5.asp')
    soup = BeautifulSoup(req, 'html.parser', from_encoding="utf-8")

    my_titles = soup.select(
        'tr'
    )
    data = []

    for title in my_titles:
        data.append(title.text)

    # data[3]은 3층 1열람실 내용
    return data[num+2].split()[6]









