# Vincit - 담당자별 전날 문의현황 대시보드

구글 시트 데이터를 기반으로 한 부동산 담당자별 문의현황 대시보드입니다.

## 기능

- 구글 시트에서 실시간 데이터 연동
- 담당자별 전날 문의 수 표시
- 담당자별 매물 목록 및 문의 현황
- 매물별 조회수 정보
- 담당자 순위 및 통계

## 로컬 개발 환경 설정

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 구글 서비스 계정 설정

1. Google Cloud Console에서 프로젝트 생성
2. Google Sheets API 및 Google Drive API 활성화
3. 서비스 계정 생성 및 JSON 키 파일 다운로드
4. JSON 키 파일을 다음 경로에 저장:
   ```
   C:\Users\1\Desktop\구글서비스키\더탑원이스트 구글서비스키\thetopone-fe6caa586b15.json
   ```

### 3. 구글 시트 권한 설정

1. 구글 시트를 서비스 계정 이메일과 공유
2. 편집 권한 부여

### 4. 로컬 실행

```bash
python app.py
```

서버가 시작되면 브라우저에서 `http://localhost:5000`으로 접속하세요.

## Render 배포 가이드

### 1. GitHub 저장소 준비
1. 이 프로젝트를 GitHub에 업로드
2. Google 서비스 계정 JSON 파일은 **절대 GitHub에 올리지 마세요** (.gitignore에 포함됨)

### 2. Render 계정 생성 및 서비스 생성
1. [Render.com](https://render.com)에 가입
2. "New +" 버튼 클릭 → "Web Service" 선택
3. GitHub 저장소 연결

### 3. Render 배포 설정
- **Name**: 원하는 서비스 이름 (예: vincit-dashboard)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 4. 환경 변수 설정
Render 대시보드에서 "Environment" 탭으로 이동하여 다음 환경 변수를 추가:

#### GOOGLE_SERVICE_ACCOUNT_JSON
Google 서비스 계정 JSON 키 파일의 **전체 내용**을 복사하여 붙여넣기:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

#### FLASK_ENV (선택사항)
- Value: `production`

### 5. 배포 완료
- "Create Web Service" 클릭
- 배포가 완료되면 Render에서 제공하는 URL로 접속 가능

### 6. 자동 재배포
- GitHub에 코드를 푸시하면 자동으로 재배포됩니다
- 수동 배포: Render 대시보드에서 "Manual Deploy" 클릭

## 구글 시트 데이터 형식

다음과 같은 컬럼이 필요합니다:

- 가격: 매물 가격
- 주소: 매물 주소
- 등록날짜: 매물 등록일
- 조회수: 총 조회수
- 담당자: 담당자 이름 (E열)
- 등록번호: 매물 고유번호 (G열)
- 문의건수: 문의 건수 (H열)
- 올린날짜: 올린 날짜 (I열)
- 일평균조회수: 일평균 조회수
- 어제문의수: 어제 문의 수 (K열)

## 파일 구조

```
├── app.py                   # 메인 Flask 애플리케이션 (배포용)
├── 일일사이트메인최종.py      # 로컬 개발용 파일
├── requirements.txt         # 필요한 패키지 목록
├── README.md               # 프로젝트 설명서
├── .gitignore              # Git 제외 파일 목록
├── templates/
│   └── index.html          # 웹 대시보드 템플릿
└── static/                 # 정적 파일 (CSS, JS, 이미지 등)
```

## 주요 기능

### 담당자 목록
- 담당자별 전날 문의 수 표시
- 클릭하여 담당자 선택

### 담당매물
- 선택된 담당자의 매물 목록
- 매물번호, 주소, 금액, 문의수 표시
- 문의수 기준 오름차순 정렬

### 조회수
- 선택된 담당자의 매물별 조회수
- 일평균 조회수 기준 오름차순 정렬

### 순위
- 전체 담당자 문의수 기준 순위
- 1-3위 특별 표시
- 총 문의수 및 평균 문의수 통계

## 문제 해결

### 구글 시트 연결 오류
1. 서비스 계정 JSON 파일 경로 확인
2. 구글 시트 공유 권한 확인
3. API 활성화 상태 확인

### 데이터가 표시되지 않는 경우
1. 구글 시트의 '최종데이터' 시트 이름 확인
2. 컬럼명이 정확한지 확인
3. 브라우저 개발자 도구에서 오류 메시지 확인

### Render 배포 오류
1. 환경 변수 `GOOGLE_SERVICE_ACCOUNT_JSON`이 올바르게 설정되었는지 확인
2. JSON 형식이 유효한지 확인
3. Render 로그에서 오류 메시지 확인

## 보안 주의사항

- **Google 서비스 계정 JSON 키를 GitHub에 절대 업로드하지 마세요**
- 환경 변수로만 관리하세요
- `.gitignore` 파일이 올바르게 설정되어 있는지 확인하세요

## 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Data Source**: Google Sheets API
- **Deployment**: Render
- **Libraries**: gspread, pandas, google-auth 