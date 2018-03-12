from bs4 import BeautifulSoup
import datetime, requests
import random


def seo_crawl(cafeteria, date):
    today = datetime.date.today()

    if date == 'tomorrow':
        today = today + datetime.timedelta(days=1)


    today_d = today.strftime("%Y%m%d")
    today_w = today.strftime("%w")
    ##today_d = "20170615"
    try:
        if cafeteria == '인문관':
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=인문관식당&caf_id=h101')
        elif cafeteria == '교수회관':
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=교수회관식당&caf_id=h102')
        elif cafeteria == '스카이 라운지':
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=스카이라운지&caf_id=h103')
    except:
        error = "\n서울캠 로딩. 학교 사이트 점검중!\n학식내용을 불러올 수 없습니다."
        return error

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
            return "                "
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
    menu = ['','','','','','','','','']
    count = -1
    for size in range(1, menu_size):
        time_size = len(cafe_menu[size])
        if today_w == "6":      # 0은 일요일 6은 토요일
            if '인문관' in cafeteria:
                if size in [1, 3, 4]:
                    continue


        ##menu = menu + '\n----------------\n'
        count = count + 1
        for what in range(0, time_size):
            if what == 0:
                menu[count] = menu[count] + cafe_menu[size][what] + '\n\n'
            elif what == (time_size-1):
                menu[count] = menu[count] + '\n가격 : ' + cafe_menu[size][what]
            elif cafe_menu[size][what].isdigit() == 1:
                # Kcal앞 숫자의 경우에
                menu[count] = menu[count] + cafe_menu[size][what]
            else:
                menu[count] = menu[count] + cafe_menu[size][what] + '\n'


    if "인문관" in cafeteria:
        ##인문관 일요일 hfspn 뜨는 오류 수정
        size = len(menu)
        for i in range(0, size):
            if 'hfspn' in menu[i]:
                menu[i] = ''


    return menu


