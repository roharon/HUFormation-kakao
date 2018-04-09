#!/home/roharon98/hufscoops/venv/lib/python3.5

import sqlite3
import datetime
import os, sys
from hufscoops import haksik_pre
import temp_sikdan
HOME_DIR = os.path.dirname(os.path.realpath(__file__))
DB_DIR = os.path.join(HOME_DIR,"DB")
DB_NAME = "haksik_data.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)
DB_NAME_TOMORROW = "tomorrow_haksik_data.db"
DB_PATH_TOMORROW = os.path.join(DB_DIR, DB_NAME_TOMORROW)


if not os.path.isdir(DB_DIR):
    os.mkdir(DB_DIR)

table_names = ("후생관","어문관","기숙사","교직원","국제사회교육원","인문관","교수회관","스카이라운지")
day_kr = ('월', '화', '수', '목', '금', '토', '일')

def db_init(db_cursor):
    print(" > DB init ...")
    try:
        query_delete = ("DROP TABLE IF EXISTS {};")
        query_create = ("CREATE TABLE {}(breakfast TEXT, lunch TEXT, dinner TEXT);")
        for tname in table_names:
            db_cursor.execute(query_delete.format(tname))
            db_cursor.execute(query_create.format(tname))
    except:
        print("Database create error.", file=sys.stderr)
        raise

def crawl(day):
    print(" > Crawling ...")
    assert(day in ('today', 'tomorrow'))
    print("   > seo crawling ...")
    inmoon = haksik_pre.seo_crawl('인문관', day)
    gyosoo = haksik_pre.seo_crawl('교수회관', day)
    sky_lounge = haksik_pre.seo_crawl('스카이 라운지', day)
    print("   > glo crawling ...")
    hooseng = haksik_pre.glo_crawl('후생관', day)
    print(hooseng)
    umoon = haksik_pre.glo_crawl('어문관', day)
    dorm = haksik_pre.glo_crawl('기숙사 식당', day)
    professor = haksik_pre.glo_crawl('교직원 식당', day)
    gookje = haksik_pre.glo_crawl('국제사회교육원', day)
    return (inmoon,gyosoo,sky_lounge,hooseng,umoon,dorm,professor,gookje)

def insert_menu(cur, cafe, menu):
    query_insert = "INSERT INTO {}(breakfast, lunch, dinner) VALUES(?,?,?)"
    cur.execute(query_insert.format(cafe), menu)

