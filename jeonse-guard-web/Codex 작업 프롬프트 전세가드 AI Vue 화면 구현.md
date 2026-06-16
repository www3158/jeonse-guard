# Codex 작업 프롬프트: 전세가드 AI Vue 화면 구현

## 1. 프로젝트 개요

현재 프로젝트는 **“전세가드 AI”** 라는 AI 기반 전세 매물 추천 및 전세사기 위험 분석 서비스입니다.

기존 Spring Boot는 사용하지 않고, 현재 백엔드는 **FastAPI + PostgreSQL 14** 로 동작합니다.
프론트엔드는 **Vue 3** 로 구현합니다.

---

## 2. 참고 디자인 방향

참고 사이트:

```text
http://kjrealty.co.kr/
```

참고할 부분:

* 고급 부동산 중개 사이트 느낌
* 깔끔한 헤더
* 큰 Hero 섹션
* 매물 카드 배치
* 상담/문의 CTA
* 카카오톡 오픈채팅 바로가기 같은 플로팅 버튼
* 부동산 서비스 특유의 신뢰감 있는 레이아웃

주의사항:

* 기존 사이트의 HTML, CSS, 이미지, 문구, 상호, 연락처, 로고는 절대 복사하지 않는다.
* 참고 사이트의 분위기와 구조만 참고한다.
* 콘텐츠는 모두 **전세가드 AI** 주제에 맞게 새로 작성한다.

---

## 3. 서비스명

```text
전세가드 AI
```

---

## 4. 기술 스택

```text
Frontend: Vue 3
Backend: FastAPI
Database: PostgreSQL 14
```

---

## 5. 현재 FastAPI 백엔드 주소

```text
기본 주소: http://localhost:8000
매물 목록 API: GET http://localhost:8000/api/properties
추천 매물 API: GET http://localhost:8000/api/recommendations
매물 상세 API: GET http://localhost:8000/api/properties/{id}
매물 위험 분석 API: GET http://localhost:8000/api/properties/{id}/analysis
```

추천 API 호출 예시:

```text
/api/recommendations
/api/recommendations?max_deposit=250000000
/api/recommendations?region=구로구&max_deposit=250000000
/api/recommendations?property_type=VILLA&max_deposit=200000000
```

---

## 6. 외부 연결 정보

```text
카카오톡 오픈채팅 링크:
https://open.kakao.com/o/g7TDr4yi

문의 메일:
last5324@gmail.com
```

---

## 7. 작업 목표

Vue 화면을 고급 부동산 서비스처럼 보이게 만들고, FastAPI와 연결해서 실제 DB 매물 데이터를 표시한다.

포트폴리오 시연용이므로 다음을 우선한다.

* 화면 완성도
* API 연결 안정성
* 고급스러운 부동산 서비스 느낌
* 전세사기 위험 분석 서비스라는 주제 전달력
* 모바일 반응형 대응

---

## 8. 필수 구현 화면/섹션

다음 섹션을 구현한다.

1. 메인 홈 Hero 섹션
2. 서비스 소개 섹션
3. 추천 매물 섹션
4. 전체 매물 목록 섹션
5. 매물 상세 위험 분석 모달 또는 패널
6. 전세사기 체크리스트 섹션
7. 문의하기 섹션
8. 카카오톡/메일 문의 플로팅 버튼

---

## 9. 전체 디자인 요구사항

### 디자인 톤

```text
고급 부동산 + AI 안전 진단 서비스
```

### 색상

```text
기본: 화이트
메인: 딥 네이비
포인트: 골드 / 베이지
보조 배경: 연한 그레이
위험 표시:
- 안전: 초록
- 주의: 주황
- 위험: 빨강
```

### 폰트

```text
Pretendard 우선
없으면 system-ui 사용
```

### UI 스타일

* 넓은 여백
* 카드형 UI
* 둥근 모서리
* 은은한 그림자
* 부드러운 hover 효과
* 고급스럽고 신뢰감 있는 분위기
* 과한 애니메이션은 피하고 깔끔하게 구현

