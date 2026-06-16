# 전세가드 AI 작업 로그

작성일: 2026-06-16

## 1. 작업 기준

프로젝트 방향성은 전세 매물을 100% 안전하다고 단정하는 서비스가 아니라, 현재 데이터 기준으로 위험 요소와 추가 확인 항목을 리포트로 제공하는 서비스다.

핵심 표현 기준:

```text
현재 데이터 기준 위험 요소
추가 확인 필요 항목
근거 기반 분석
계약 전 전문가 및 최신 서류 확인 권장
```

사용하지 않을 표현:

```text
안전합니다
문제없습니다
계약해도 됩니다
전세사기가 아닙니다
```

## 2. 현재 프로젝트 상태 확인

확인 경로:

```text
C:\pk\jeonse-guard
```

확인된 주요 폴더:

```text
jeonse-db
jeonse-guard-api
jeonse-guard-web
md정리
더미 및 실제 데이터
```

루트 `C:\pk\jeonse-guard`는 git 저장소가 아니었다.

## 3. 프론트엔드 상태

경로:

```text
C:\pk\jeonse-guard\jeonse-guard-web
```

확인 내용:

```text
Vue 3 프로젝트 구조 존재
src/components 구성 존재
src/api/propertyApi.js 존재
index.html은 현재 Vue 진입점이 아니라 정적 HTML/JS 화면 상태
npm run build 성공
```

현재 `index.html`은 이전에 `preview.html` 내용을 그대로 반영한 상태다.

## 4. 백엔드 상태

경로:

```text
C:\pk\jeonse-guard\jeonse-guard-api
```

확인된 API 구조:

```text
app/main.py
app/database.py
app/routers/properties.py
app/routers/recommendations.py
app/routers/analysis.py
```

기존 등록 라우트:

```text
GET /
GET /health
GET /api/properties
GET /api/properties/{property_id}
GET /api/recommendations
```

문제:

```text
analysis.py는 존재했지만 main.py에 analysis_router가 등록되지 않아
GET /api/properties/{property_id}/analysis 라우트가 미등록 상태였다.
```

## 5. analysis_router 등록 작업

수정 파일:

```text
C:\pk\jeonse-guard\jeonse-guard-api\app\main.py
```

추가 내용:

```python
app.include_router(analysis_router)
```

검증:

```text
python -m py_compile app\main.py 통과
GET /api/properties/{property_id}/analysis 라우트 등록 확인
```

## 6. DB 상태 확인

Docker 컨테이너:

```text
jeonse-postgres
```

상태:

```text
실행 중
포트: 5434 -> 5432
DB 접속 성공
```

확인된 테이블 및 건수:

```text
ai_reports: 0
properties: 50
property_risk_checks: 50
recommendation_logs: 30
risk_score_rules: 12
stg_dummy_properties: 50
stg_recommendation_logs: 30
stg_user_preferences: 10
user_preferences: 10
```

## 7. 실제 CSV 데이터 확인

데이터 경로:

```text
C:\pk\jeonse-guard\더미 및 실제 데이터
```

확인 결과:

```text
CSV 총 57개
전체 용량 약 387.77MB
```

구성:

```text
더미/시드 CSV 5개
법정동코드 CSV 1개
아파트 전월세 CSV 12개
연립다세대 전월세 CSV 13개
오피스텔 전월세 CSV 13개
단독다가구 전월세 CSV 13개
```

실거래가 CSV 특징:

```text
파일 첫 줄부터 바로 컬럼이 아님
상단 안내문 존재
실제 컬럼 헤더는 보통 16번째 줄부터 시작
전월세구분 컬럼으로 전세/월세 구분 가능
보증금 단위는 만원
DB 적재 시 원 단위 변환 필요
```

## 8. 실제 실거래가 staging 적재 스크립트 추가

추가 파일:

```text
C:\pk\jeonse-guard\jeonse-guard-api\scripts\load_real_rent_transactions.py
```

역할:

```text
실제 전월세 CSV 파일 탐색
아파트, 연립다세대, 오피스텔, 단독다가구 파일만 대상
CSV 상단 안내문 skip
전월세구분 = 전세 행만 적재
보증금/월세 만원 단위를 원 단위로 변환
계약년월/계약일을 contract_date로 변환
CP949, EUC-KR, UTF-8 계열 인코딩 자동 감지
```

생성 테이블:

```text
stg_real_rent_transactions
```

주요 컬럼:

```text
source_file
source_row_no
property_type
property_type_kr
address_region
sido
sigungu
eupmyeondong
jibun
complex_name
lease_type
area_m2
contract_date
deposit_won
monthly_rent_won
floor
built_year
road_name
contract_type
renewal_right_used
housing_type
road_condition
```

주택 유형 매핑:

```text
아파트 -> APT
연립다세대 -> VILLA
오피스텔 -> OFFICETEL
단독다가구 -> SINGLE_MULTI
```

## 9. 실제 CSV 적재 결과

실행 결과:

```text
총 전세 행 801,923건 적재
대상 CSV 51개
보증금 null 0건
```

유형별 적재 건수:

```text
APT: 545,318
VILLA: 97,594
OFFICETEL: 74,230
SINGLE_MULTI: 84,781
```

계약일 범위:

```text
2025-05-06 ~ 2026-06-04
```

## 10. 다음 권장 작업

다음 단계는 실제 실거래가 staging 데이터를 바로 매물로 쓰는 것이 아니라, 먼저 지역/주택유형별 전세 시세 요약 테이블을 만드는 것이다.

권장 작업:

```text
1. stg_real_rent_transactions 기반 지역/유형별 시세 요약 테이블 생성
2. 중앙값, 평균, 샘플 수 계산
3. 기존 properties 매물의 보증금과 지역 시세 비교
4. 분석 리포트에 주변 전세가 대비 보증금 수준 표시
5. 추천 API에서 가격 근거 점수 개선
```

서비스 메시지 방향:

```text
현재 매물 보증금이 같은 지역과 주택유형의 최근 전세 거래 대비 어느 수준인지 보여준다.
단, 실거래가 데이터는 참고 지표이며 계약 전 최신 등기부등본, 권리관계, 보증보험 가능 여부 확인이 필요하다.
```
