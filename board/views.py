from .models import Board
import random
from django.shortcuts import render, redirect
from .models import Card, User
from django.shortcuts import get_object_or_404

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

def ranking(request):
    rankers = User.objects.order_by('-score')[:3]
    
    ctx = {
        "rankers": rankers,
    }
    
    return render(request, "board/ranking.html", ctx)
    

def attack_game(request):
    random_numbers = random.sample(range(1, 11), 5)

    if request.user.is_authenticated:
        # 기존 카드 삭제, 새로운 카드 5개 생성
        Card.objects.filter(owner=request.user).delete()
        for num in random_numbers:
            Card.objects.create(number=num, owner=request.user)
        # 생성된 카드들을 DB에서 가져오기
        cards = Card.objects.filter(owner=request.user)
    else:
        cards = []
    
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else User.objects.all()

    return render(request, 'board/start_game.html', {
        'random_numbers': random_numbers, 
        'cards': cards, 
        'users': users
    })


def attack(request):
    if request.method == "POST":
        attacker = request.user
        defender_id = request.POST.get('defender')
        attacker_card_id = request.POST.get('attacker_card')  
        defender_card_id = request.POST.get('defender_card')


        defender = User.objects.get(id=defender_id)
        attacker_card = Card.objects.get(id=attacker_card_id)
        defender_card = Card.objects.get(id=defender_card_id) if defender_card_id else None


        Board.objects.create(
            attacker_id=attacker,
            defender_id=defender,
            attack_num=attacker_card.number,
            defend_num=defender_card.number if defender_card else None,
            attacker_card=attacker_card,
            defender_card=defender_card,
            status="진"  # 기본 상태는 진행중 
        )

        return redirect('game_list')  

    return redirect('attack_game')

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
        defender_card_id = request.POST.get('defender_card')
        defender_card = Card.objects.get(id=defender_card_id)

        game.defend_num = defender_card.number
        game.defender_card = defender_card
        game.status = "종"  # 게임 상태를 종료로 설정

        # 게임 결과 계산
        if game.howTowin == "H":  # 높은 숫자가 승리
            if game.defend_num > game.attack_num:
                game.result = "D"
            elif game.defend_num < game.attack_num:
                game.result = "A"
            else:
                game.result = None  # 무승부경우 None? 수정 필요
        else:  # 낮은 숫자가 승리
            if game.defend_num < game.attack_num:
                game.result = "D"
            elif game.defend_num > game.attack_num:
                game.result = "A"
            else:
                game.result = None  # 무승부경우 None? 수정 필요

        game.save()
        return redirect('board:board_info', pk=game.pk)

    # 1부터 10까지의 숫자 중 5개를 랜덤으로 선택하여 카드 목록 생성
    random_numbers = random.sample(range(1, 11), 5)
    defender_cards = [Card.objects.create(number=num, owner=defender) for num in random_numbers]

    return render(request, 'board/counter_attack.html', {'game': game, 'defender_cards': defender_cards})

