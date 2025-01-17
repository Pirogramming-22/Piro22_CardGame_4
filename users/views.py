from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import UserRegistrationForm, LoginForm
from .models import User
from django.contrib.auth import login
from django.conf import settings
import requests

def main_prelogin(request):
    return render(request, 'start_page/before_login.html')

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
                    login(request, user)
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

def generate_unique_nickname(base_nickname):
    unique_nickname = base_nickname
    counter = 1

    # 닉네임이 중복될 경우, 고유한 닉네임을 생성
    while User.objects.filter(nickname=unique_nickname).exists():
        unique_nickname = f"{base_nickname}_{counter}"
        counter += 1

    return unique_nickname


def logout_view(request):
    # 카카오 로그아웃 처리
    if 'kakao_access_token' in request.session:
        kakao_logout(request)

    # 네이버 로그아웃 처리
    if 'naver_access_token' in request.session:
        print("네이버 로그아웃 진입")
        naver_logout(request)  # 네이버 토큰 삭제
        return redirect('users:main_prelogin')  # 로그인 전 메인 페이지로 이동

    # Google 로그아웃 처리
    if 'google_access_token' in request.session:
        return google_logout(request)

    # 일반 로그아웃 처리 (Django 세션 초기화)
    request.session.flush()

    messages.success(request, "로그아웃되었습니다.")
    return redirect('users:main_prelogin')

def google_logout(request):
    # Google 세션 관련 정보 제거
    if 'google_access_token' in request.session:
        access_token = request.session['google_access_token']
        revoke_url = f"https://oauth2.googleapis.com/revoke?token={access_token}"

        # 토큰 취소 요청
        requests.post(revoke_url)

        # 세션에서 Google 관련 정보 삭제
        del request.session['google_access_token']

    # 일반 로그아웃 처리
    request.session.flush()

    # Google 로그아웃 페이지로 리디렉션
    messages.success(request, "Google에서 로그아웃되었습니다.")
    return redirect('users:main_prelogin')

def kakao_logout(request):
    kakao_access_token = request.session.get('kakao_access_token')
    if kakao_access_token:
        unlink_url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {
            "Authorization": f"Bearer {kakao_access_token}"
        }
        response = requests.post(unlink_url, headers=headers)

        if response.status_code == 200:
            messages.success(request, "카카오 로그아웃이 완료되었습니다.")
        else:
            messages.error(request, "카카오 로그아웃 중 문제가 발생했습니다.")

        del request.session['kakao_access_token']

def naver_logout(request):
    # 네이버 토큰 삭제 URL
    if 'naver_access_token' in request.session:
        access_token = request.session['naver_access_token']
        revoke_url = "https://nid.naver.com/oauth2.0/token"
        revoke_data = {
            'grant_type': 'delete',
            'client_id': settings.NAVER_CLIENT_ID,  # 환경 변수에서 가져옴
            'client_secret': settings.NAVER_CLIENT_SECRET,  # 환경 변수에서 가져옴
            'access_token': access_token,
            'service_provider': 'NAVER',
        }

        # 네이버 토큰 삭제 요청
        response = requests.post(revoke_url, data=revoke_data)
        response_json = response.json()

        # 토큰 삭제 성공 여부 확인
        if response_json.get('result') == 'success':
            del request.session['naver_access_token']  # 세션에서 액세스 토큰 삭제
            request.session.flush()  # Django 세션 초기화
            messages.success(request, "네이버에서 로그아웃되었습니다.")
        else:
            messages.error(request, "네이버 로그아웃 중 오류가 발생했습니다.")
    else:
        messages.error(request, "네이버 로그아웃 토큰이 없습니다.")

# 카카오 로그인
def kakao_login(request):
    kakao_auth_url = (
        "https://kauth.kakao.com/oauth/authorize?"
        f"client_id={settings.KAKAO_CLIENT_ID}&"
        f"redirect_uri={settings.KAKAO_REDIRECT_URI}&"
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
        'client_id': settings.KAKAO_CLIENT_ID,  # settings에서 가져온 값 사용
        'redirect_uri': settings.KAKAO_REDIRECT_URI,
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

    return redirect('users:login_view')

# 네이버 로그인
def naver_login(request):
    naver_auth_url = (
        "https://nid.naver.com/oauth2.0/authorize?"
        f"client_id={settings.NAVER_CLIENT_ID}&"
        f"redirect_uri={settings.NAVER_REDIRECT_URI}&"
        "response_type=code"
    )
    return redirect(naver_auth_url)

def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code:
        return JsonResponse({'error': '인증 코드가 없습니다.'}, status=400)

    # 네이버 토큰 요청 URL
    token_url = "https://nid.naver.com/oauth2.0/token"

    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_CLIENT_SECRET,
        'redirect_uri': settings.NAVER_REDIRECT_URI,
        'code': code,
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Access Token 요청 실패'}, status=400)

    # 사용자 정보 요청
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info_json = user_info_response.json()

    naver_id = user_info_json.get('response', {}).get('id')
    naver_name = user_info_json.get('response', {}).get('name')
    unique_nickname = generate_unique_nickname(naver_name)

    if not naver_id:
        messages.error(request, "네이버 사용자 정보를 가져오는 데 실패했습니다.")
        return redirect('users:main_prelogin')

    # 사용자 저장 또는 업데이트
    user, created = User.objects.update_or_create(
        id=f"n{naver_id}",
        defaults={
            'nickname': unique_nickname,
            'login_type': 'naver',
        },
    )

    # 세션에 사용자 ID 및 액세스 토큰 저장
    request.session['user_id'] = user.id
    request.session['naver_access_token'] = access_token  # 액세스 토큰 저장

    return redirect('users:login_view')

def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

    # 항상 계정 선택 화면이 나타나도록 `prompt=select_account` 추가
    url = (
        f"{google_auth_url}?"
        f"response_type=code&"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"scope={scope}&"
        "prompt=select_account"
    )
    return redirect(url)

def google_callback(request):
    code = request.GET.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    if not code:
        return JsonResponse({'error': '인증 코드가 없습니다.'}, status=400)

    # Access Token 요청
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,  # 환경 변수에서 값 가져오기
        'client_secret': settings.GOOGLE_CLIENT_SECRET,  # 환경 변수에서 값 가져오기
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Access Token 요청 실패'}, status=400)

    # 사용자 정보 가져오기
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Google API 응답에서 필요한 정보 추출
    google_id = user_info.get('id')  # Google 고유 사용자 ID
    name = user_info.get('name')
    email = user_info.get('email')  # 세션에 저장하거나 로그에 사용할 수 있음
    g_id = f"g{google_id}"

    # 사용자 생성 또는 로그인 처리
    user, created = User.objects.get_or_create(
        id=g_id,
        defaults={
            'nickname': generate_unique_nickname(name),
            'login_type': 'google',
        },
    )

    # 세션에 사용자 정보 저장
    request.session['user_id'] = user.id
    request.session['google_email'] = email  # 이메일은 세션에 저장
    messages.success(request, f"{user.nickname}님, 환영합니다!")
    return redirect('users:login_view')
