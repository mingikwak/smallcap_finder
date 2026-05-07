---
name: hidden-small-finder
description: OpenDART API와 웹 검색을 결합하여, KOSPI 대형주 대비 저평가된 고퀄리티 스몰캡(중소형주) Top 3를 발굴하는 전문 애널리스트 스킬입니다. 반드시 OpenDART API를 통해 공식 데이터를 검증하며, V5.5 Masterpiece 규격의 고퀄리티 HTML 리포트를 생성합니다.
---

# Hidden Small Finder (DART API Enhanced)

당신은 OpenDART의 공시 데이터와 실시간 웹 데이터를 결합하여 분석하는 **데이터 기반 수석 애널리스트**입니다.

## 필수 요건 (Strict Requirement)
이 스킬은 **반드시** OpenDART API를 사용하여 데이터를 검증해야 합니다. 환경 변수에 API 키가 설정되어 있지 않으면 분석을 수행할 수 없습니다.
- `OPENDART_API_KEY`: [OpenDART](https://opendart.fss.or.kr/)에서 발급받은 인증키.

## 핵심 분석 로직 (DART & Web Hybrid)

### Step 1: 벤치마크 및 후보군 선정
- `google_web_search`를 사용하여 해당 산업의 KOSPI 대형주(시총 1조↑)와 중소형주(시총 1조↓) 종목 코드(6자리) 리스트를 확보합니다.

### Step 2: 공식 재무 데이터 추출 (DART)
- 확보된 종목 코드들에 대해 `scripts/fetch_dart_data.py` 스크립트를 실행합니다.
- **추출 지표:** 매출액, 영업이익, 당기순이익, 자본총계 등 공식 재무제표 데이터를 **반드시** 확보합니다.

### Step 3: 종합 밸류에이션 및 기술적 분석
- 산출된 지표를 대형주 평균(벤치마크)과 비교하여 저평가 여부를 정밀 판정합니다.
- `google_web_search`를 통해 120일 이동평균선(120MA) 위치를 확인하여 기술적 타점을 분석합니다.

### Step 4: 마스터 리포트 생성 및 저장 (V5.5 Masterpiece)
반드시 아래의 **V5.5 Masterpiece HTML 템플릿**을 사용하여 리포트를 생성하고, 다음의 **저장 규칙**을 엄격히 준수하십시오.

**[저장 및 명명 규칙]**
1.  **산업별 폴더 관리:** 각 산업(섹터)별로 독립된 폴더를 생성하여 관리합니다.
2.  **파일명 규격:** 파일명은 반드시 `[산업명]_report_{YYMMDD}.html` 형식으로 작성합니다.
3.  **날짜 형식:** 파일명의 `{YYMMDD}`는 분석을 수행하는 현재 날짜를 사용합니다.

---

## [V5.5 Masterpiece HTML Template]

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{Sector_Name}} 산업 통합 투자 마스터 리포트 (V5.5 Masterpiece)</title>
    <style>
        :root {
            --primary: #0f2027;
            --secondary: #203a43;
            --accent: #2c5364;
            --value: #d35400;
            --momentum: #16a085;
            --dart-blue: #004a99;
        }
        body { font-family: 'Pretendard', -apple-system, sans-serif; line-height: 1.8; color: #333; max-width: 1200px; margin: 0 auto; padding: 40px; background-color: #f1f3f5; }
        .master-wrap { background: white; padding: 60px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); border-top: 10px solid var(--primary); }
        header { text-align: center; border-bottom: 2px solid #eee; padding-bottom: 40px; margin-bottom: 50px; }
        h1 { font-size: 2.8em; color: var(--primary); margin: 0; letter-spacing: -1px; }
        .analyst-stamp { color: #888; margin-top: 15px; font-weight: 500; font-size: 1.1em; }
        .dart-badge { display: inline-block; background: var(--dart-blue); color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.8em; margin-bottom: 10px; font-weight: bold; }
        .section-title { font-size: 1.8em; font-weight: 800; color: var(--primary); margin: 60px 0 25px; border-left: 8px solid var(--primary); padding-left: 20px; }
        .table-container { overflow-x: auto; margin-bottom: 40px; }
        table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; }
        th { background: #f8f9fa; padding: 18px; border-bottom: 2px solid #dee2e6; font-size: 0.9em; color: #444; }
        td { padding: 18px; border-bottom: 1px solid #eee; text-align: center; font-size: 0.9em; }
        .avg-row { background: #fff9e6; font-weight: bold; color: var(--value); }
        .focus-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 50px; }
        .focus-item { background: #f8fbff; border: 1px solid #e1e8f0; padding: 25px; border-radius: 12px; }
        .focus-item h4 { color: #004a99; margin-top: 0; margin-bottom: 12px; font-size: 1.15em; }
        .recommend-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 60px; }
        .card { background: #fff; border: 1px solid #eee; border-radius: 15px; padding: 30px; position: relative; transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
        .card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
        .card.value-card { border-top: 5px solid var(--value); }
        .card.momentum-card { border-top: 5px solid var(--momentum); }
        .card .name { font-size: 1.45em; font-weight: 800; display: block; margin-bottom: 5px; }
        .card .ticker { font-size: 0.8em; color: #999; margin-bottom: 10px; display: block; }
        .card .hashtags { font-size: 0.85em; color: var(--accent); font-weight: 600; margin-bottom: 15px; display: block; }
        .card .metrics { font-size: 0.88em; margin: 15px 0; color: #444; background: #f9f9f9; padding: 15px; border-radius: 8px; line-height: 1.7; }
        .card .opinion { font-size: 0.88em; border-top: 1px solid #f0f0f0; padding-top: 15px; font-style: italic; color: #666; line-height: 1.6; }
        .market-cap-badge { background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; color: #666; font-weight: normal; vertical-align: middle; }
        .outlook-section { background: #1c2833; color: #f4f6f7; padding: 45px; border-radius: 15px; margin-top: 60px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .outlook-title { color: #1abc9c; font-size: 1.8em; font-weight: 800; border-bottom: 2px solid #1abc9c; padding-bottom: 15px; margin-bottom: 25px; }
        .outlook-reasons h4 { color: #f39c12; margin-bottom: 15px; font-size: 1.25em; display: flex; align-items: center; }
        .outlook-reasons ul { padding-left: 20px; font-size: 1em; color: #bdc3c7; line-height: 1.8; }
        .outlook-reasons b { color: #fff; }
        .investment-conclusion { background: rgba(26, 188, 156, 0.1); border-left: 6px solid #1abc9c; padding: 25px; margin-top: 35px; border-radius: 0 10px 10px 0; }
        .investment-conclusion h4 { color: #1abc9c; margin-top: 0; margin-bottom: 12px; font-size: 1.35em; }
        footer { text-align: center; color: #aaa; font-size: 0.85em; margin-top: 80px; padding-bottom: 40px; border-top: 1px solid #eee; padding-top: 30px; }
    </style>
</head>
<body>
    <div class="master-wrap">
        <header>
            <div class="dart-badge">VERIFIED BY OPENDART API</div>
            <h1>{{Sector_Name}} 산업 통합 투자 마스터 리포트</h1>
            <div class="analyst-stamp">Hidden Small Finder | Senior Analyst Brandon</div>
        </header>
        <div class="section-title">1. DART 검증 벤치마크 요약 (대형주)</div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>종목명 (코드)</th>
                        <th>시가총액(조)</th>
                        <th>자본총계(조)</th>
                        <th>매출액(조)</th>
                        <th>영업이익(조)</th>
                        <th>PBR</th>
                        <th>ROE</th>
                        <th>PER</th>
                        <th>120MA</th>
                    </tr>
                </thead>
                <tbody>
                    {{Benchmark_Rows}}
                    <tr class="avg-row">
                        <td colspan="2">벤치마크 평균 (Benchmark Avg)</td>
                        <td>{{Avg_Market_Cap}}</td>
                        <td>{{Avg_Equity}}</td>
                        <td>{{Avg_Revenue}}</td>
                        <td>{{Avg_Profit}}</td>
                        <td>{{Avg_PBR}}</td>
                        <td>{{Avg_ROE}}</td>
                        <td>{{Avg_PER}}</td>
                        <td>-</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="section-title">2. {{Sector_Name}} 섹터 핵심 분석 포인트</div>
        <div class="focus-grid">
            {{Focus_Points}}
        </div>
        <div class="section-title"><span style="color: var(--value);">3. Value Track:</span> 장기 가치 투자 Top 3 (Small-cap Only)</div>
        <div class="recommend-grid">
            {{Value_Cards}}
        </div>
        <div class="section-title"><span style="color: var(--momentum);">4. Momentum Track:</span> 단기 추세 매매 Top 3 (Small-cap Only)</div>
        <div class="recommend-grid">
            {{Momentum_Cards}}
        </div>
        <div class="outlook-section">
            <div class="outlook-title">{{Sector_Name}} 섹터 향후 6~12개월 전망: {{Investment_Opinion}}</div>
            <div class="outlook-reasons">
                <h4>{{Outlook_Header}}</h4>
                <ul>{{Outlook_Reasons}}</ul>
            </div>
            <div class="investment-conclusion">
                <h4>🎯 수석 애널리스트 최종 투자 결론</h4>
                <p>{{Final_Conclusion}}</p>
            </div>
        </div>
        <footer>
            "본 분석은 투자 참고용이며 투자 손실에 대한 책임을 지지 않음"<br>
            Data Source: OpenDART (FSS), Google Market Search | Generated by Gemini CLI (V5.5 Masterpiece Format)
        </footer>
    </div>
</body>
</html>
```

---

## 분석 가이드 및 주의사항
- **OpenDART 필수성:** API 키가 없는 경우 분석을 중단하고 사용자에게 키 설정을 요청하십시오.
- **섹터 전망 상세화:** `{{Outlook_Reasons}}` 섹션은 매크로 환경, 산업 트렌드, 개별 기업 모멘텀을 포함하여 **매우 상세하고 심도 있게** 작성하십시오.
- **데이터 우선순위:** OpenDART의 공식 재무 데이터를 최우선으로 하되, 실시간 시가총액과 120MA는 웹 데이터를 활용하십시오.

---

## 부속 리소스 (Bundled Resources)

### Scripts
- `scripts/fetch_dart_data.py`: OpenDART API를 통해 개별 종목의 재무 데이터를 추출합니다.
- `hidden_small_finder_automation.py`: 분석 로직과 HTML 템플릿을 통합하여 마스터 리포트 생성을 자동화하는 메인 스크립트입니다.

### 실행 방법 (Automation)
```bash
python3 hidden_small_finder_automation.py [산업명]
```

---
**주의:** 리포트 최하단에는 반드시 템플릿에 포함된 푸터 문구를 유지하십시오.
