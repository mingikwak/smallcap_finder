# 🔍 Hidden Small Finder

> OpenDART API와 웹 검색을 결합하여, KOSPI 대형주 대비 저평가된 고퀄리티 스몰캡(중소형주) Top 3를 발굴하는 AI 기반 수석 애널리스트 스킬

---

## 개요

Hidden Small Finder는 Claude AI의 스킬(Skill) 형태로 구현된 **KOSPI 스몰캡 발굴 시스템**입니다.  
사용자가 특정 산업군을 입력하면, 해당 섹터의 대형 우량주를 벤치마크로 설정하고,  
이와 비교해 저평가된 중소형 우량주 Top 3를 **장기 가치 투자(Value Track)**와 **단기 모멘텀 투자(Momentum Track)** 두 트랙으로 분류하여 HTML 리포트로 제시합니다.

---

## 분석 로직 (DART & Web Hybrid)

```
[Step 1] 벤치마크 및 후보군 선정
         └─ 웹 검색으로 대형주(시총 1조↑) / 중소형주(시총 1조↓) 종목 코드 확보

[Step 2] 공식 재무 데이터 추출
         └─ OpenDART API → 매출액, 영업이익, 당기순이익, 자본총계 수집

[Step 3] 종합 밸류에이션 & 기술적 분석
         ├─ OPM, ROE, PBR, PER 일괄 산출 (DART 재무 + 웹 검색 시가총액 결합)
         ├─ 대형주 평균(벤치마크) 대비 저평가 여부 판정
         └─ 120일 이동평균선(120MA) 위치 확인 (웹 검색)

[Step 4] HTML 마스터 리포트 생성
         ├─ Value Track Top 3  : PBR·ROE 기준 저평가 종목 (장기 가치 투자)
         └─ Momentum Track Top 3 : 120MA 돌파·수급 호전 종목 (단기 추세)
```

---

## 데이터 소스

| 데이터 항목 | 소스 |
|---|---|
| 매출액 · 영업이익 · 당기순이익 · 자본총계 | OpenDART API (공시 기반 재무제표) |
| OPM · ROE · PBR · PER 산출 | DART 재무 + 웹 검색 시가총액 결합 |
| 현재 주가 · 시가총액 | 웹 검색 (네이버 금융 등) |
| 120일 이동평균선 | 웹 검색 |

---

## 출력 리포트 구성

1. **DART 검증 벤치마크 요약** — 대형주 재무 지표 테이블 (시가총액, 자본총계, 영업이익, ROE, PBR, PER, 120MA 위치)
2. **섹터 핵심 분석 포인트** — 섹터별 3대 핵심 이슈
3. **Value Track Top 3** — PBR·ROE 기준 저평가 종목 (장기 가치 투자)
4. **Momentum Track Top 3** — 120MA 돌파·수급 호전 종목 (단기 추세)
5. **산업 전망 및 투자 결론** — 수석 애널리스트의 향후 6~12개월 총평 및 전략

---

## 사용 예시

```
사용자: 반도체 산업 스몰캡 찾아줘
  → 반도체 섹터 대형주 벤치마크 설정
  → OpenDART API로 공식 재무 데이터 추출
  → OPM·ROE·PBR·PER 산출 및 저평가 판정
  → Value / Momentum Top 3 HTML 리포트 출력
```

---

## 설치 및 설정

### 1. OpenDART API 키 발급
[OpenDART](https://opendart.fss.or.kr/)에서 API 키를 발급받아 환경 변수에 설정합니다.

```bash
export OPENDART_API_KEY=your_api_key_here
```

### 2. 부속 스크립트 준비
`scripts/fetch_dart_data.py` 파일이 없는 경우, `SKILL.md` 내 소스 코드를 참고하여 생성합니다.

```bash
python scripts/fetch_dart_data.py [종목코드6자리]
```

---

## 주의 사항

- 본 도구의 분석 결과는 **투자 참고용**이며, 실제 투자 손실에 대한 책임을 지지 않습니다.
- Data Source: OpenDART (FSS), Google Market Search


---

## 라이선스

MIT
