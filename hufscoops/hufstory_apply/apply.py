from django.http import JsonResponse

def apply_hufstory():
    return JsonResponse({
            'message': {
                'text': '훕포메이션과 훕스토리가 합쳐집니다.\n5천명이 이용하는 학식서비스 훕포메이션과\n학생커뮤니티 훕스토리\n\n'
                    + '함께할 신입팀원을 모집합니다\n'
                    + '✔️모집 기간 2/26 ~ 3/8(금요일)\n'
                    + '✔️서류발표 3/9\n'
                    + '✔️면접기간 3/12 ~ 3/13\n'
                    + '✔️최종 팀원 발표 3/15\n'
                    + '자세한 사항은 http://recruit.hufstory.co.kr 에서 확인가능합니다\n\n'
                    + '새로운 IT서비스를 개발하고 싶은 분\n캠퍼스 행사 기획과 디자인을 담당해보고 싶은 분 환영합니다~!!'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학식', '내일의 학식', '시간별 학식', '이미지 학식', '도서관', '캠퍼스 변경', '훕포메이션과 함께할 팀원 모집 [~3/8]']
            }
        })