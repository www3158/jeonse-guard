# 전세가드 AI 프로젝트 작업 정리

작성일: 2026-06-16

---

## 1. 프로젝트 개요

현재 프로젝트는 **전세가드 AI**라는 이름의 전세 매물 추천 및 전세사기 위험 요소 분석 서비스이다.

처음에는 단순히 전세 매물을 추천하는 서비스처럼 접근했지만, 최종 방향은 다음처럼 정리했다.

```text
전세가드 AI는 매물이 100% 안전하다고 단정하지 않는다.
대신 공공데이터, 지역 위험도, 전월세 실거래가, 보증사고 데이터, 권리관계 체크리스트를 기준으로
어떤 위험 요소가 있고 무엇을 추가 확인해야 하는지 근거와 함께 보여준다.
```

따라서 이 프로젝트의 핵심은 다음과 같다.

```text
전세 계약 전 위험 검증 리포트가 붙은 매물 추천 서비스
```

---

## 2. 최종 기술 스택

기존에는 Spring Boot 사용 가능성도 있었지만, 현재는 Spring Boot를 제외하고 **FastAPI 중심**으로 정리했다.

```text
Frontend: HTML / CSS / JavaScript 또는 Vue 3
Backend: FastAPI
Database: PostgreSQL 14
Container: Docker
API Server: Uvicorn
```

현재 전체 구조는 다음과 같다.

```text
Frontend 화면
    ↓
FastAPI
    ↓
PostgreSQL 14
```

---

## 3. 핵심 서비스 방향

이 서비스는 “AI가 안전하다고 판단한 매물”이라고 말하면 안 된다.  
왜냐하면 등기부등본, 선순위 임차인, 임대인 세금 체납, 보증보험 가입 가능 여부 등을 100% 실시간으로 검증하지 않는 이상 안전을 보장할 수 없기 때문이다.

### 피해야 할 표현

```text
이 매물은 안전합니다.
이 매물은 전세사기가 아닙니다.
계약해도 됩니다.
문제없는 매물입니다.
```

### 사용해야 할 표현

```text
현재 데이터 기준 위험 요소가 낮은 매물입니다.
확인된 위험 항목이 적습니다.
계약 전 추가 확인이 필요한 항목을 안내합니다.
권리관계와 보증금 위험 요소를 기준으로 분석한 결과입니다.
위험 요소를 확인하고 추천한 매물입니다.
현재 데이터 기준 위험도가 낮은 매물입니다.
```

---

## 4. 안전함을 증명하는 방식

이 프로젝트에서 중요한 것은 “AI가 안전하다고 말하는 것”이 아니다.

중요한 것은 다음이다.

```text
왜 위험도가 낮다고 판단했는지
어떤 항목을 확인했는지
어떤 항목은 추가 확인이 필요한지
점수가 어떤 기준으로 계산되었는지
```

즉, 사용자가 봤을 때 단순한 AI 점수가 아니라 **근거 기반 위험 분석 리포트**를 확인할 수 있어야 한다.

---

## 5. 위험 검증 리포트 구조

매물 상세 분석에서는 다음 구조를 보여주는 것이 좋다.

```text
전세가드 AI 분석 리포트

1. 위험 점수
현재 데이터 기준 위험점수는 18점입니다.
위험 요소가 낮은 편이지만 계약 전 서류 재확인은 필요합니다.

2. 확인된 항목
- 압류/가압류 위험 없음
- 신탁등기 위험 없음
- 중개사 영업상태 확인 완료
- 건축물대장 확인 완료

3. 추가 확인 필요 항목
- 잔금 전 등기부등본 재확인 필요
- 선순위 임차인 보증금 확인 필요
- 전세보증금반환보증 가입 가능 여부 확인 필요

4. 중개사에게 물어볼 질문
- 현재 등기부등본 기준 근저당권이 있나요?
- 선순위 임차인이 있다면 보증금 총액은 얼마인가요?
- HUG 전세보증보험 가입 가능한 매물인가요?
- 잔금일 직전 등기부등본을 다시 확인할 수 있나요?

5. 특약 예시
- 잔금 지급 전 등기부등본상 추가 권리 변동이 발생한 경우 계약을 해제할 수 있다.
- 전세보증금반환보증 가입이 불가능한 경우 계약을 해제할 수 있다.
```

---

