#!/home/roharon98/hufscoops/venv/lib/python3.5

import sqlite3
from hufscoops import haksik_pre

print(haksik_pre.seo_crawl('스카이 라운지'))

## 크론작업
#/home/roharon98/hufscoops/venv/bin/python3.5 /home/roharon98/develop/haksik_upload.py > /home/roharon98/develop/haksik_error.log 2>&1



con = sqlite3.connect("/home/roharon98/hufscoops/DB/haksik_data.db")
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

inmoon = haksik_pre.seo_crawl('인문관')
gyosoo = haksik_pre.seo_crawl('교수회관')
sky_lounge = haksik_pre.seo_crawl('스카이 라운지')

hooseng = haksik_pre.glo_crawl('후생관')
umoon = haksik_pre.glo_crawl('어문관')
dorm = haksik_pre.glo_crawl('기숙사 식당')
professor = haksik_pre.glo_crawl('교직원 식당')
gookje = haksik_pre.glo_crawl('국제사회교육원')

if '컵밥' in hooseng[1]:
    print('후생관_컵밥있음')
    #cur.execute("INSERT into 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", (hooseng[0], hooseng[1], hooseng[4]))
    cur.execute("INSERT into 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))
    cur.execute("INSERT into 후생관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', hooseng[2], ''))


cur.execute("INSERT into 어문관(breakfast, lunch, dinner) VALUES(?,?,?)", (umoon[0],umoon[0],umoon[0]))


if '조식(T/O)' in dorm[1]:
    if '중식(특식)' in dorm[3]:
        if '석식(일품)' in dorm[5]:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], dorm[5]))
        else:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[4]))
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], dorm[3], ''))
    else:
        if '석식(일품)' in dorm[4]:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', dorm[4]))
        else:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[1], '', ''))
else:
    if '중식(특식)' in dorm[2]:
        cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[3]))
        cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', dorm[2], dorm[4]))
    else:
        if '석식(일품)' in dorm[3]:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[2], dorm[3]))
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", ('', '', dorm[4]))
        else:
            cur.execute("INSERT into 기숙사(breakfast, lunch, dinner) VALUES(?,?,?)", (dorm[0], dorm[1], dorm[2]))

cur.execute("INSERT into 교직원(breakfast, lunch, dinner) VALUES(?,?,?)", ('',professor[0], professor[1]))

cur.execute("INSERT into 국제사회교육원(breakfast, lunch, dinner) VALUES(?,?,?)", (gookje[0],gookje[1],gookje[2]))

cur.execute("INSERT into 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", (inmoon[0], inmoon[1], inmoon[4]))
cur.execute("INSERT into 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[2], ''))
cur.execute("INSERT into 인문관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', inmoon[3], ''))

cur.execute("INSERT into 교수회관(breakfast, lunch, dinner) VALUES(?,?,?)", ('', gyosoo[0], gyosoo[1]))

cur.execute("INSERT into 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[0], ''))
cur.execute("INSERT into 스카이라운지(breakfast, lunch, dinner) VALUES(?,?,?)", ('', sky_lounge[1], ''))
#cur.execute("INSERT into 후생관(breakfast) VALUES(?)", (hooseng[0]))

con.commit()
con.close()