def db_insert(inmoon,gyosoo,sky_lounge,hooseng,umoon,dorm,professor,gookje,cur=None,day=None,days=None):
    print(" > DB inserting ...")
    query_insert = "INSERT INTO {}(breakfast, lunch, dinner) VALUES(?,?,?)"
    if '조식' in hooseng[0]:
        if '컵밥' in hooseng[1]:
            if '한식' in hooseng[2]:
                if '일품' in hooseng[3]:
                    try:
                        insert_menu(cur, "후생관", (hooseng[0], hooseng[1],
                                        hooseng[4] if '석식' in hooseng[4] else ''))
                        insert_menu(cur, "후생관", ('', hooseng[2], ''))
                        insert_menu(cur, "후생관", ('', hooseng[3], ''))
                    except:
                        print('석식 없음 오류')
                else:
                    insert_menu(cur, "후생관", (hooseng[0], hooseng[1], ''))
                    if '석식' in hooseng[3]:
                        insert_menu(cur, "후생관", ('', hooseng[2], hooseng[3]))
        else:
            insert_menu(cur, "후생관", (hooseng[0], hooseng[1], hooseng[3]))
            insert_menu(cur, "후생관", ('', hooseng[2], ''))
    elif '일품' in hooseng[0]:
        insert_menu(cur, "후생관", ('', hooseng[0], ''))
        insert_menu(cur, "후생관", (hooseng[0], hooseng[1], hooseng[4]))
    elif '뚝배기' in hooseng[0]:
        insert_menu(cur,"후생관", ('',hooseng[0],hooseng[0]))
        insert_menu(cur,"후생관",('',hooseng[1],hooseng[1]))
        if len(hooseng)>2:
            if '일품1' in hooseng[1]:
                insert_menu(cur, "후생관", ('',hooseng[2],hooseng[2]))
                insert_menu(cur, "후생관", ('', hooseng[3] if '일품' in hooseng[3] else '', hooseng[3] if ('석식' or '일품') in hooseng[3] else ''))
                #fix it. 20180327-11pm


    elif '탕류' in hooseng[0]:
        if '뚝배기' in hooseng[1]:
            if '일품1' in hooseng[2]:
                    if '일품2' in hooseng[3]:
                        #일품2 있고
                        insert_menu(cur, "후생관", ('', hooseng[0], hooseng[0]))
                        insert_menu(cur, "후생관", ('', hooseng[1], hooseng[1]))
                        insert_menu(cur, "후생관", ('', hooseng[2], hooseng[2]))
                        insert_menu(cur, "후생관", ('', hooseng[3], hooseng[3]))
                        try:
                            insert_menu(cur,"후생관",('','',hooseng[4] if '석식' in hooseng[4] else ''))
                        except:
                            pass

                    else:
                        # 일품2없고 석식없고
                        insert_menu(cur, "후생관", ('', hooseng[0], hooseng[0]))
                        insert_menu(cur, "후생관", ('', hooseng[1], hooseng[1]))
                        insert_menu(cur, "후생관", ('', hooseng[2], hooseng[2]))
                        insert_menu(cur,"후생관",('','',hooseng[3] if '석식' in hooseng[3] else ''))



    insert_menu(cur, "어문관", (umoon[0], umoon[0], umoon[0]))

    if '조식(T/O)' in dorm[1]:
        if '중식(특식)' in dorm[3]:
            if '스넥' in dorm[4]:
                if '석식' in dorm[5]:
                    try:
                        insert_menu(cur, "기숙사", (dorm[0], dorm[2], dorm[5]))
                        insert_menu(cur, "기숙사", (dorm[1], dorm[3],''))
                        insert_menu(cur, "기숙사", ('', dorm[4], ''))
                    except:
                        insert_menu(cur, "기숙사", ('기숙사식단 오류', '기숙사 식단 오류', '기숙사식단 오류'))
                else:
                    try:
                        insert_menu(cur, "기숙사", (dorm[0], dorm[2], ''))
                        insert_menu(cur, "기숙사", (dorm[1], dorm[3], ''))
                        insert_menu(cur, "기숙사", ('', dorm[4], ''))
                    except:
                        insert_menu(cur, "기숙사", ('기숙사식단 오류', '기숙사 식단 오류', '기숙사식단 오류'))


            else:
                insert_menu(cur, "기숙사", (dorm[0], dorm[2], dorm[4]))
                insert_menu(cur, "기숙사", (dorm[1], dorm[3], dorm[5] if '석식' in dorm[5] else ''))
        else:
            insert_menu(cur, "기숙사", (dorm[0], dorm[2], dorm[3]))
            insert_menu(cur, "기숙사", (dorm[1], '', dorm[4] if '석식(일품)' in dorm[4] else ''))
    else:
        if '중식(특식)' in dorm[2]:
            insert_menu(cur, "기숙사", (dorm[0], dorm[1], dorm[3]))
            insert_menu(cur, "기숙사", ('', dorm[2], dorm[4]))
        else:
            if '석식(일품)' in dorm[3]:
                insert_menu(cur, "기숙사", (dorm[0], dorm[2], dorm[3]))
                insert_menu(cur, "기숙사", ('', '', dorm[4]))
            else:
                insert_menu(cur, "기숙사", (dorm[0], dorm[1], dorm[2]))

    insert_menu(cur, "교직원", ('', professor[0], professor[1]))
    insert_menu(cur, "국제사회교육원", (gookje[0], gookje[1], gookje[2]))


    if (day == 'today' and days in ['토', '일']) or \
            (day == 'tomorrow' and days in ['금', '토']):
        insert_menu(cur, "인문관", (inmoon[0], inmoon[0], ''))
        insert_menu(cur, "교수회관", (' ', ' ', ' '))
        insert_menu(cur, "스카이라운지", ('', '', ''))
        insert_menu(cur, "스카이라운지", ('', '', ''))
    else:
        insert_menu(cur, "인문관", (inmoon[0], inmoon[1], inmoon[4]))
        insert_menu(cur, "인문관", ('', inmoon[2], ''))
        insert_menu(cur, "인문관", ('', inmoon[3], ''))
        insert_menu(cur, "교수회관", ('', gyosoo[0], gyosoo[1]))
        insert_menu(cur, "스카이라운지", ('', sky_lounge[0], ''))
        insert_menu(cur, "스카이라운지", ('', sky_lounge[1], ''))



def db_crontab():
    days = day_kr[datetime.datetime.today().weekday()]




    for db_path, day in ((DB_PATH, 'today'), (DB_PATH_TOMORROW, 'tomorrow')):
        try:
            data = crawl(day)
        except:
            print("Crawling connection error.", file=sys.stderr)
            raise
        con= sqlite3.connect(db_path)
        cur = con.cursor()
        db_init(cur)
        check_date = datetime.datetime.now().strftime('%m%d') # new

        inmoon, gyosoo, sky_lounge, hooseng, umoon, dorm, professor, gookje = data

        if int(check_date) >= int('0409') and int(check_date) <= int('0413'):
            hooseng=temp_sikdan.hooseng_temp(check_date)
        else:
            pass

        db_insert(inmoon, gyosoo, sky_lounge, hooseng, umoon, dorm, professor, gookje, cur, day, days=days)


        con.commit()
        con.close()


db_crontab()



## Database binary checksum
#
# MD5 (DB/haksik_data.db)          = 7f49a064166e312860afd45573c6836f
# MD5 (DB/tomorrow_haksik_data.db) = fb235b93ca605543ac83cbee4bf82d9c
#
