# Render 배포 가이드

## 🚀 Render 배포 단계별 가이드

### 1. 사전 준비
- [x] GitHub 저장소에 코드 업로드
- [x] Google 서비스 계정 JSON 키 준비
- [x] Google Sheets API 활성화
- [x] 구글 시트 공유 권한 설정

### 2. Render 계정 및 서비스 생성
1. [Render.com](https://render.com) 가입
2. "New +" → "Web Service" 선택
3. GitHub 저장소 연결

### 3. 배포 설정
```yaml
Name: vincit-dashboard
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

### 4. 필수 환경 변수 설정
Render 대시보드 → Environment 탭에서 다음 변수들을 추가:

#### GOOGLE_SERVICE_ACCOUNT_JSON
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

#### GOOGLE_SPREADSHEET_ID (선택사항)
```
1I0Vp01nTB2PnXK4QOY-kIdu5JbYFGT5RJ8jXCZ5YXjM
```

#### FLASK_ENV
```
production
```

### 5. 배포 확인
- 배포 완료 후 제공되는 URL로 접속
- `/health` 엔드포인트로 헬스체크
- `/api/test` 엔드포인트로 구글 시트 연결 테스트

### 6. 문제 해결
#### 배포 실패 시
1. Render 로그 확인
2. 환경 변수 설정 재확인
3. JSON 형식 유효성 검사

#### 데이터 로드 실패 시
1. 구글 시트 공유 권한 확인
2. 서비스 계정 이메일 권한 확인
3. API 활성화 상태 확인

### 7. 자동 재배포
- GitHub에 푸시하면 자동 재배포
- 수동 배포: Render 대시보드에서 "Manual Deploy"

## 🔧 로컬 개발 환경

### 환경 변수 설정
1. `env.example`을 `.env`로 복사
2. 실제 값으로 변경
3. 또는 JSON 키 파일을 다음 위치에 저장:
   - `service-account.json` (프로젝트 루트)
   - `keys/service-account.json`

### 실행
```bash
pip install -r requirements.txt
python app.py
```

## 📋 체크리스트

### 배포 전
- [ ] 환경 변수 설정 완료
- [ ] Google 서비스 계정 JSON 키 준비
- [ ] 구글 시트 공유 권한 설정
- [ ] requirements.txt 확인

### 배포 후
- [ ] 웹사이트 접속 확인
- [ ] 데이터 로드 확인
- [ ] 모든 기능 테스트
- [ ] 에러 로그 확인 

## Vercel 배포 가이드

### 1. 환경 변수 설정

Vercel 대시보드에서 다음 환경 변수들을 설정해야 합니다:

#### 필수 환경 변수:
- `GOOGLE_SERVICE_ACCOUNT_JSON`: 구글 서비스 계정 JSON 키 (전체 JSON 내용을 문자열로)
- `GOOGLE_SPREADSHEET_ID`: 구글 스프레드시트 ID (기본값: 1I0Vp01nTB2PnXK4QOY-kIdu5JbYFGT5RJ8jXCZ5YXjM)

#### 환경 변수 설정 방법:
1. Vercel 대시보드 → 프로젝트 선택
2. Settings → Environment Variables
3. 다음 변수들을 추가:

```
Name: GOOGLE_SERVICE_ACCOUNT_JSON
Value: {"type":"service_account","project_id":"your-project-id",...} (전체 JSON)

Name: GOOGLE_SPREADSHEET_ID  
Value: 1I0Vp01nTB2PnXK4QOY-kIdu5JbYFGT5RJ8jXCZ5YXjM
```

### 2. 구글 서비스 계정 설정

1. Google Cloud Console에서 서비스 계정 생성
2. Google Sheets API 활성화
3. 서비스 계정 키 다운로드 (JSON 형식)
4. 구글 스프레드시트에 서비스 계정 이메일 공유 권한 부여

### 3. 문제 해결

#### API에서 빈 배열 [] 반환되는 경우:
1. `/api/test` 엔드포인트로 연결 상태 확인
2. 환경 변수 설정 확인
3. 구글 시트 공유 권한 확인
4. 허용된 담당자 목록과 실제 데이터 일치 여부 확인

#### 디버깅 방법:
- Vercel 함수 로그 확인: Vercel 대시보드 → Functions → 로그 확인
- 테스트 엔드포인트 사용: `https://your-app.vercel.app/api/test` 