from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, LoginForm
from .models import User

def main_prelogin(request):
    return render(request, 'main_prelogin.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)  # 비밀번호 암호화
            user.save()
            messages.success(request, "회원가입이 완료되었습니다!")
            return redirect('users:login_view')
        else:
            messages.error(request, "회원가입 양식에 오류가 있습니다.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

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
    return render(request, 'login.html', {'form': form})

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
    return render(request, 'main.html', context)

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # 세션에서 사용자 ID 제거
        messages.success(request, "로그아웃되었습니다.")
    return redirect('users:main_prelogin')