def glo_crawl(cafeteria, date):

    today = datetime.date.today()
    t = ['월', '화', '수', '목', '금', '토', '일']
    r = datetime.datetime.today().weekday()
    days = t[r]

    if date == 'tomorrow':
        today = today + datetime.timedelta(days=1)
        r = datetime.datetime.today().weekday()
        days = t[r]
    elif date == 'test':
        today = today + datetime.timedelta(days=3)
        r = datetime.datetime.today().weekday()
        days = t[r]

    today_d = today.strftime("%Y%m%d")
    end_d = today_d

    today_w = today.strftime("%w")
    ###today_d = "20170615"
    try:
        if cafeteria == "후생관":
            req = requests.get(
                'https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + end_d + '&caf_name=후생관+학생식당&caf_id=h203')
        elif cafeteria == "어문관":
            req = requests.get(
                'https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + end_d + '&caf_name=어문관&caf_id=h204')
        elif cafeteria == "기숙사 식당":
            req = requests.get(
                'https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + end_d + '&caf_name=HufsDorm+식당&caf_id=h205')
        elif cafeteria == "교직원 식당":
            req = requests.get(
                'https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + end_d + '&caf_name=후생관+교직원식당&caf_id=h202')
        elif cafeteria == "국제사회교육원":
            req = requests.get(
                'https://webs.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + end_d + '&caf_name=국제사회교육원식당&caf_id=h201')
    except:
        error = "\n글로벌캠 로딩. 학교 사이트 점검중!\n학식내용을 불러올 수 없습니다."
        return error

    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    my_titles = soup.select(
        'tr'
    )
    data = []
    cafe_menu = []

    for title in my_titles:
        title.text.replace('일품1','일품 ')
        title.text.replace('일품2', '일품 ')
        title.text.replace('일품3', '일품 ')
        data.append(title.text)


    for i in data:
        if len(data) == 1:
            cafe_menu.append(i)
            return "         "
        else:
            if "\n" in i:
                if "방학 중" in i:
                    break
                elif '우리 식당은' in i:
                    break
                elif '농협' in i:
                    break
                else:
                    if '어문관' in cafeteria:
                        if '1430' in i:
                            continue

                    i = i.replace('\n', ' ').replace('&', '').replace('*', '').split()
                    cafe_menu.append(i)


    menu = ['', '', '', '', '', '', '', '', '','','','','','','','']
    menu_size = len(cafe_menu)
    count = -1

    if cafeteria == "어문관":
        menu_size = len(cafe_menu)-1

    for size in range(1, menu_size):
        time_size = len(cafe_menu[size])
        ##menu = menu + '\n----------------\n'
        count += 1
        for what in range(0, time_size):

            if what == (time_size-1):
                if cafeteria == "국제사회교육원":
                    menu[count] = menu[count] + cafe_menu[size][what] + '\n'
                elif cafeteria == '어문관':
                    if size > 1:
                        try:
                            menu[count] = menu[count] + cafe_menu[size][what] + '\n'
                        except:
                            pass
                    else:
                        menu[count] = menu[count] + '\n가격 : ' + cafe_menu[size][what]
                        menu[count] = menu[count] + '\n\n선택식\n'
                else:
                    menu[count] = menu[count] + '\n가격 : ' + cafe_menu[size][what]
            elif what == 0:
                if cafeteria == '어문관':
                    if '1430' in cafe_menu[size][what]:
                        continue
                    else:
                        if '일품' in cafe_menu[size][what]:
                            menu[count] = menu[count] + cafe_menu[size][what] + '\n\n'
                        else:
                            try:
                                if '면' in cafe_menu[size][what]:
                                    menu[count] = menu[count] + cafe_menu[size][what]
                                else:
                                    menu[count] = menu[count] + cafe_menu[size][what] + ' : '
                            except:
                                print("Umoon error-select.")
                                break
                else:
                    try:
                        if cafeteria == '기숙사 식당':
                            if days in ['토', '일']:
                                if '0830~0900' in cafe_menu[size][what]:
                                    cafe_menu[size][what] = cafe_menu[size][what].replace('0830~0900', '08:00~09:00')
                                if '1730~1800' in cafe_menu[size][what]:
                                    cafe_menu[size][what] = cafe_menu[size][what].replace('1730~1800', '17:30~18:30')
                            else:
                                if '0830~0900' in cafe_menu[size][what]:
                                    cafe_menu[size][what] = cafe_menu[size][what].replace('0830~0900', '08:00~09:30')
                                if '1730~1800' in cafe_menu[size][what]:
                                    cafe_menu[size][what] = cafe_menu[size][what].replace('1730~1800', '17:30~19:00')
                                if '1200~1300' in cafe_menu[size][what]:
                                    cafe_menu[size][what] = cafe_menu[size][what].replace('1200~1300', '12:00~14:00')
                        elif cafeteria == '후생관':
                            if '11030' in cafe_menu[size][what]:
                                cafe_menu[size][what] = cafe_menu[size][what].replace('1030~1830', ' 10:30~18:30')
                        ##JunKiBeom fix the following code.
                        
                            if '1030' in cafe_menu[size][what]:
                                cafe_menu[size][what] = cafe_menu[size][what].replace('1030~소진시까지', ' 10:30~소진시까지')
                            if '1100' in cafe_menu[size][what]:
                                cafe_menu[size][what] = cafe_menu[size][what].replace('1100~1830', ' 11:00~18:30')
                            if '21030' in cafe_menu[size][what]:
                                cafe_menu[size][what] = cafe_menu[size][what].replace('1030~1830', ' 10:30~18:30')
                            if '1730' in cafe_menu[size][what]:
                                cafe_menu[size][what] = cafe_menu[size][what].replace('1730~1830', ' 17:30~18:30')
                        ##JunKiBeom fix the following code.
    
                    except:
                        print("haksik_pre 기숙사 식당 시간오류")

                    menu[count] = menu[count] + cafe_menu[size][what] + '\n\n'

            else:
                if cafeteria is not '어문관':
                    try:

                        menu[count] = menu[count] + cafe_menu[size][what] + '\n'
                    except:
                        pass
                for i in range(0,len(menu)):
                    if '중식(특식)' in menu[i]:
                        menu[i]=menu[i].replace('3,700', '7,400')
    if cafeteria == '어문관':
        umoon_temp = []
        umoon_select = ''
        umoon_size = int(len(menu))

        for i in range(0, umoon_size):

            if '일품' in menu[i]:
                continue
            else:
                menu[i] = menu[i].replace('\n', '')
                if '' == menu[i]:
                    continue
                elif '자장면' in menu[i]:
                    continue
                elif '\n' in menu[-1]:
                    menu[-1].replace('\n', '')
                else:
                    umoon_temp.append(menu[i])


        for i in range(int(len(umoon_temp)/2)):
            umoon_select += str(umoon_temp[2*i]) + '  ' + str(umoon_temp[2*i+1]) + '\n'
        try:
            if umoon_temp[-1] not in umoon_select:
                umoon_select += '\n' + umoon_temp[-1]
        except:
            pass
        umoon_select = menu[0] + umoon_select
        menu = [umoon_select]


    return menu

print(glo_crawl('기숙사 식당','today'))
