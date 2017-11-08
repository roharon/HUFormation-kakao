#-*- coding: utf-8 -*-
from selenium import webdriver
import facebook
import datetime
import os

def make_image(imgtitle):

    driver = webdriver.PhantomJS('/home/roharon98/hufscoops/facebook_upload/phantomjs-2.1.1/bin/phantomjs')
    driver.get('http://localhost:8001/seoul_menu')
    driver.save_screenshot('/home/roharon98/hufscoops/assets/img/' + 'seoul' + imgtitle+'.png')
    driver.quit()

    driver = webdriver.PhantomJS('/home/roharon98/hufscoops/facebook_upload/phantomjs-2.1.1/bin/phantomjs')
    driver.get('http://localhost:8001/global_menu')
    driver.save_screenshot('/home/roharon98/hufscoops/assets/img/' + 'global' + imgtitle+'.png')
    driver.quit()
today = datetime.date.today()
imgtitle=today.strftime('%Y%m%d')

yesterday=today+datetime.timedelta(days=-1)
yesterday=yesterday.strftime('0%y%m%d')
try:
    os.remove('/home/roharon98/hufscoops/assets/img/'+'global'+yesterday+'.png')
    os.remove('/home/roharon98/hufscoops/assets/img/' + 'seoul' + yesterday + '.png')
except:
    pass


make_image(imgtitle)

graph = facebook.GraphAPI('USER TOKEN HERE')

#graph.put_object("296489604149867", message='훕포메이션 연결테스트', link="http://roharon.github.io")


today_date = today.strftime('%m월 %d일')

graph.put_photo(image=open('/home/roharon98/hufscoops/assets/img/'+'seoul'+imgtitle+'.png', 'rb'), message='서울캠퍼스  ' + today_date + ' 점심 식단표입니다~')
graph.put_photo(image=open('/home/roharon98/hufscoops/assets/img/'+'global'+imgtitle+'.png', 'rb'), message='글로벌캠퍼스  ' + today_date + ' 점심 식단표입니다~')


print('완료')