---

## 10. 헤더 요구사항

상단 고정 sticky header를 구현한다.

### 구성

좌측 로고:

```text
전세가드 AI
```

메뉴:

```text
서비스 소개
추천 매물
매물 보기
위험 체크
문의하기
```

우측 버튼:

```text
카카오톡 상담
```

### 기능

* 메뉴 클릭 시 해당 섹션으로 부드럽게 스크롤 이동
* 카카오톡 상담 버튼 클릭 시 아래 링크를 새 창으로 연다.

```text
https://open.kakao.com/o/g7TDr4yi
```

---

## 11. Hero 섹션 요구사항

### 메인 제목

```text
AI가 도와주는 안전한 전세 매물 선택
```

### 부제

```text
보증금, 지역, 권리관계 위험 요소를 분석해 전세사기 가능성을 낮추는 매물 추천 서비스
```

### CTA 버튼

1. 추천 매물 보기
2. 위험 체크하기

### 우측 시각 요소

실제 이미지를 사용하지 않아도 된다. CSS 카드와 그래픽 요소로 아래 내용을 표현한다.

* 부동산 매물 카드
* AI 위험 점수 카드
* 안전 / 주의 / 위험 배지
* 분석 완료 느낌의 미니 대시보드 UI

---

## 12. 서비스 소개 섹션

핵심 기능 4개를 카드로 표시한다.

1. AI 전세 위험 분석
2. 보증금 조건 기반 매물 추천
3. 계약 전 질문 자동 생성
4. 특약 예시 제공

### 문구 톤

법률 자문처럼 단정하지 않는다.

사용 가능한 표현:

```text
확인 필요
위험 요소 안내
계약 전 전문가 확인 권장
추가 확인이 필요합니다
```

피해야 할 표현:

```text
사기입니다
무조건 안전합니다
계약해도 됩니다
법적으로 문제없습니다
```

---

## 13. 추천 매물 섹션

FastAPI의 `/api/recommendations` API를 호출한다.

### 필터 UI

다음 입력 UI를 제공한다.

* 지역 검색 input
* 주택 유형 select

  * 전체
  * APT
  * VILLA
  * OFFICETEL
  * SINGLE_MULTI
* 최대 보증금 input
* 추천 조회 버튼

### API 호출 방식

필터 버튼 클릭 시 query string을 조합해서 호출한다.

예시:

```text
/api/recommendations?region=구로구&max_deposit=250000000
```

### 추천 결과 카드 표시 필드

```text
title
address
region
property_type
deposit
area_m2
floor
station_distance_min
risk_level
risk_score
final_score
safety_score
transport_score
budget_score
```

### 표시 방식

* `final_score`가 있으면 “추천 점수”로 표시한다.
* `safety_score`는 “안전 점수”
* `transport_score`는 “교통 점수”
* `budget_score`는 “예산 점수”
* 각 카드에 “상세 위험 분석” 버튼을 제공한다.

---

## 14. 전체 매물 목록 섹션

FastAPI의 `/api/properties` API를 호출한다.

### 요구사항

* 전체 매물 50개 표시
* PC: 3열 카드 그리드
* 태블릿: 2열 카드 그리드
* 모바일: 1열 카드 그리드

### 카드 표시 정보

```text
매물명
주소
보증금
면적
층수
역 거리
위험등급
위험점수
위험태그
```

### 위험등급 배지

```text
안전: 초록
주의: 주황
위험: 빨강
```

### 카드 효과

* hover 시 살짝 위로 올라감
* hover 시 그림자 강화
* “상세 분석 보기” 버튼 제공
* 버튼 클릭 시 `/api/properties/{id}/analysis` 호출

---

## 15. 매물 상세 위험 분석 모달

“상세 분석 보기” 클릭 시 모달 또는 우측 패널로 표시한다.

### 호출 API

