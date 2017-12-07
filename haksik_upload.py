#!/home/roharon98/hufscoops/venv/lib/python3.5

import sqlite3
import datetime
import os
from hufscoops import haksik_pre

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
DB_DIR = os.path.join(HOME_DIR,"DB")
DB_NAME = "haksik_data.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)
DB_NAME_TOMORROW = "tomorrow_haksik_data.db"
DB_PATH_TOMORROW = os.path.join(DB_DIR, DB_NAME_TOMORROW)


if not os.path.isdir(DB_DIR):
    os.mkdir(DB_DIR)

def db_crontab():
    t = ['월', '화', '수', '목', '금', '토', '일']
    r = datetime.datetime.today().weekday()
    days = t[r]

    print(haksik_pre.glo_crawl('교직원 식당', 'today'))
    ## 크론작업
    # 0,52 0 * * * /home/roharon98/hufscoops/venv/bin/python3.5 /home/roharon98/hufscoops/haksik_upload.py > /home/roharon98/hufscoops/haksik_crontab_error.log 2>&1

    con = sqlite3.connect(DB_PATH)
    #con=sqlite3.connect("./DB/haksik_data.db")
    ###con = sqlite3.connect("/home/roharon98/develop/DB/haksik_data.db")

    try:
        inmoon = haksik_pre.seo_crawl('인문관', 'today')
        gyosoo = haksik_pre.seo_crawl('교수회관', 'today')
        sky_lounge = haksik_pre.seo_crawl('스카이 라운지', 'today')

        hooseng = haksik_pre.glo_crawl('후생관', 'today')
        umoon = haksik_pre.glo_crawl('어문관', 'today')
        dorm = haksik_pre.glo_crawl('기숙사 식당', 'today')
        professor = haksik_pre.glo_crawl('교직원 식당', 'today')
        gookje = haksik_pre.glo_crawl('국제사회교육원', 'today')
    except:
        print("연결오류")
        return 0

    cur = con.cursor()
    try:
        cur.execute("DELETE FROM 후생관")
        cur.execute("DELETE FROM 어문관")
        cur.execute("DELETE FROM 기숙사")
        cur.execute("DELETE FROM 교직원")
        cur.execute("DELETE FROM 국제사회교육원")

        cur.execute("DELETE FROM 인문관")
        cur.execute("DELETE FROM 교수회관")
        cur.execute("DELETE FROM 스카이라운지")
    except:
        pass

    try:
        ## 각 카페테리아별 테이블을 만들어 아침점심저녁 콜럼을 넣자
        # 어문관 경우에 예외처리.
        cur.execute("CREATE TABLE 후생관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 어문관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 기숙사(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 교직원(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 국제사회교육원(breakfast TEXT, lunch TEXT, dinner TEXT);")

        cur.execute("CREATE TABLE 인문관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 교수회관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 스카이라운지(breakfast TEXT, lunch TEXT, dinner TEXT);")


    except:
        print("@@예외")
        pass
    print(haksik_pre.seo_crawl('인문관', 'today'))

    if '조식' in hooseng[0]:
        if '컵밥' in hooseng[1]:
            if '한식' in hooseng[2]:
                if '일품' in hooseng[3]:
                    try:
                        if '석식' in hooseng[4]:
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                        (hooseng[0], hooseng[1], hooseng[4]))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[3], ''))
                        else:
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                        (hooseng[0], hooseng[1], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[3], ''))
                    except:
                        print('석식 없음 오류')
                else:
                    cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                (hooseng[0], hooseng[1], ''))
                    if '석식' in hooseng[3]:
                        cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                    ('', hooseng[2], hooseng[3]))
        else:
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", (hooseng[0], hooseng[1], hooseng[3]))
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
    else:
        if '일품' in hooseng[0]:
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[0], ''))

            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", (hooseng[0], hooseng[1], hooseng[4]))

    cur.execute("INSERT INTO 어문관(breakfast, lunch, dinner) VALUES(?,?,?)", (umoon[0], umoon[0], umoon[0]))

    if '조식(T/O)' in dorm[1]:
        if '중식(특식)' in dorm[3]:
            if '석식(일품)' in dorm[5]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], dorm[5]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], ''))
        else:
            if '석식(일품)' in dorm[4]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', dorm[4]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', ''))
    else:
        if '중식(특식)' in dorm[2]:
            cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[3]))
            cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', dorm[2], dorm[4]))
        else:
            if '석식(일품)' in dorm[3]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', dorm[4]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[2]))

    cur.execute("INSERT INTO 교직원(breakfast, lunch, dinner) VALUES(?,?,?)", ('', professor[0], professor[1]))

    cur.execute("INSERT INTO 국제사회교육원(breakfast, lunch, dinner) VALUES(?,?,?)", (gookje[0], gookje[1], gookje[2]))

    if days in ['토', '일']:
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", (inmoon[0], inmoon[0], ''))
        cur.execute("INSERT INTO 교수회관(breakfast, lunch, dinner) VALUES(?,?,?)", (' ', ' ', ' '))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', ''))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', ''))
    else:
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", (inmoon[0], inmoon[1], inmoon[4]))
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[2], ''))
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[3], ''))
        cur.execute("INSERT INTO 교수회관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', gyosoo[0], gyosoo[1]))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[0], ''))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[1], ''))



    # cur.execute("INSERT into 후생관(breakfast) VALUES(?)", (hooseng[0]))

    con.commit()
    con.close()

def tomorrow_db_crontab():
    t = ['월', '화', '수', '목', '금', '토', '일']
    r = datetime.datetime.today().weekday()
    days = t[r]

    print(haksik_pre.glo_crawl('교직원 식당', 'tomorrow'))
    ## 크론작업
    # 0,52 0 * * * /home/roharon98/hufscoops/venv/bin/python3.5 /home/roharon98/hufscoops/haksik_upload.py > /home/roharon98/hufscoops/haksik_crontab_error.log 2>&1

    con = sqlite3.connect(DB_PATH_TOMORROW)
    #con=sqlite3.connect("./DB/tomorrow_haksik_data.db")
    ###con = sqlite3.connect("/home/roharon98/develop/DB/haksik_data.db")

    cur = con.cursor()
    try:
        cur.execute("DELETE FROM 후생관")
        cur.execute("DELETE FROM 어문관")
        cur.execute("DELETE FROM 기숙사")
        cur.execute("DELETE FROM 교직원")
        cur.execute("DELETE FROM 국제사회교육원")

        cur.execute("DELETE FROM 인문관")
        cur.execute("DELETE FROM 교수회관")
        cur.execute("DELETE FROM 스카이라운지")
    except:
        pass

    try:
        ## 각 카페테리아별 테이블을 만들어 아침점심저녁 콜럼을 넣자
        # 어문관 경우에 예외처리.
        cur.execute("CREATE TABLE 후생관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 어문관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 기숙사(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 교직원(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 국제사회교육원(breakfast TEXT, lunch TEXT, dinner TEXT);")

        cur.execute("CREATE TABLE 인문관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 교수회관(breakfast TEXT, lunch TEXT, dinner TEXT);")
        cur.execute("CREATE TABLE 스카이라운지(breakfast TEXT, lunch TEXT, dinner TEXT);")


    except:
        print("@@예외")
        pass
    print(haksik_pre.seo_crawl('인문관', 'tomorrow'))
    inmoon = haksik_pre.seo_crawl('인문관', 'tomorrow')
    gyosoo = haksik_pre.seo_crawl('교수회관', 'tomorrow')
    sky_lounge = haksik_pre.seo_crawl('스카이 라운지', 'tomorrow')

    hooseng = haksik_pre.glo_crawl('후생관', 'tomorrow')
    umoon = haksik_pre.glo_crawl('어문관', 'tomorrow')
    dorm = haksik_pre.glo_crawl('기숙사 식당', 'tomorrow')
    professor = haksik_pre.glo_crawl('교직원 식당', 'tomorrow')
    gookje = haksik_pre.glo_crawl('국제사회교육원', 'tomorrow')

    if '조식' in hooseng[0]:
        if '컵밥' in hooseng[1]:
            if '한식' in hooseng[2]:
                if '일품' in hooseng[3]:
                    try:
                        if '석식' in hooseng[4]:
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                        (hooseng[0], hooseng[1], hooseng[4]))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[3], ''))
                        else:
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                        (hooseng[0], hooseng[1], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
                            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[3], ''))
                    except:
                        print('석식 없음 오류')
                else:
                    cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                (hooseng[0], hooseng[1], ''))
                    if '석식' in hooseng[3]:
                        cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)",
                                    ('', hooseng[2], hooseng[3]))
        else:
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", (hooseng[0], hooseng[1], hooseng[3]))
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
    else:
        if '일품' in hooseng[0]:
            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[0], ''))

            cur.execute("INSERT INTO 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", (hooseng[0], hooseng[1], hooseng[4]))

    cur.execute("INSERT INTO 어문관(breakfast, lunch, dinner) VALUES(?,?,?)", (umoon[0], umoon[0], umoon[0]))

    if '조식(T/O)' in dorm[1]:
        if '중식(특식)' in dorm[3]:
            if '석식(일품)' in dorm[5]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], dorm[5]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], ''))
        else:
            if '석식(일품)' in dorm[4]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', dorm[4]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', ''))
    else:
        if '중식(특식)' in dorm[2]:
            cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[3]))
            cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', dorm[2], dorm[4]))
        else:
            if '석식(일품)' in dorm[3]:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', dorm[4]))
            else:
                cur.execute("INSERT INTO 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[2]))

    cur.execute("INSERT INTO 교직원(breakfast, lunch, dinner) VALUES(?,?,?)", ('', professor[0], professor[1]))

    cur.execute("INSERT INTO 국제사회교육원(breakfast, lunch, dinner) VALUES(?,?,?)", (gookje[0], gookje[1], gookje[2]))

    if days in ['금', '토']:
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", (inmoon[0], inmoon[0], ''))
        cur.execute("INSERT INTO 교수회관(breakfast, lunch, dinner) VALUES(?,?,?)", (' ', ' ', ' '))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', ''))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', ''))
    else:
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", (inmoon[0], inmoon[1], inmoon[4]))
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[2], ''))
        cur.execute("INSERT INTO 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[3], ''))
        cur.execute("INSERT INTO 교수회관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', gyosoo[0], gyosoo[1]))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[0], ''))
        cur.execute("INSERT INTO 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[1], ''))



    # cur.execute("INSERT into 후생관(breakfast) VALUES(?)", (hooseng[0]))

    con.commit()
    con.close()


db_crontab()
tomorrow_db_crontab()
