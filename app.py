import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# 구글 시트 설정
SPREADSHEET_ID = '1I0Vp01nTB2PnXK4QOY-kIdu5JbYFGT5RJ8jXCZ5YXjM'
SHEET_NAME = '최종데이터'

# 필터링할 담당자 목록
ALLOWED_MANAGERS = ['유현준', '백은주', '윤진식', '문수인', '김혜린', '김민재', '함원식', '이상준']

def get_google_sheet_data():
    """구글 시트에서 데이터를 가져오는 함수"""
    try:
        # 서비스 계정 인증
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        # 환경 변수에서 JSON 키 읽기 (Render 배포용)
        service_account_info = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if service_account_info:
            # JSON 문자열을 딕셔너리로 변환
            service_account_dict = json.loads(service_account_info)
            credentials = Credentials.from_service_account_info(
                service_account_dict, scopes=scope)
        else:
            # 로컬 개발용 파일 사용 (fallback)
            local_file = r'C:\Users\1\Desktop\구글서비스키\더탑원이스트 구글서비스키\thetopone-fe6caa586b15.json'
            if os.path.exists(local_file):
                credentials = Credentials.from_service_account_file(local_file, scopes=scope)
            else:
                print("Google 서비스 계정 키를 찾을 수 없습니다.")
                return []
        
        # 구글 시트 클라이언트 생성
        gc = gspread.authorize(credentials)
        
        # 스프레드시트 열기
        spreadsheet = gc.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        
        # 모든 데이터 가져오기
        data = worksheet.get_all_records()
        
        return data
    except Exception as e:
        print(f"구글 시트 데이터 가져오기 오류: {e}")
        return []