```text
GET /api/properties/{id}/analysis
```

### 표시 데이터

```text
title
address
deposit
risk_level
risk_score
risk_tags
summary
risk_reasons
questions_to_broker
special_clause_examples
```

### UI 구성

1. 상단

   * 매물명
   * 주소
   * 위험등급 배지

2. 요약

   * `summary`

3. 위험 사유

   * `risk_reasons` 리스트 카드

4. 중개사에게 물어볼 질문

   * `questions_to_broker` 리스트

5. 특약 예시

   * `special_clause_examples` 강조 박스

### 필수 기능

* 모달 닫기 버튼
* 로딩 상태 처리
* 에러 상태 처리
* 모바일에서도 깨지지 않게 표시

---

## 16. 전세사기 체크리스트 섹션

체크리스트 항목은 다음과 같다.

```text
등기부등본 최신본 확인
소유자와 계약자 일치 확인
근저당권 확인
압류/가압류 확인
신탁등기 확인
임차권등기명령 확인
선순위 임차인 보증금 확인
전세보증금반환보증 가입 가능 여부 확인
건축물대장 확인
공인중개사 등록 및 영업상태 확인
잔금 전 등기부등본 재확인
```

체크리스트는 카드 또는 리스트 UI로 깔끔하게 보여준다.

---

## 17. 문의하기 섹션

### 제목

```text
계약 전, 한 번 더 확인하세요
```

### 설명 문구

```text
전세가드 AI는 매물 데이터를 기반으로 위험 요소를 정리해주지만, 최종 계약 전에는 반드시 전문가와 서류 확인이 필요합니다.
```

### 버튼 2개

1. 카카오톡 오픈채팅 문의

   * 클릭 시 새 창으로 열기

```text
https://open.kakao.com/o/g7TDr4yi
```

2. 메일로 문의하기

   * 클릭 시 mailto 연결

```text
mailto:last5324@gmail.com?subject=전세가드 AI 문의
```

### 문의 폼을 만들 경우

다음 필드를 구성한다.

```text
이름
이메일
문의 내용
메일 앱으로 문의하기 버튼
```

버튼 클릭 시 `mailto` 링크로 제목과 본문을 포함해서 메일 앱을 연다.

주의:

* 실제 서버로 메일 전송 기능은 구현하지 않는다.
* 백엔드 메일 API를 새로 만들지 않는다.

---

## 18. 플로팅 빠른 상담 버튼

화면 우측 하단에 고정한다.

### 버튼 구성

1. 카카오톡 상담
2. 메일 문의
3. 추천 매물 보기

### 동작

카카오톡 상담:

```text
https://open.kakao.com/o/g7TDr4yi
```

메일 문의:

```text
mailto:last5324@gmail.com?subject=전세가드 AI 문의
```

추천 매물 보기:

```text
추천 매물 섹션으로 스크롤 이동
```

### 모바일 동작

모바일에서는 우측 세로 버튼이 아니라 하단 고정 바 형태로 변경한다.

---

## 19. API 연동 요구사항

API 주소는 상수로 분리한다.

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const KAKAO_OPENCHAT_URL = import.meta.env.VITE_KAKAO_OPENCHAT_URL || "https://open.kakao.com/o/g7TDr4yi";
const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL || "last5324@gmail.com";
```

### API 호출 방식

* fetch 사용
* axios는 꼭 필요하지 않으면 추가하지 않는다.

### API 실패 시 메시지

```text
데이터를 불러오지 못했습니다. FastAPI 서버와 Docker DB 실행 상태를 확인해주세요.
```

### 로딩 상태

```text
불러오는 중...
```

또는 skeleton UI를 사용한다.

### 빈 결과 메시지

```text
조건에 맞는 매물이 없습니다. 필터를 조정해주세요.
```

---

## 20. 데이터 포맷 요구사항

### 금액 포맷 함수

다음처럼 보이게 한다.

```text
250000000 → 2억 5,000만원
65000000 → 6,500만원
```

### 주택 유형 한글 변환

```text
APT → 아파트
VILLA → 빌라
OFFICETEL → 오피스텔
SINGLE_MULTI → 단독/다가구
```

### 위험등급 class 분기

```text
안전 → safe
주의 → caution
위험 → danger
```

---

## 21. 권장 파일 구조

현재 Vue 프로젝트 구조를 먼저 확인한 뒤, 필요하면 아래처럼 구성한다.

```text
src/
  api/
    propertyApi.js
  components/
    HeaderNav.vue
    HeroSection.vue
    PropertyCard.vue
    RecommendationSection.vue
    RiskAnalysisModal.vue
    ChecklistSection.vue
    ContactSection.vue
    FloatingContactButtons.vue
  App.vue
  main.js
  style.css 또는 assets/main.css
