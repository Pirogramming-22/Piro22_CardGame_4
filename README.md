# 🔥🔥4조 카드게임🔥🔥
<br>

## 팀 멤버⭐️
◽김규일<br>
◽김은성<br>
◽김태린<br>
◽박수연<br>
◽박태희<br>
=======
# **Piro22_CardGame_4**


## 파트


 **김태린** 

- base(header-footer)
- 회원가입


**박수연**

- 로그인 전 main
- 로그인 후 main


**김규일**

- 로그인


**박태희**

- 공격하기 페이지 - 반격하기 페이지
- 게임 전적 페이지


**김은성**

- 게임 정보 페이지
- 랭킹 페이지

## 🚀  Stacks


**HTML**

**CSS**

**JavaScript**

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHLN0RrPTmNUSMhl6MTeX0p_uIIj6Qzoxok9gjmzjELFRCeJaN34K8nOSaG56rrrw-evQ&usqp=CAU" alt="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHLN0RrPTmNUSMhl6MTeX0p_uIIj6Qzoxok9gjmzjELFRCeJaN34K8nOSaG56rrrw-evQ&usqp=CAU" width="40px" /> **Python**

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHLN0RrPTmNUSMhl6MTeX0p_uIIj6Qzoxok9gjmzjELFRCeJaN34K8nOSaG56rrrw-evQ&usqp=CAU" alt="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHLN0RrPTmNUSMhl6MTeX0p_uIIj6Qzoxok9gjmzjELFRCeJaN34K8nOSaG56rrrw-evQ&usqp=CAU" width="40px" /> **Django**


**sqlite**


## 🛠  Tools

---

<img src="https://cdn-icons-png.flaticon.com/512/5968/5968705.png" alt="https://cdn-icons-png.flaticon.com/512/5968/5968705.png" width="40px" /> **Figma**


<img src="https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png" alt="https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png" width="40px" /> **Git**


## 👥  Collaboration

---

<img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40px" /> [**GitHub**](https://github.com/Pirogramming-22/Piro22_CardGame_4)


<img src="https://cdn.icon-icons.com/icons2/2389/PNG/512/notion_logo_icon_145025.png" alt="https://cdn.icon-icons.com/icons2/2389/PNG/512/notion_logo_icon_145025.png" width="40px" /> [**Notion**](https://www.notion.so/Piro22_CardGame_4-17d9d162b06c80d8a4a5ff3b8b0ee699?pvs=21)


<img src="https://cdn-icons-png.flaticon.com/512/5968/5968756.png" alt="https://cdn-icons-png.flaticon.com/512/5968/5968756.png" width="40px" /> **Discord**

---
## env 파일 생성 설명

프로젝트의 루트 디렉토리에 .env 파일을 생성합니다.
(루트 디렉토리는 [manage.py](http://manage.py/) 파일이 있는 디렉토리입니다.)

아래 내용을 .env 파일에 추가합니다:

### Kakao API

KAKAO_CLIENT_ID=카카오_클라이언트_ID

KAKAO_CLIENT_SECRET=카카오_클라이언트_시크릿

KAKAO_REDIRECT_URI=http://127.0.0.1:8000/kakao/callback

### Naver API

NAVER_CLIENT_ID=네이버_클라이언트_ID

NAVER_CLIENT_SECRET=네이버_클라이언트_시크릿

NAVER_REDIRECT_URI=http://127.0.0.1:8000/naver/callback/

### Google API

GOOGLE_CLIENT_ID=구글_클라이언트_ID

GOOGLE_CLIENT_SECRET=구글_클라이언트_시크릿

GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/google/callback/

각 항목에 플랫폼에서 발급받은 실제 API 키와 시크릿 값을 입력합니다.

---

1. 가상환경을 활성화
2. requirements.txt 실행

```jsx
1. 가상환경 활성화

2. requirements.txt 실행
pip install -r requirements.txt

3. .env 파일 root 디렉터리에 추가

4. 마이그레이션 파일 생성
python manage.py makemigrations

5. 마이그레이션 파일 적용
python manage.py migrate

6. 서버 실행
python manage.py runserver
```

### 추가 참고 사항

---

.env 파일은 민감한 정보를 포함하고 있으므로 절대 깃허브에 업로드하지 않도록 합니다.

requirements.txt에 포함된 라이브러리는 프로젝트 실행에 필요한 최소한의 패키지로 구성되어 있습니다.

운영 환경에서는 환경 변수 관리 도구를 사용하여 .env 파일 대신 보안적으로 관리하는 것을 권장합니다.

>>>>>>> a0802bae424c7139d108b7f2edf35153cfd2e476
