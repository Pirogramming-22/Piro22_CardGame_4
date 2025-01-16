from django.shortcuts import render
from .models import Board
from .models import User

# Create your views here.
def info(request, pk):
    board = Board.objects.get(id=pk)
    
    #### TODO: 이 아래 pseudo_code 구현
    login_user = User.objects.get(id=login_user_id)     # 로그인한 유저 정보 받아옴
    
    # 결과 계산
    result = ""
    if login_user.id == board.attacker_id:
        # 유저가 공격자일 때
        if board.result == "A":
            result = "승리"
        else:
            result = "패배"
    else:
        # 유저가 방어자일 때
        if board.result == "A":
            result = "패배"
        else:
            result = "승리"
    
    ctx = {
        'board': board,
        'login_user': login_user,
        'result': result,
    }
    
    return render(request, 'board/info.html', ctx)
    
    