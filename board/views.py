from .models import Board
import random
from django.shortcuts import render, redirect
from .models import User
from django.shortcuts import get_object_or_404

# Create your views here.
def info(request, pk):
    board = Board.objects.get(id=pk)
    
    login_user = request.user     # 로그인한 유저 정보 받아옴
    
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

def ranking(request):
    rankers = User.objects.order_by('-score')[:3]
    
    ctx = {
        "rankers": rankers,
    }
    
    return render(request, "board/ranking.html", ctx)
    

def attack_game(request):
    random_numbers = random.sample(range(1, 11), 5)

    if request.user.is_authenticated:
        cards = list(random_numbers)
    else:
        cards = []
    
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else User.objects.all()

    return render(request, 'board/start_game.html', {
        'random_numbers': random_numbers, 
        'cards': cards, 
        'users': users
    })


######### attack전용view
def attack(request):
    if request.method == "POST":
        attacker = request.user
        print(type(attacker))
        defender_id = request.POST.get('defender')
        
        attack_number = int(request.POST.get('card'))


        Board.objects.create(
            howTowin = random.choice(('L', 'H')),
            attacker_id=attacker,
            attack_num=attack_number,
            defender_id=User.objects.get(id=defender_id),
            defend_num=None,
            status="진",  # 기본 상태는 진행중
            result = None
        )

        return redirect('board:game_list')  

    return redirect('board:attack_game')

# 게임 전적 페이지
from django.contrib.auth.decorators import login_required

def game_list(request):
    user = request.user
    games_as_attacker = Board.objects.filter(attacker_id=user)
    games_as_defender = Board.objects.filter(defender_id=user)

    context = {
        'games_as_attacker': games_as_attacker,
        'games_as_defender': games_as_defender,
    }

    return render(request, 'board/game_list.html', context)


# 반격하기 페이지
@login_required
def counter_attack(request, pk):
    game = get_object_or_404(Board, pk=pk)
    defender = request.user

    if request.method == "POST":

        game.defend_num = int(request.POST.get('card'))
        game.status = "종"  # 게임 상태를 종료로 설정

        # 게임 결과 계산
        if game.howTowin == "H":  # 높은 숫자가 승리
            if game.defend_num > game.attack_num:
                game.result = "D"
            elif game.defend_num < game.attack_num:
                game.result = "A"
            else:
                game.result = "무"  # 무승부경우 None? 수정 필요
        else:  # 낮은 숫자가 승리
            if game.defend_num < game.attack_num:
                game.result = "D"
            elif game.defend_num > game.attack_num:
                game.result = "A"
            else:
                game.result = "무"  # 무승부경우 None? 수정 필요

        game.save()
        return redirect('board:board_info', pk=game.pk)

    # 1부터 10까지의 숫자 중 5개를 랜덤으로 선택하여 카드 목록 생성
    random_numbers = random.sample(range(1, 11), 5)
    defender_cards = list(random_numbers)

    return render(request, 'board/counter_attack.html', {'game': game, 'defender_cards': defender_cards})


def delete(request, pk):
    if request.method == "POST":
        board = Board.objects.get(id=pk)
        board.delete()
        return redirect("board:game_list")     # 전적목록으로 돌아가기
        
    
    return redirect("board:game_list")