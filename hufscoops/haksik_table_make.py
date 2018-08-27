import sqlite3
from django.shortcuts import render
import datetime

def to_seo_table(request):

    context = {}
    context['menu'] = seo_haksik_load()
    # 식단표 단어별로 분류 완료

    #print(context['menu'])
    #print(context)
    return render(request, 'seo_haksik_table.html', context)

def to_glo_table(request):

    context = {}
    context['menu'] = glo_haksik_load()
    # 식단표 단어별로 분류 완료

    #print(context['menu'])
    #print(context)
    return render(request, 'glo_haksik_table.html', context)

def seo_haksik_load():

    t = ['월', '화', '수', '목', '금', '토', '일']
    r = datetime.datetime.today().weekday()
    days = t[r]

    all_menu = {}

    time = 'lunch'
    menu_list = formatted_haksik(time, '인문관')
    #print(menu_list)
    try:
        if len(menu_list) == 1:
            inmoon_menu = dict(
                inmoon_today_menu0=menu_list[0][1],
                inmoon_today_price0=menu_list[0][-1],
            )
        elif len(menu_list) == 2:
            inmoon_menu = dict(
                inmoon_today_menu0=menu_list[0][1],
                inmoon_today_price0=menu_list[0][-1],
                inmoon_today_menu1=menu_list[1][1],
                inmoon_today_price1=menu_list[1][-1],
            )
        elif len(menu_list) == 3:
            inmoon_menu = dict(
                inmoon_today_menu0=menu_list[0][1],
                inmoon_today_price0=menu_list[0][-1],
                inmoon_today_menu1=menu_list[1][1],
                inmoon_today_price1=menu_list[1][-1],
                inmoon_today_menu2=menu_list[2][1],
                inmoon_today_price2=menu_list[2][-1],
            )
            all_menu.update(inmoon_menu)
    except:
        pass

    #print(inmoon_menu)
    menu_list = formatted_haksik(time, '교수회관')

    try:
        if len(menu_list) == 1:
            gyosoo_menu = dict(
                gyosoo_today_menu0=menu_list[0][1],
                gyosoo_today_price0=menu_list[0][-1],
            )
        elif len(menu_list) == 2:
            gyosoo_menu = dict(
                gyosoo_today_menu0=menu_list[0][1],
                gyosoo_today_price0=menu_list[0][-1],
                gyosoo_today_menu1=menu_list[1][1],
                gyosoo_today_price1=menu_list[1][-1],
            )
        all_menu.update(gyosoo_menu)
    except:
        pass

    menu_list = formatted_haksik(time, '스카이라운지')

    try:
        if len(menu_list) == 1:
            lounge_menu = dict(
                lounge_today_menu0=menu_list[0][1],
                lounge_today_price0=menu_list[0][-1],
            )
        elif len(menu_list) == 2:
            lounge_menu = dict(
                lounge_today_menu0=menu_list[0][1],
                lounge_today_price0=menu_list[0][-1],
                lounge_today_menu1=menu_list[1][1],
                lounge_today_price1=menu_list[1][-1],
            )

        all_menu.update(lounge_menu)
    except:
        pass
    #print(menu_list)
    #print(all_menu)
    return all_menu