```

컴포넌트 분리가 너무 복잡해지면 `App.vue` 중심으로 구현해도 된다.

다만 다음 컴포넌트는 분리하는 것을 권장한다.

```text
PropertyCard
RiskAnalysisModal
FloatingContactButtons
```

---

## 22. Vue `.env` 파일 생성

Vue 프로젝트 루트에 `.env` 파일을 만들고 아래 값을 넣는다.

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_KAKAO_OPENCHAT_URL=https://open.kakao.com/o/g7TDr4yi
VITE_CONTACT_EMAIL=last5324@gmail.com
```

---

## 23. 주의사항

다음은 절대 하지 않는다.

* 참고 사이트의 실제 상호 사용
* 참고 사이트의 실제 연락처 사용
* 참고 사이트의 실제 이미지 사용
* 참고 사이트의 실제 문구 복사
* 참고 사이트의 CSS 코드 복사
* “경제공인중개사”, “JPS” 같은 실제 이름 사용
* 실제 매물 사진 사용
* 실제 전화번호 사용

우리 서비스명은 반드시 다음으로 통일한다.

```text
전세가드 AI
```

전세사기 여부를 단정하지 않는다.

피해야 할 표현:

```text
사기입니다
무조건 안전합니다
계약해도 됩니다
법적으로 문제없습니다
```

권장 표현:

```text
위험 요소가 확인됩니다
추가 확인이 필요합니다
계약 전 전문가 확인을 권장합니다
현재 데이터 기준으로 확인이 필요합니다
```

---

## 24. 완료 후 반드시 확인할 것

작업 완료 후 아래 항목을 확인한다.

1. `npm install` 필요 시 실행
2. `npm run dev` 실행 가능
3. `http://localhost:5173` 접속 가능
4. FastAPI 서버가 켜져 있을 때 매물 50개 표시
5. 추천 필터 동작
6. 상세 위험 분석 모달 동작
7. 카카오톡 상담 버튼 클릭 시 아래 링크가 새 창으로 열림

```text
https://open.kakao.com/o/g7TDr4yi
```

8. 메일 문의 버튼 클릭 시 아래 주소로 mailto 실행

```text
last5324@gmail.com
```

9. 모바일 화면에서 카드와 플로팅 버튼이 깨지지 않음
10. 콘솔에 심각한 에러가 없음

---

## 25. 최종 목표

최종 결과물은 다음 흐름이 가능해야 한다.

```text
사용자가 Vue 화면 접속
→ 메인 Hero 확인
→ 추천 조건 입력
→ FastAPI 추천 API 호출
→ 추천 매물 카드 표시
→ 상세 위험 분석 클릭
→ 위험 사유 / 중개사 질문 / 특약 예시 확인
→ 카카오톡 또는 메일 문의 가능
```

포트폴리오 시연 시 한눈에 다음 메시지가 전달되어야 한다.

```text
이 서비스는 단순 부동산 목록 서비스가 아니라,
전세 계약 전 위험 요소를 확인하고
안전한 매물 선택을 돕는 AI 기반 전세 위험 분석 서비스다.
```
