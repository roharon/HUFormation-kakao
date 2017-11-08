from bs4 import BeautifulSoup
import datetime, requests
import random


def seo_crawl(cafeteria):
    today = datetime.date.today()
    today_d = today.strftime("%Y%m%d")
    today_w = today.strftime("%w")

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
        error = "\n학교 사이트 점검중!\n학식내용을 불러올 수 없습니다."
        return error

    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    my_titles = soup.select(
        'tr'
    )
    data = []
    cafe_menu = []

    emoti = '(허걱)', '(멘붕)', '(깜짝)', '(허걱)', '(부르르)', '(훌쩍)', '(우와)', '(심각)', '(헉)'
    for title in my_titles:
        data.append(title.text)

    for i in data:
        if len(data) == 1:
            cafe_menu.append(i)
            return "\n오늘은 학식이 없어요 " + random.choice(emoti)
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
        if today_w == "6":      # 0은 일요일 6은 토요일
            if cafeteria in '인문관':
                if size in [1, 3, 4]:
                    continue
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


def glo_crawl(cafeteria):
    today = datetime.date.today()
    today_d = today.strftime("%Y%m%d")

    try:
        if cafeteria == "후생관":
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=후생관+학생식당&caf_id=h203')
        elif cafeteria == "어문관":
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=어문관&caf_id=h204')
        elif cafeteria == "기숙사 식당":
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=HufsDorm+식당&caf_id=h205')
        elif cafeteria == "교직원 식당":
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=후생관+교직원식당&caf_id=h202')
        elif cafeteria == "국제사회교육원":
            req = requests.get(
                'https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/viewWeek.jsp?startDt=' + today_d + '&endDt=' + today_d + '&caf_name=국제사회교육원식당&caf_id=h201')
    except:
        error = "\n학교 사이트 점검중!\n학식내용을 불러올 수 없습니다."
        return error

    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    my_titles = soup.select(
        'tr'
    )
    data = []
    cafe_menu = []

    emoti = '(허걱)', '(멘붕)', '(깜짝)', '(허걱)', '(부르르)', '(훌쩍)', '(우와)', '(심각)', '(헉)'

    for title in my_titles:
        data.append(title.text)

    for i in data:
        if len(data) == 1:
            cafe_menu.append(i)
            return "\n오늘은 학식이 없어요 " + random.choice(emoti)
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

    return menu