## 6. 위험 점수 산정 기준

위험 점수는 단순 AI 점수가 아니라 룰 기반으로 설명 가능해야 한다.

| 항목 | 조건 | 위험점수 |
|---|---:|---:|
| 근저당 있음 | `has_mortgage = true` | +20 |
| 압류 있음 | `has_seizure = true` | +35 |
| 가압류 있음 | `has_provisional_seizure = true` | +30 |
| 신탁등기 있음 | `has_trust = true` | +40 |
| 임차권등기 있음 | `has_leasehold_registration = true` | +35 |
| 보증보험 미확인 | `insurance_checked = false` | +10 |
| 선순위 임차인 미확인 | `senior_tenant_checked = false` | +15 |
| 건축물대장 미확인 | `building_register_checked = false` | +10 |
| 중개사 상태 미확인 | `broker_status_checked = false` | +10 |
| 잔금 전 등기부 재확인 미완료 | `registry_checked_before_balance = false` | +15 |

등급 기준 예시:

```text
0~25점: 위험 요소 낮음
26~55점: 주의 필요
56점 이상: 위험 요소 많음
```

---

## 7. 데이터 수집 및 활용 방향

현재 프로젝트에서 활용하기로 한 데이터는 다음과 같다.

### 7.1 임대시장 현황

파일:

```text
임대시장 현황_전체.xls
```

활용 내용:

```text
시도 / 시군구
아파트 전세가율 1년 / 3개월
연립·다세대 전세가율 1년 / 3개월
보증사고 건수
보증사고 금액
보증사고 사고율
경매건수
낙찰건수
낙찰률
낙찰가율
```

활용 목적:

```text
지역별 위험도 산정
전세가율 참고
보증사고 많은 지역 판단
```

### 7.2 법정동 코드

파일:

```text
국토교통부_법정동코드_20250805.csv
```

활용 내용:

```text
법정동코드
법정동명
폐지여부
```

활용 목적:

```text
지역명과 법정동 코드 매칭
공공데이터 지역 기준 통일
```

### 7.3 전월세 실거래가 데이터

활용하기로 한 데이터:

```text
아파트 전월세
연립다세대 전월세
오피스텔 전월세
단독다가구 전월세
```

확인된 데이터 규모:

```text
아파트 전월세: 1,079,888건
연립다세대 전월세: 280,216건
오피스텔 전월세: 305,182건
단독다가구 전월세: 562,679건
총 전월세 데이터: 2,227,965건
```

활용 목적:

```text
주변 전세 시세 비교
보증금 수준 적정성 판단
지역별 전월세 흐름 참고
```

### 7.4 HUG 전세금반환보증 사고 현황

파일:

```text
주택도시보증공사_지역별 전세금반환보증 사고현황_20250831.xlsx
```

활용 목적:

```text
지역별 보증사고 위험도 분석
보증사고 많은 지역 가중치 반영
```

### 7.5 부동산 중개업소 정보

파일:

```text
부동산중개업사무소정보.zip
```

확인된 영업상태 예시:

```text
영업중: 107,625
휴업: 515
업무정지: 78
휴업연장: 44
```

활용 목적:

```text
중개업소 영업상태 확인
중개사 위험 요소 반영
```

---

## 8. MVP에서 제외한 기능

현재 MVP에서는 다음 기능은 제외하기로 했다.

```text
등기부등본 자동 수집
등기부등본 OCR
등기부등본 PDF 업로드 분석
매매 실거래가 기반 직접 전세가율 계산
Spring Boot 백엔드
```

제외 이유:

```text
등기부등본 자동 수집/OCR은 MVP에서 구현 난이도가 높다.
현재 목적은 전세 위험 요소를 설명하고 확인 항목을 제공하는 것이다.
매매 데이터는 현재 전세사기 예방 MVP의 핵심이 아니므로 제외한다.
```

---

## 9. 데이터베이스 구성

현재 PostgreSQL 14를 Docker로 사용한다.

### 9.1 Docker 컨테이너

```text
컨테이너명: jeonse-postgres
이미지: pgvector/pgvector:pg14
포트: 5434:5432
DB명: jeonse_guard
사용자명: jeonse
비밀번호: 1234
```

기존 Hi-Five DB가 5433을 사용하고 있기 때문에, 전세가드 DB는 5434 포트를 사용한다.

### 9.2 Docker Compose

