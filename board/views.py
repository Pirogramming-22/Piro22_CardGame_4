import random
from django.shortcuts import render, redirect
from .models import Card, User, Attack


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
    return render(request, 'board/start_game.html', {'random_numbers': random_numbers, 'cards': cards, 'users': users})


def attack(request):
    if request.method == "POST":
        attacker = request.user
        defender_id = request.POST.get('defender')
        card_id = request.POST.get('card')

        defender = User.objects.get(id=defender_id)
        card = Card.objects.get(id=card_id)
        Attack.objects.create(attacker=attacker, defender=defender, card=card)
        return redirect('game_list')

    return redirect('attack_game')
