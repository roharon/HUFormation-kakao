# HUFORMATION - KakaoTalk Plusfriend
![](https://img.shields.io/badge/License-MIT-blue.svg)![](https://img.shields.io/badge/Python-3.6-blue.svg)![](https://img.shields.io/pypi/djversions/djangorestframework.svg)



> 한국외국어대학교 식당메뉴 조회 플러스친구

[훕포메이션](http://pf.kakao.com/_xdERZxl)

## Environment

- Ubuntu 16.04
- PyCharm
- VirtualEnv
- Python 3.6.1
- Django 1.11.2

## Library

- beautifulsoup4
- Django
- lxml
- requests
- sqlite3

`requirements.txt`참고

> assets, hufscoops, hufscoops_project 폴더가 있는 디렉토리에 DB폴더 생성

> `./facebook_upload/upload.py` 와 `./haksik_upload.py` 는        
cron 작업을 통해 실행

    //서버실행
    python manage.py runserver IP:PORT
    
    //cron 작업실행
    0 0 * * * ./haksik_upload.py
    0 0 * * * ./facebook_upload/upload.py

---

# 미리보기

- 메인메뉴 화면

    ![](https://github.com/roharon/HUFormation-kakao/blob/master/preview/main_menu.jpg?raw=true)

- 도서관 기능

    ![](https://github.com/roharon/HUFormation-kakao/blob/master/preview/library_menu.jpg?raw=true)

- 학식메뉴 기능

    ![](https://github.com/roharon/HUFormation-kakao/blob/master/preview/cafeteria_menu.jpg?raw=true)