```yaml
services:
  jeonse-postgres:
    image: pgvector/pgvector:pg14
    container_name: jeonse-postgres
    restart: always
    environment:
      POSTGRES_DB: jeonse_guard
      POSTGRES_USER: jeonse
      POSTGRES_PASSWORD: 1234
    ports:
      - "5434:5432"
    volumes:
      - jeonse-postgres-data:/var/lib/postgresql/data

volumes:
  jeonse-postgres-data:
```

### 9.3 pgAdmin 연결 정보

```text
Host name/address: localhost
Port: 5434
Maintenance database: jeonse_guard
Username: jeonse
Password: 1234
```

---

## 10. 생성한 DB 테이블

주요 테이블:

```text
properties
property_risk_checks
risk_score_rules
user_preferences
recommendation_logs
ai_reports
```

스테이징 테이블:

```text
stg_dummy_properties
stg_user_preferences
stg_recommendation_logs
```

---

## 11. 더미 데이터

생성한 더미 데이터 파일:

```text
jeonse_dummy_seed_dataset.xlsx
jeonse_dummy_seed_csv.zip
```

CSV 구성:

```text
dummy_properties.csv
risk_score_rules.csv
user_preferences_seed.csv
recommendation_logs_seed.csv
data_dictionary.csv
```

더미 매물 구조:

```text
총 50개 매물
안전 15개
주의 20개
위험 15개
```

대상 지역:

```text
인천 부평구
인천 미추홀구
경기도 부천시 원미구
서울 구로구
서울 관악구
```

최종 DB 적재 결과:

```text
properties: 50건
property_risk_checks: 50건
user_preferences: 10건
recommendation_logs: 30건
risk_score_rules: 12건
```

---

## 12. FastAPI 백엔드

FastAPI 프로젝트 경로:

```text
C:\pk\jeonse-guard\jeonse-guard-api
```

실행 명령어:

```bat
cd /d C:\pk\jeonse-guard\jeonse-guard-api
.venv\Scripts\activate
docker start jeonse-postgres
python -m uvicorn app.main:app --reload --port 8000
```

---

## 13. FastAPI 환경 변수

`.env` 파일:

```env
DB_HOST=localhost
DB_PORT=5434
DB_NAME=jeonse_guard
DB_USER=jeonse
DB_PASSWORD=1234
```

---

## 14. FastAPI 프로젝트 구조

```text
jeonse-guard-api
 ├─ app
 │   ├─ __init__.py
 │   ├─ main.py
 │   ├─ database.py
 │   └─ routers
 │       ├─ __init__.py
 │       ├─ properties.py
 │       ├─ recommendations.py
 │       └─ analysis.py
 ├─ .env
 └─ requirements.txt
```

---

## 15. 구현된 API

현재 사용 중인 API:

```text
GET /
GET /health
GET /api/properties
GET /api/properties/{property_id}
GET /api/recommendations
GET /api/properties/{property_id}/analysis
```

추천 API 예시:

```text
/api/recommendations
/api/recommendations?max_deposit=250000000
/api/recommendations?region=구로구&max_deposit=250000000
/api/recommendations?property_type=VILLA&max_deposit=200000000
```

---

## 16. API 동작 확인

`/api/properties`는 정상적으로 50개 매물을 반환했다.

반환 필드 예시:

```text
id
external_property_id
title
address
region
lawd_cd
property_type
deposit
monthly_rent
area_m2
floor
maintenance_fee
station_distance_min
move_in_date
risk_level
risk_tags
risk_score
has_mortgage
has_seizure
has_provisional_seizure
has_trust
has_leasehold_registration
insurance_checked
senior_tenant_checked
building_register_checked
broker_status_checked
```

`/api/recommendations`도 SQL 파라미터 오류를 수정한 뒤 정상 동작했다.

---

## 17. 프론트엔드 방향

초기에는 Vue 3 기반으로 구성하려 했지만, 바로 열어서 확인하기 위해 HTML/CSS/JS 단일 파일 버전도 만들었다.

프론트엔드 핵심 요구사항:

```text
기업형 부동산 홈페이지 느낌
고급 부동산 메인 비주얼
흰색 헤더
블랙/골드/아이보리 색감
추천 매물 카드
전체 매물 카드
테마별 매물 섹션
전세 체크리스트
AI 안전 인사이트 섹션
카카오톡 오픈채팅 연결
메일 문의 연결
상세 위험 분석 모달
```