def glo_haksik_load():
    all_menu = {}
    time='lunch'


    menu_list=formatted_haksik(time, '후생관')
    try:
        if len(menu_list)==0:
            hooseng_menu=dict()

        elif len(menu_list)==1:
            hooseng_menu=dict(
                hooseng_today_menu0=menu_list[0][1],
                hooseng_today_price0=menu_list[0][-1],
            )
        elif len(menu_list)==2:
            hooseng_menu=dict(
                hooseng_today_menu0=menu_list[0][1],
                hooseng_today_price0=menu_list[0][-1],
                hooseng_today_menu1=menu_list[1][1],
                hooseng_today_price1=menu_list[1][-1],

            )
        elif len(menu_list)==3:
            hooseng_menu=dict(
                hooseng_today_menu0=menu_list[0][1],
                hooseng_today_price0=menu_list[0][-1],
                hooseng_today_menu1=menu_list[1][1],
                hooseng_today_price1=menu_list[1][-1],
                hooseng_today_menu2=menu_list[2][1],
                hooseng_today_price2=menu_list[2][-1],
            )
        elif len(menu_list)==4:
            hooseng_menu=dict(
                hooseng_today_menu0=menu_list[0][1],
                hooseng_today_price0=menu_list[0][-1],
                hooseng_today_menu1=menu_list[1][1],
                hooseng_today_price1=menu_list[1][-1],
                hooseng_today_menu2=menu_list[2][1],
                hooseng_today_price2=menu_list[2][-1],
                hooseng_today_menu3=menu_list[3][1],
                hooseng_today_price3=menu_list[3][-1],
            )
        elif len(menu_list)==5:
            hooseng_menu=dict(
                hooseng_today_menu0=menu_list[0][1],
                hooseng_today_price0=menu_list[0][-1],
                hooseng_today_menu1=menu_list[1][1],
                hooseng_today_price1=menu_list[1][-1],
                hooseng_today_menu2=menu_list[2][1],
                hooseng_today_price2=menu_list[2][-1],
                hooseng_today_menu3=menu_list[3][1],
                hooseng_today_price3=menu_list[3][-1],
                hooseng_today_menu4=menu_list[4][1],
                hooseng_today_price4=menu_list[4][-1],
            )
    except:
        pass

    all_menu.update(hooseng_menu)

    menu_list=formatted_haksik(time, '교직원')

    try:
        if len(menu_list)==0:
            gyojik_menu=dict()
        elif len(menu_list)==1:
            gyojik_menu=dict(
                gyojik_today_menu0=menu_list[0][1],
                gyojik_today_price0=menu_list[0][-1],
            )
        elif len(menu_list)==2:
            gyojik_menu=dict(
                gyojik_today_menu0=menu_list[0][1],
                gyojik_today_price0=menu_list[0][-1],
                gyojik_today_menu1=menu_list[1][1],
                gyojik_today_price1=menu_list[1][-1],
            )
    except:
        pass
    all_menu.update(gyojik_menu)

    menu_list=formatted_haksik(time, '어문관')

    try:
        umoon_menu = dict(
        )
        if len(menu_list)==1:
            umoon_menu=dict(
                umoon_today_menu0=menu_list[0][1],
                umoon_today_price0=menu_list[0][-1],
            )
        elif len(menu_list)==2:
            umoon_menu=dict(
                umoon_today_menu0=menu_list[0][1],
                umoon_today_price0=menu_list[0][-1],
                umoon_today_menu1=menu_list[1][1],
                umoon_today_price1=menu_list[1][-1],
            )
    except:
        pass
    all_menu.update(umoon_menu)

    menu_list=formatted_haksik(time, '기숙사')

    try:
        if len(menu_list)==0:
            hufsdorm_menu=dict()

        elif len(menu_list)==1:
            hufsdorm_menu=dict(
                hufsdorm_today_menu0=menu_list[0][1],
                hufsdorm_today_price0=menu_list[0][-1],
            )
        elif len(menu_list) == 2:
            hufsdorm_menu = dict(
            hufsdorm_today_menu0=menu_list[0][1],
            hufsdorm_today_price0=menu_list[0][-1],
            hufsdorm_today_menu1=menu_list[1][1],
            hufsdorm_today_price1=menu_list[1][-1],
            )
        elif len(menu_list) == 3:
            hufsdorm_menu = dict(
            hufsdorm_today_menu0=menu_list[0][1],
            hufsdorm_today_price0=menu_list[0][-1],
            hufsdorm_today_menu1=menu_list[1][1],
            hufsdorm_today_price1=menu_list[1][-1],
            hufsdorm_today_menu2=menu_list[2][1],
            hufsdorm_today_price2=menu_list[2][-1],
            )
        elif len(menu_list) == 4:
            hufsdorm_menu = dict(
            hufsdorm_today_menu0=menu_list[0][1],
            hufsdorm_today_price0=menu_list[0][-1],
            hufsdorm_today_menu1=menu_list[1][1],
            hufsdorm_today_price1=menu_list[1][-1],
            hufsdorm_today_menu2=menu_list[2][1],
            hufsdorm_today_price2=menu_list[2][-1],
            hufsdorm_today_menu3=menu_list[3][1],
            hufsdorm_today_price3=menu_list[3][-1],
            )
        elif len(menu_list) == 5:
            hufsdorm_menu = dict(
            hufsdorm_today_menu0=menu_list[0][1],
            hufsdorm_today_price0=menu_list[0][-1],
            hufsdorm_today_menu1=menu_list[1][1],
            hufsdorm_today_price1=menu_list[1][-1],
            hufsdorm_today_menu2=menu_list[2][1],
            hufsdorm_today_price2=menu_list[2][-1],
            hufsdorm_today_menu3=menu_list[3][1],
            hufsdorm_today_price3=menu_list[3][-1],
            hufsdorm_today_menu4=menu_list[4][1],
            hufsdorm_today_price4=menu_list[4][-1],
            )
    except:
        pass
    all_menu.update(hufsdorm_menu)
    print(all_menu)
    #print(menu_list)
    return all_menu




def formatted_haksik(time, cafeteria):

    con = sqlite3.connect('./DB/haksik_data.db')
    cur = con.cursor()

    querys = 'SELECT ' + time + ' FROM ' + cafeteria
    cur.execute(querys)
    menu_size = len(cur.fetchall())
    cur.execute(querys)

    menu_list = []

    for i in range(0, menu_size):
        menu = cur.fetchone()[0]
        if len(menu) <= 1:
            continue
        else:
            menu_list.append(menu)

    for size in range(0, len(menu_list)):
        menu_list[size] = menu_list[size].split('\n')

        for i in range(0, len(menu_list[size])):
            try:
                menu_list[size].remove('')
                #print(menu_list)
# 어문관 작업중 .  2017-11-06

                for i in range(0,len(menu_list[size])):
                    if '선택식' in menu_list[size][i]:
                        #어문관일때 선택식으로 인한 가격수정
                        menu_list[size][-1] = str(menu_list[size][i-1]).replace('가격 : ', '')
                    else:
                        menu_list[size][-1] = menu_list[size][-1].replace('가격 : ', '')
            except:
                pass
    con.close()

    return menu_list
seo_haksik_load()
glo_haksik_load()