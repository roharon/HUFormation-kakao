from .rep import *
from .file_replace import *


if __name__=="__main__":

    make_json()
    while True:
        a = input("말 가르치기 : ")

        print(" 대답 : " + make_reply(a))

        """
    # 챗봇의 경우 make_reply(입력값)을 반환시켜야한다.


        """