---

## 18. 참고 사이트 디자인 방향

참고 사이트 캡처를 기반으로 다음 방향을 잡았다.

```text
고급 부동산 회사 홈페이지
상단 기업형 헤더
대형 메인 비주얼
매물 카드 중심 구성
분야별 추천 매물
우측 상담 버튼
기업형 푸터
```

단, 실제 참고 사이트의 코드, 이미지, 상호, 연락처, 문구는 복사하지 않고 구조와 분위기만 참고했다.

---

## 19. 생성한 프론트 시안 파일

생성한 HTML 시안:

```text
jeonse_guard_ai_single.html
jeonse_guard_corporate_single.html
jeonse_guard_premium_corporate.html
jeonse_guard_luxury_corporate_v2.html
```

마지막 고급 버전:

```text
jeonse_guard_luxury_corporate_v2.html
```

구성:

```text
상단 블랙 안내 바
흰색 sticky 헤더
로고: 전세가드 AI
추천매물 / 전체매물 / 테마매물 / 안전분석 / 체크리스트 / 문의하기 메뉴
대형 히어로 이미지
우측 AI 안전 분석 패널
히어로 하단 통계 박스
오늘의 AI 추천매물
분야별 추천매물
최신분양 & 컨설턴트 추천
AI 전세 안전 인사이트
계약 전 체크리스트
문의하기
기업형 푸터
우측 오픈채팅 / 메일문의 / 추천매물 플로팅 버튼
```

---

## 20. 프론트 실행 방법

HTML 파일을 저장한 폴더에서 실행:

```bat
python -m http.server 5173
```

브라우저 접속:

```text
http://localhost:5173/jeonse_guard_luxury_corporate_v2.html
```

FastAPI도 함께 켜야 실제 매물 데이터가 표시된다.

```bat
cd /d C:\pk\jeonse-guard\jeonse-guard-api
.venv\Scripts\activate
docker start jeonse-postgres
python -m uvicorn app.main:app --reload --port 8000
```

---

## 21. 카카오톡 / 메일 연결 정보

카카오톡 오픈채팅:

```text
https://open.kakao.com/o/g7TDr4yi
```

문의 메일:

```text
last5324@gmail.com
```

프론트 연결 방식:

```text
카카오톡 상담 버튼 클릭 → 오픈채팅 새 창 열기
메일 문의 버튼 클릭 → mailto:last5324@gmail.com 실행
문의 폼 제출 → mailto 제목/본문 자동 생성
```

---

## 22. 현재까지의 핵심 결론

이 프로젝트의 최종 설득 포인트는 다음이다.

```text
우리는 매물이 100% 안전하다고 단정하지 않는다.

대신,
공공데이터 + 지역 위험도 + 실거래가 + 보증사고 데이터 + 권리관계 체크리스트를 기준으로
어떤 위험 요소가 있고,
무엇을 추가 확인해야 하는지
근거와 함께 보여준다.
```

따라서 프로젝트 소개 문구는 다음처럼 잡는 것이 좋다.

```text
전세가드 AI는 공공데이터와 체크리스트 기반으로
매물의 위험 요소를 점수화하고,
계약 전 확인해야 할 항목을 리포트로 제공합니다.
```

---

## 23. 향후 작업 방향

다음 작업은 아래 순서로 진행하면 된다.

```text
1. 프론트 문구에서 “안전 보장” 표현 제거
2. “전세 위험 검증 리포트” 중심으로 화면 문구 수정
3. 상세 분석 모달에 점수 산정 근거 표시
4. 데이터 출처 표시 섹션 추가
5. 추천 매물 카드에 “근거 보기” 버튼 강화
6. FastAPI analysis API 응답 구조 보강
7. 실제 전월세 실거래가 / HUG / 임대시장 데이터와 연결 확장
8. 포트폴리오 발표용 시나리오 작성
```

---

## 24. 발표에서 강조할 말

```text
이 서비스는 단순 부동산 매물 추천 사이트가 아닙니다.

전세 계약 전 확인해야 할 위험 요소를
공공데이터와 체크리스트 기반으로 정리하고,
매물별 위험 점수와 확인 항목을 리포트로 제공하는
전세 위험 검증 기반 매물 추천 서비스입니다.
```
