#-*- coding: utf-8 -*-
from selenium import webdriver
import facebook
import datetime
import os

project_path = "/home/roharon1998/HUFormation-kakao"

def make_image(imgtitle):
    driver = webdriver.PhantomJS(executable_path = project_path + '/facebook_upload/phantomjs-2.1.1/bin/phantomjs')
    driver.get('http://localhost:8001/seoul_menu')
    driver.save_screenshot(project_path + '/assets/img/' + 'seoul' + imgtitle+'.png')
    driver.quit()

    driver = webdriver.PhantomJS(executable_path = project_path + '/facebook_upload/phantomjs-2.1.1/bin/phantomjs')
    driver.get('http://localhost:8001/global_menu')
    driver.save_screenshot(project_path + '/assets/img/' + 'global' + imgtitle+'.png')
    driver.quit()
today = datetime.date.today()
imgtitle=today.strftime('%Y%m%d')

yesterday=today+datetime.timedelta(days=-1)
yesterday=yesterday.strftime('0%y%m%d')
try:
    os.remove(project_path + '/assets/img/'+'global'+yesterday+'.png')
    os.remove(project_path + '/assets/img/' + 'seoul' + yesterday + '.png')
except:
    pass


make_image(imgtitle)

graph = facebook.GraphAPI('EAADoZCgROJ5MBAEEQI32RNmjfCryFiJGq9RwrEJut0yZBKM5k08thQYwZC7EZCoqKEt4zZAFgw13VdzoosHUuZBUiHtH2tgaSbqjXl3XzhrUTARvCaikLU3z8VdgrY4Ju1xl0ZBMgO5IxNq8FduSq1lJjXJkyB5ru9CmCXxDqD5DQZDZD')

#graph.put_object("296489604149867", message='훕포메이션 연결테스트', link="http://roharon.github.io")


today_date = today.strftime('%m월 %d일')

graph.put_photo(image=open(project_path + '/assets/img/'+'seoul'+imgtitle+'.png', 'rb'), message='서울캠퍼스  ' + today_date + ' 점심 식단표입니다~')
graph.put_photo(image=open(project_path + '/assets/img/'+'global'+imgtitle+'.png', 'rb'), message='글로벌캠퍼스  ' + today_date + ' 점심 식단표입니다~')


print('완료')




