import sqlite3
import random
import datetime
#from django.shortcuts import render

def db_send(cafeteria, dates):

    if dates == 'today':
        today = datetime.date.today()
        today_date = today.strftime('%m월 %d일')
        con = sqlite3.connect("./DB/haksik_data.db")
        cur = con.cursor()

    elif dates == 'tomorrow':
        today = datetime.date.today() + datetime.timedelta(days=1)
        today_date = today.strftime('%m월 %d일')
        con = sqlite3.connect("./DB/tomorrow_haksik_data.db")
        cur = con.cursor()
    else:
        con = sqlite3.connect("./DB/haksik_data.db")
        cur = con.cursor()

    line_mark = '_____________________'
    if cafeteria == '인문관':
        cur.execute("SELECT breakfast from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT breakfast from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT breakfast from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT breakfast from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT breakfast from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT breakfast from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT breakfast from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT breakfast from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) == 0:
            pass
        else:
            haksik_list.append(info[i][0])

    #print(haksik_list)
    count = len(haksik_list)
    # print(num)
    # print(cur.fetchone()[0])
    # 메뉴 개수
    menu = ''
    for i in range(0, count):
        menu = menu + '\n' + line_mark + '\n' + str(haksik_list[i])

    if cafeteria == '인문관':
        cur.execute("SELECT lunch from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT lunch from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT lunch from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT lunch from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT lunch from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT lunch from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT lunch from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT lunch from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) <= 3:
            pass
        else:
            haksik_list.append(info[i][0])

    #print(haksik_list)
    count = len(haksik_list)
    # print(num)
    # print(cur.fetchone()[0])
    # 메뉴 개수
    for i in range(0, count):
        if haksik_list[i] in menu:
            pass
        else:
            menu = menu + '\n' + line_mark + '\n' + str(haksik_list[i])

    if cafeteria == '인문관':
        cur.execute("SELECT dinner from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT dinner from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT dinner from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT dinner from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT dinner from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT dinner from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT dinner from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT dinner from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    #print(info)
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) <= 4:
            pass
        else:
            haksik_list.append(info[i][0])

    #print(haksik_list)
    count = len(haksik_list)
    # print(num)
    # print(cur.fetchone()[0])
    # 메뉴 개수
    for i in range(0, count):
        if haksik_list[i] in menu:
            pass
        else:
            menu = menu + '\n' + str(line_mark) + '\n' + str(haksik_list[i])

    con.close()

    if len(menu) <= 27:

        emoti = '(허걱)', '(멘붕)', '(깜짝)', '(허걱)', '(부르르)', '(훌쩍)', '(우와)', '(심각)', '(헉)'
        menu = '\n오늘은 학식이 없어요 ' + random.choice(emoti)

    return [menu, today_date]



def db_time_send(campus, cafe_time):
    con = sqlite3.connect("./DB/haksik_data.db")
    cur = con.cursor()

    menu = ''

    today = datetime.date.today()
    today_date = today.strftime('%m월 %d일')

    if cafe_time == '아침':
        sentence = 'breakfast'
    elif cafe_time == '점심':
        sentence = 'lunch'
    elif cafe_time == '저녁':
        sentence = 'dinner'

    if campus == 'seoul':
        cafeteria = ["인문관", "교수회관", "스카이라운지"]
    elif campus == 'global':
        cafeteria = ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원']

    for j in range(0, len(cafeteria)):
        querys = "SELECT " + sentence + " from " + cafeteria[j]

        cur.execute(querys)
        haksik_list = []
        info = cur.fetchall()
        num = len(info)

        for i in range(0, num):
            if len(info[i][0]) == 0:
                pass
            else:
                haksik_list.append(info[i][0])

        count = len(haksik_list)

        for i in range(0, count):
            if len(str(haksik_list[i])) < 4:
                continue
            menu = menu + '\n' + '_____________' + '\n' + cafeteria[j] + ' 메뉴\n' + str(haksik_list[i])

    con.close()

    if len(menu) <= 18:
        emoti = '(허걱)', '(멘붕)', '(깜짝)', '(허걱)', '(부르르)', '(훌쩍)', '(우와)', '(심각)', '(헉)'
        menu = '\n오늘은 학식이 없어요 ' + random.choice(emoti)

    return menu

"""
def template(campus, cafe_time):

    con = sqlite3.connect('./DB/haksik_data.db')
    cur = con.cursor()

    if cafe_time == '아침':
        sentence = 'breakfast'
    elif cafe_time == '점심':
        sentence = 'lunch'
    elif cafe_time == '저녁':
        sentence = 'dinner'

    if campus == 'seoul':
        cafeteria = ["인문관", "교수회관", "스카이라운지"]
    elif campus == 'global':
        cafeteria = ['후생관', '어문관', '기숙사 식당', '교직원 식당', '국제사회교육원']

    cafemenu = []
    return render(request, 'blog/glo_haksik_table.html', {'posts': posts}



template('global', '점심')
"""








"""
    elif campus == '글로벌':

    if cafeteria == '아침':
        cur.execute("SELECT breakfast from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT breakfast from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT breakfast from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT breakfast from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT breakfast from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT breakfast from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT breakfast from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT breakfast from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) == 0:
            pass
        else:
            haksik_list.append(info[i][0])

    count = len(haksik_list)

    # 메뉴 개수
    menu = ''
    for i in range(0, count):
        menu = menu + '\n' + '_____________' + '\n' + str(haksik_list[i])

    if cafeteria == '인문관':
        cur.execute("SELECT lunch from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT lunch from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT lunch from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT lunch from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT lunch from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT lunch from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT lunch from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT lunch from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) <= 2:
            pass
        else:
            haksik_list.append(info[i][0])

    #print(haksik_list)
    count = len(haksik_list)
    # print(num)
    # print(cur.fetchone()[0])
    # 메뉴 개수
    for i in range(0, count):
        if haksik_list[i] in menu:
            pass
        else:
            menu = menu + '\n' + '_____________' + '\n' + str(haksik_list[i])

    if cafeteria == '인문관':
        cur.execute("SELECT dinner from 인문관")
    elif cafeteria == '교수회관':
        cur.execute("SELECT dinner from 교수회관")
    elif cafeteria == '스카이 라운지':
        cur.execute("SELECT dinner from 스카이라운지")
    elif cafeteria == '후생관':
        cur.execute("SELECT dinner from 후생관")
    elif cafeteria == '어문관':
        cur.execute("SELECT dinner from 어문관")
    elif cafeteria == '기숙사 식당':
        cur.execute("SELECT dinner from 기숙사")
    elif cafeteria == '교직원 식당':
        cur.execute("SELECT dinner from 교직원")
    elif cafeteria == '국제사회교육원':
        cur.execute("SELECT dinner from 국제사회교육원")

    haksik_list = []
    info = cur.fetchall()
    #print(info)
    num = len(info)

    for i in range(0, num):
        if len(info[i][0]) == 0:
            pass
        else:
            haksik_list.append(info[i][0])

    #print(haksik_list)
    count = len(haksik_list)
    # print(num)
    # print(cur.fetchone()[0])
    # 메뉴 개수
    for i in range(0, count):
        if haksik_list[i] in menu:
            pass
        else:
            menu = menu + '\n' + '_____________' + '\n' + str(haksik_list[i])

    con.close()

    if len(menu) <= 16:

        emoti = '(허걱)', '(멘붕)', '(깜짝)', '(허걱)', '(부르르)', '(훌쩍)', '(우와)', '(심각)', '(헉)'
        menu = '\n오늘은 학식이 없어요 ' + random.choice(emoti)

    return menu
"""
