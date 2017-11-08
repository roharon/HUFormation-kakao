HUFormation
-----------
>MIT라이선스 하에 사용가능합니다.

> 카카오톡 [@훕포메이션](http://pf.kakao.com/_xdERZxl) 을 통해서 확인할 수 있습니다.
> 문의 roharon@hufs.ac.kr

<html>
<p>

<br>
  <h2>개발 환경</h2>
    <ul>
    <li>Ubuntu 16.04</li>
    <li>PyCharm</li>
  <li>VirtualEnv</li>
    <li>Python 3.6.1</li>
    <li>Django 1.11.2</li>
    </ul>
    
</p>
<p>
<h2>사용된 모듈
</h2>
<ul>
<li>beautifulsoup4</li>
<li>Django</li>
<li>lxml</li>
<li>requests</li>
<li>sqlite3 (Django에 내장</li>
</ul>
자세한 부분은 requirements.txt 참조

</p>

#사용법
> assets, hufscoops, hufscoops_project 폴더가 있는 디렉토리에 DB폴더 생성해야합니다
> ./facebook_upload/upload.py 와 ./haksik_upload.py 는 cron 작업을 통해 실행합니다 
<pre>code>
cron 작업실행
0 0 * * * ./haksik_upload.py
0 0 * * * ./facebook_upload/upload.py
</code></pre>
 <pre><code>
python manage.py migrate    //DB 마이그레이션

python manage.py runserver [server_address]:[PORT]    //서버 실행
</code></pre>
    
    
</html>