def process_data(raw_data):
    """원시 데이터를 처리하여 대시보드용 데이터로 변환"""
    if not raw_data:
        return []
    
    # DataFrame으로 변환
    df = pd.DataFrame(raw_data)
    
    # 컬럼명 확인 및 매핑 (E열=담당자, G열=등록번호, H열=문의건수, I열=올린날짜, K열=어제문의수)
    columns = list(df.columns)
    print(f"사용 가능한 컬럼: {columns}")
    
    # 정확한 매핑: E열(인덱스 4) = 담당자, G열(인덱스 6) = 등록번호, H열(인덱스 7) = 문의건수, I열(인덱스 8) = 올린날짜, K열(인덱스 10) = 어제문의수
    if len(columns) >= 11:  # K열까지 있는지 확인
        manager_col = columns[4]  # E열 (인덱스 4) - 담당자
        property_id_col = columns[6]  # G열 (인덱스 6) - 등록번호(매물번호)
        inquiry_count_col = columns[7]  # H열 (인덱스 7) - 문의건수
        upload_date_col = columns[8]  # I열 (인덱스 8) - 올린날짜
        yesterday_inquiry_col = columns[10]  # K열 (인덱스 10) - 어제문의수
    else:
        # 기존 컬럼명 사용 (fallback)
        manager_col = '담당자'
        property_id_col = '등록번호'
        inquiry_count_col = '문의수'  # fallback
        upload_date_col = '업데이트날짜'  # fallback
        yesterday_inquiry_col = '문의수'  # fallback
    
    print(f"담당자 컬럼: {manager_col} (E열), 등록번호 컬럼: {property_id_col} (G열), 문의건수 컬럼: {inquiry_count_col} (H열), 올린날짜 컬럼: {upload_date_col} (I열), 어제문의수 컬럼: {yesterday_inquiry_col} (K열)")
    
    # 빈 행 제거 및 허용된 담당자만 필터링
    df = df[df[manager_col].notna() & (df[manager_col] != '') & (df[manager_col] != '0') & df[manager_col].isin(ALLOWED_MANAGERS)]
    
    # 담당자별 데이터 그룹화
    manager_data = []
    
    for manager_name in df[manager_col].unique():
        if pd.isna(manager_name) or manager_name == '' or manager_name == '0' or manager_name not in ALLOWED_MANAGERS:
            continue
            
        manager_df = df[df[manager_col] == manager_name]
        
        # 총 문의 수 계산 (H열 문의건수 컬럼의 합)
        total_inquiries = int(manager_df[inquiry_count_col].fillna(0).sum()) if inquiry_count_col in df.columns else 0
        
        # 어제 문의 수 계산 (K열의 합)
        yesterday_inquiries = int(manager_df[yesterday_inquiry_col].fillna(0).sum()) if yesterday_inquiry_col in df.columns else 0
        
        # 총 기간 계산 (올린날짜의 최대값)
        total_days = 0
        if upload_date_col in df.columns:
            try:
                max_days = manager_df[upload_date_col].fillna(0).max()
                if pd.notna(max_days) and str(max_days).strip() != '':
                    total_days = int(float(max_days))
            except (ValueError, TypeError):
                total_days = 0
        
        # 담당 매물 수 계산 - C열(담당자)의 G열(등록번호) 개수
        unique_property_ids = manager_df[property_id_col].dropna().unique()
        property_count = len(unique_property_ids)
        
        # 담당 매물 목록 - 등록번호 기준으로 중복 제거
        unique_properties = manager_df.drop_duplicates(subset=[property_id_col])
        
        properties = []
        for _, row in unique_properties.iterrows():
            try:
                # 가격 처리
                price = str(row['가격']) if '가격' in df.columns and pd.notna(row['가격']) else '0'
                
                # 주소 처리
                address = str(row['주소']) if '주소' in df.columns and pd.notna(row['주소']) else ''
                
                # 등록번호를 매물ID로 사용
                property_id = str(row[property_id_col]) if pd.notna(row[property_id_col]) else 'N/A'
                
                # 해당 등록번호의 모든 행에서 문의수 합계 계산
                property_inquiries = 0
                if inquiry_count_col in df.columns:
                    property_inquiries = int(manager_df[manager_df[property_id_col] == row[property_id_col]][inquiry_count_col].fillna(0).sum())
                
                # 일평균 조회수 (해당 등록번호의 첫 번째 값 사용)
                daily_views = 0
                if '일평균조회수' in df.columns:
                    try:
                        daily_views_value = row['일평균조회수']
                        if pd.notna(daily_views_value) and str(daily_views_value).strip() != '':
                            daily_views = float(daily_views_value)
                        else:
                            daily_views = 0
                    except (ValueError, TypeError):
                        daily_views = 0
                
                # 올린날짜 처리
                upload_days = 0
                if upload_date_col in df.columns:
                    try:
                        upload_date_value = row[upload_date_col]
                        if pd.notna(upload_date_value) and str(upload_date_value).strip() != '':
                            upload_days = int(float(upload_date_value))
                        else:
                            upload_days = 0
                    except (ValueError, TypeError):
                        upload_days = 0
                
                properties.append({
                    'propertyId': property_id,
                    'address': address,
                    'amount': price,
                    'inquiries': property_inquiries,
                    'dailyViews': daily_views,
                    'uploadDays': upload_days
                })
            except Exception as e:
                print(f"매물 데이터 처리 오류: {e}")
                continue
        
        if property_count > 0:  # 매물이 있는 담당자만 추가
            manager_data.append({
                'name': manager_name,
                'totalInquiries': total_inquiries,
                'yesterdayInquiries': yesterday_inquiries,
                'totalDays': total_days,
                'properties': properties,
                'propertyCount': property_count  # 실제 매물 수 추가
            })
    
    return manager_data

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API 엔드포인트: 대시보드 데이터 반환"""
    try:
        raw_data = get_google_sheet_data()
        processed_data = process_data(raw_data)
        return jsonify(processed_data)
    except Exception as e:
        print(f"데이터 처리 오류: {e}")
        return jsonify([])

if __name__ == '__main__':
    # templates 폴더 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # static 폴더 생성
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("서버 시작 중...")
    # Render 배포용 포트 설정
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    if debug_mode:
        print("브라우저에서 http://localhost:5000 으로 접속하세요.")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port) 