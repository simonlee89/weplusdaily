# Vercel 배포 가이드

## 1. 환경 변수 설정

Vercel 대시보드에서 다음 환경 변수들을 설정해야 합니다:

### 1.1 Vercel 대시보드 접속
1. [Vercel 대시보드](https://vercel.com/dashboard)에 로그인
2. 프로젝트 선택
3. Settings 탭 클릭
4. Environment Variables 메뉴 선택

### 1.2 필수 환경 변수

#### GOOGLE_SPREADSHEET_ID
- **값**: `1I0Vp01nTB2PnXK4QOY-kIdu5JbYFGT5RJ8jXCZ5YXjM`
- **설명**: 구글 스프레드시트 ID

#### GOOGLE_SERVICE_ACCOUNT_JSON
- **값**: 구글 서비스 계정 JSON 전체 내용 (한 줄로)
- **예시**: 
```json
{"type":"service_account","project_id":"your-project-id","private_key_id":"your-key-id","private_key":"-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n","client_email":"your-service-account@your-project.iam.gserviceaccount.com","client_id":"your-client-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}
```

#### FLASK_ENV
- **값**: `production`
- **설명**: Flask 환경 설정

## 2. 구글 서비스 계정 설정

### 2.1 구글 클라우드 콘솔에서 서비스 계정 생성
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 선택 또는 새 프로젝트 생성
3. "IAM 및 관리자" > "서비스 계정" 메뉴 선택
4. "서비스 계정 만들기" 클릭
5. 서비스 계정 이름 입력 후 생성
6. 생성된 서비스 계정 클릭 > "키" 탭 > "키 추가" > "새 키 만들기" > JSON 선택
7. 다운로드된 JSON 파일의 내용을 복사

### 2.2 Google Sheets API 활성화
1. Google Cloud Console에서 "API 및 서비스" > "라이브러리" 선택
2. "Google Sheets API" 검색 후 활성화
3. "Google Drive API"도 검색 후 활성화

### 2.3 스프레드시트 공유
1. 구글 스프레드시트 열기
2. "공유" 버튼 클릭
3. 서비스 계정 이메일 주소 추가 (JSON의 client_email 값)
4. "편집자" 권한 부여

## 3. 배포 확인

### 3.1 테스트 엔드포인트
배포 후 다음 URL들을 확인하세요:

- **메인 페이지**: `https://your-app.vercel.app/`
- **헬스체크**: `https://your-app.vercel.app/health`
- **연결 테스트**: `https://your-app.vercel.app/api/test`
- **데이터 API**: `https://your-app.vercel.app/api/data`

### 3.2 문제 해결
1. **환경 변수 확인**: `/api/test` 엔드포인트에서 환경 변수 상태 확인
2. **로그 확인**: Vercel 대시보드 > Functions 탭에서 로그 확인
3. **권한 확인**: 구글 스프레드시트 공유 권한 재확인

## 4. 주의사항

- 환경 변수의 JSON 값에는 개행 문자가 포함되어 있으므로 정확히 복사해야 합니다
- private_key 값의 `\n`은 실제 개행 문자로 처리됩니다
- 서비스 계정 이메일이 스프레드시트에 공유되어 있어야 합니다
- Vercel의 서버리스 함수는 실행 시간 제한이 있으므로 대용량 데이터 처리 시 주의가 필요합니다 