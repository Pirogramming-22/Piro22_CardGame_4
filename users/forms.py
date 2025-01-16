from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'nickname', 'login_type', ] 
        widgets = {
            'password': forms.PasswordInput(),  # 비밀번호 입력 필드
        }

    def clean_id(self):
        user_id = self.cleaned_data.get('id')
        if User.objects.filter(id=user_id).exists():
            raise forms.ValidationError("이미 사용 중인 ID입니다.")
        return user_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email


class LoginForm(forms.Form):
    id = forms.CharField(max_length=50, label="ID")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

