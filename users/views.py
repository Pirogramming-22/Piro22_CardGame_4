from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import UserRegistrationForm, LoginForm
from .models import User
from django.contrib.auth import login
import requests

def main_prelogin(request):
    return render(request, 'user/main_prelogin.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            messages.success(request, "회원가입이 완료되었습니다!")  
            return redirect('users:login_view')  
    else:
        form = UserRegistrationForm()
    return render(request, 'user/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(id=user_id)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id 
                    return redirect('users:main_page')
                else:
                    messages.error(request, "비밀번호가 일치하지 않습니다.")
            except User.DoesNotExist:
                messages.error(request, "존재하지 않는 사용자입니다.")
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def main_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('users:login_view')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "사용자 정보를 가져올 수 없습니다.")
        return redirect('users:login_view')
    context = {
        'user': user
    }
    return render(request, 'user/main.html', context)


def logout_view(request):
    # 카카오 로그아웃 처리
    kakao_access_token = request.session.get('kakao_access_token')  # 세션에서 토큰 가져오기

    if kakao_access_token:
        # 카카오 연결 해제 API 호출
        unlink_url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {
            "Authorization": f"Bearer {kakao_access_token}"
        }
        response = requests.post(unlink_url, headers=headers)

        if response.status_code == 200:
            messages.success(request, "카카오 로그아웃이 완료되었습니다.")
        else:
            messages.error(request, "카카오 로그아웃 중 문제가 발생했습니다.")

        # 세션에서 카카오 토큰 삭제
        del request.session['kakao_access_token']

    # 세션에서 사용자 ID 삭제
    if 'user_id' in request.session:
        del request.session['user_id']

    messages.success(request, "로그아웃되었습니다.")
    return redirect('users:main_prelogin')



def kakao_login(request):
    kakao_auth_url = (
        "https://kauth.kakao.com/oauth/authorize?"
        "client_id=ebdda9bce68d2e8bb2fb42a35dd17fd6&"  # REST API 키를 넣으세요
        "redirect_uri=http://127.0.0.1:8000/kakao/callback&"
        "response_type=code"
    )
    return redirect(kakao_auth_url)

def kakao_callback(request):
    code = request.GET.get('code')  # 카카오에서 전달한 인증 코드
    if not code:
        return JsonResponse({'error': '인증 코드가 없습니다.'}, status=400)

    # 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': 'ebdda9bce68d2e8bb2fb42a35dd17fd6',  # REST API 키
        'redirect_uri': 'http://127.0.0.1:8000/kakao/callback',
        'code': code,
    }
    token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    if not access_token:
        return JsonResponse({'error': '액세스 토큰 요청 실패'}, status=400)

    # 기존 세션 데이터 덮어쓰기
    request.session['kakao_access_token'] = access_token

    # 사용자 정보 요청
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_info_headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=user_info_headers)
    user_info_json = user_info_response.json()

    kakao_id = user_info_json.get('id')
    kakao_nickname = user_info_json.get('properties', {}).get('nickname')

    # 고유한 닉네임 생성
    unique_nickname = generate_unique_nickname(kakao_nickname)

    # User 생성 또는 업데이트
    user, created = User.objects.update_or_create(
        id=f"k{kakao_id}",  # 카카오 ID에 'k' 접두사 추가
        defaults={
            'nickname': unique_nickname,  # 고유 닉네임 저장
            'login_type': 'kakao',
        },
    )
    request.session['user_id'] = user.id

    return redirect('users:main_page')


def generate_unique_nickname(base_nickname):
    unique_nickname = base_nickname
    counter = 1

    # 닉네임이 중복될 경우, 고유한 닉네임을 생성
    while User.objects.filter(nickname=unique_nickname).exists():
        unique_nickname = f"{base_nickname}_{counter}"
        counter += 1

    return unique_nickname

