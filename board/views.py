from .models import Board
import random
from django.shortcuts import render, redirect
from .models import Card, User

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


        new_board = Board.objects.create(
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