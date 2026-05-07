import os
import sys
import json
import datetime
import subprocess

# SKILL.md에서 정의된 V5.5 Masterpiece HTML 템플릿
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sector_name} 산업 통합 투자 마스터 리포트 (V5.5 Masterpiece)</title>
    <style>
        :root {{
            --primary: #0f2027;
            --secondary: #203a43;
            --accent: #2c5364;
            --value: #d35400;
            --momentum: #16a085;
            --dart-blue: #004a99;
        }}
        body {{ font-family: 'Pretendard', -apple-system, sans-serif; line-height: 1.8; color: #333; max-width: 1200px; margin: 0 auto; padding: 40px; background-color: #f1f3f5; }}
        .master-wrap {{ background: white; padding: 60px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); border-top: 10px solid var(--primary); }}
        header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 40px; margin-bottom: 50px; }}
        h1 {{ font-size: 2.8em; color: var(--primary); margin: 0; letter-spacing: -1px; }}
        .analyst-stamp {{ color: #888; margin-top: 15px; font-weight: 500; font-size: 1.1em; }}
        .dart-badge {{ display: inline-block; background: var(--dart-blue); color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.8em; margin-bottom: 10px; font-weight: bold; }}
        .section-title {{ font-size: 1.8em; font-weight: 800; color: var(--primary); margin: 60px 0 25px; border-left: 8px solid var(--primary); padding-left: 20px; }}
        .table-container {{ overflow-x: auto; margin-bottom: 40px; }}
        table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; }}
        th {{ background: #f8f9fa; padding: 18px; border-bottom: 2px solid #dee2e6; font-size: 0.9em; color: #444; }}
        td {{ padding: 18px; border-bottom: 1px solid #eee; text-align: center; font-size: 0.9em; }}
        .avg-row {{ background: #fff9e6; font-weight: bold; color: var(--value); }}
        .focus-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 50px; }}
        .focus-item {{ background: #f8fbff; border: 1px solid #e1e8f0; padding: 25px; border-radius: 12px; }}
        .focus-item h4 {{ color: #004a99; margin-top: 0; margin-bottom: 12px; font-size: 1.15em; }}
        .recommend-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 60px; }}
        .card {{ background: #fff; border: 1px solid #eee; border-radius: 15px; padding: 30px; position: relative; transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }}
        .card:hover {{ transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }}
        .card.value-card {{ border-top: 5px solid var(--value); }}
        .card.momentum-card {{ border-top: 5px solid var(--momentum); }}
        .card .name {{ font-size: 1.45em; font-weight: 800; display: block; margin-bottom: 5px; }}
        .card .ticker {{ font-size: 0.8em; color: #999; margin-bottom: 10px; display: block; }}
        .card .hashtags {{ font-size: 0.85em; color: var(--accent); font-weight: 600; margin-bottom: 15px; display: block; }}
        .card .metrics {{ font-size: 0.88em; margin: 15px 0; color: #444; background: #f9f9f9; padding: 15px; border-radius: 8px; line-height: 1.7; }}
        .card .opinion {{ font-size: 0.88em; border-top: 1px solid #f0f0f0; padding-top: 15px; font-style: italic; color: #666; line-height: 1.6; }}
        .market-cap-badge {{ background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; color: #666; font-weight: normal; vertical-align: middle; }}
        .outlook-section {{ background: #1c2833; color: #f4f6f7; padding: 45px; border-radius: 15px; margin-top: 60px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .outlook-title {{ color: #1abc9c; font-size: 1.8em; font-weight: 800; border-bottom: 2px solid #1abc9c; padding-bottom: 15px; margin-bottom: 25px; }}
        .outlook-reasons h4 {{ color: #f39c12; margin-bottom: 15px; font-size: 1.25em; display: flex; align-items: center; }}
        .outlook-reasons ul {{ padding-left: 20px; font-size: 1em; color: #bdc3c7; line-height: 1.8; }}
        .outlook-reasons b {{ color: #fff; }}
        .investment-conclusion {{ background: rgba(26, 188, 156, 0.1); border-left: 6px solid #1abc9c; padding: 25px; margin-top: 35px; border-radius: 0 10px 10px 0; }}
        .investment-conclusion h4 {{ color: #1abc9c; margin-top: 0; margin-bottom: 12px; font-size: 1.35em; }}
        footer {{ text-align: center; color: #aaa; font-size: 0.85em; margin-top: 80px; padding-bottom: 40px; border-top: 1px solid #eee; padding-top: 30px; }}
    </style>
</head>
<body>
    <div class="master-wrap">
        <header>
            <div class="dart-badge">VERIFIED BY OPENDART API</div>
            <h1>{sector_name} 산업 통합 투자 마스터 리포트</h1>
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
                    {benchmark_rows}
                    <tr class="avg-row">
                        <td colspan="2">벤치마크 평균 (Benchmark Avg)</td>
                        <td>{avg_market_cap}</td>
                        <td>{avg_equity}</td>
                        <td>{avg_revenue}</td>
                        <td>{avg_profit}</td>
                        <td>{avg_pbr}</td>
                        <td>{avg_roe}</td>
                        <td>{avg_per}</td>
                        <td>-</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="section-title">2. {sector_name} 섹터 핵심 분석 포인트</div>
        <div class="focus-grid">
            {focus_points}
        </div>
        <div class="section-title"><span style="color: var(--value);">3. Value Track:</span> 장기 가치 투자 Top 3 (Small-cap Only)</div>
        <div class="recommend-grid">
            {value_cards}
        </div>
        <div class="section-title"><span style="color: var(--momentum);">4. Momentum Track:</span> 단기 추세 매매 Top 3 (Small-cap Only)</div>
        <div class="recommend-grid">
            {momentum_cards}
        </div>
        <div class="outlook-section">
            <div class="outlook-title">{sector_name} 섹터 향후 6~12개월 전망: {investment_opinion}</div>
            <div class="outlook-reasons">
                <h4>{outlook_header}</h4>
                <ul>{outlook_reasons}</ul>
            </div>
            <div class="investment-conclusion">
                <h4>🎯 수석 애널리스트 최종 투자 결론</h4>
                <p>{final_conclusion}</p>
            </div>
        </div>
        <footer>
            "본 분석은 투자 참고용이며 투자 손실에 대한 책임을 지지 않음"<br>
            Data Source: OpenDART (FSS), Google Market Search | Generated by Gemini CLI (V5.5 Masterpiece Format)
        </footer>
    </div>
</body>
</html>
"""

class HiddenSmallFinderAutomation:
    def __init__(self, sector):
        self.sector = sector
        self.date_str = datetime.datetime.now().strftime("%y%m%d")
        self.api_key = os.getenv("OPENDART_API_KEY")

    def fetch_dart_data(self, ticker):
        """scripts/fetch_dart_data.py를 사용하여 데이터를 가져옵니다."""
        try:
            result = subprocess.run(
                ["python3", "scripts/fetch_dart_data.py", ticker],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def format_benchmark_row(self, company_data):
        """벤치마크 테이블의 행을 생성합니다."""
        name = company_data.get('name', 'Unknown')
        ticker = company_data.get('ticker', '000000')
        data = company_data.get('data', {})
        
        cap = company_data.get('market_cap', 0)
        equity = float(data.get('자본총계', {}).get('amount', 0)) / 1e12
        sales = float(data.get('매출액', {}).get('amount', 0)) / 1e12
        op = float(data.get('영업이익', {}).get('amount', 0)) / 1e12
        pbr = company_data.get('pbr', 0.0)
        roe = company_data.get('roe', 0.0)
        per = company_data.get('per', 0.0)
        ma120 = company_data.get('ma120', 'N/A')

        return f"""
        <tr>
            <td>{name} ({ticker})</td>
            <td>{cap:.1f}</td>
            <td>{equity:.2f}</td>
            <td>{sales:.2f}</td>
            <td>{op:.2f}</td>
            <td>{pbr:.2f}</td>
            <td>{roe:.1f}%</td>
            <td>{per:.1f}</td>
            <td>{ma120}</td>
        </tr>
        """

    def format_card(self, company_data, card_type="value"):
        """종목 추천 카드를 생성합니다."""
        name = company_data.get('name', 'Unknown')
        ticker = company_data.get('ticker', '000000')
        hashtags = company_data.get('hashtags', '#가치 #저평가')
        metrics = company_data.get('metrics_summary', 'PBR 0.0배 | PER 0.0배')
        opinion = company_data.get('opinion', '안정적인 재무구조와 성장성이 돋보임.')
        
        css_class = "value-card" if card_type == "value" else "momentum-card"
        
        return f"""
        <div class="card {css_class}">
            <span class="name">{name} <span class="market-cap-badge">{company_data.get('market_cap_str', '스몰캡')}</span></span>
            <span class="ticker">{ticker}</span>
            <span class="hashtags">{hashtags}</span>
            <div class="metrics">
                {metrics}
            </div>
            <div class="opinion">
                {opinion}
            </div>
        </div>
        """

    def generate_report(self, results):
        """데이터를 템플릿에 주입하여 HTML 파일을 생성합니다."""
        benchmark_rows = "".join([self.format_benchmark_row(c) for c in results.get('benchmarks', [])])
        
        # 벤치마크 평균 계산
        avg_data = results.get('benchmark_avg', {})
        
        focus_points = "".join([
            f'<div class="focus-item"><h4>{p["title"]}</h4><p>{p["content"]}</p></div>'
            for p in results.get('focus_points', [])
        ])
        
        value_cards = "".join([self.format_card(c, "value") for c in results.get('value_track', [])])
        momentum_cards = "".join([self.format_card(c, "momentum") for c in results.get('momentum_track', [])])
        
        outlook_reasons = "".join([f'<li><b>{r["title"]}:</b> {r["content"]}</li>' for r in results.get('outlook_reasons', [])])

        html_content = HTML_TEMPLATE.format(
            sector_name=self.sector,
            benchmark_rows=benchmark_rows,
            avg_market_cap=avg_data.get('market_cap', '0.0'),
            avg_equity=avg_data.get('equity', '0.00'),
            avg_revenue=avg_data.get('revenue', '0.00'),
            avg_profit=avg_data.get('profit', '0.00'),
            avg_pbr=avg_data.get('pbr', '0.00'),
            avg_roe=avg_data.get('roe', '0.0%'),
            avg_per=avg_data.get('per', '0.0'),
            focus_points=focus_points,
            value_cards=value_cards,
            momentum_cards=momentum_cards,
            outlook_reasons=outlook_reasons,
            investment_opinion=results.get('investment_opinion', '[Overweight / 비중확대]'),
            outlook_header=results.get('outlook_header', '📢 섹터 비중 확대의 상세 사유'),
            final_conclusion=results.get('final_conclusion', '비중 확대 의견을 유지함.')
        )

        # 폴더 생성 및 저장
        dir_path = self.sector.lower().replace(" ", "_")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        file_name = f"{dir_path}/{dir_path}_report_{self.date_str}.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Report generated: {file_name}")
        return file_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hidden_small_finder.py [Sector]")
        sys.exit(1)
        
    sector = sys.argv[1]
    automation = HiddenSmallFinderAutomation(sector)
    
    # 예시 데이터
    mock_results = {
        "benchmarks": [
            {
                "name": "삼성전자", "ticker": "005930", "market_cap": 450.0, "pbr": 1.45, "roe": 12.5, "per": 15.2, "ma120": "정배열",
                "data": {"자본총계": {"amount": "300000000000000"}, "매출액": {"amount": "250000000000000"}, "영업이익": {"amount": "30000000000000"}}
            }
        ],
        "benchmark_avg": {
            "market_cap": "450.0", "equity": "300.00", "revenue": "250.00", "profit": "30.00", "pbr": "1.45", "roe": "12.5%", "per": "15.2"
        },
        "focus_points": [
            {"title": "매크로 환경", "content": "금리 인하 기대감으로 인한 유동성 공급 확대"},
            {"title": "산업 트렌드", "content": "AI 반도체 수요 폭증으로 인한 밸류체인 확장"}
        ],
        "value_track": [
            {
                "name": "유망중소A", "ticker": "999001", "market_cap_str": "3,500억", 
                "hashtags": "#저PBR #현금부자", "metrics_summary": "PBR 0.45배 | PER 6.2배",
                "opinion": "순현금 자산이 시총의 50%를 상회하며 본업의 이익 체력이 견고함."
            }
        ],
        "momentum_track": [
            {
                "name": "성장주B", "ticker": "999002", "market_cap_str": "5,200억", 
                "hashtags": "#신고가 #거래량급증", "metrics_summary": "120MA 돌파 | 외인 매수세",
                "opinion": "주요 고객사향 신규 수주 모멘텀이 실적으로 가시화되는 단계."
            }
        ],
        "investment_opinion": "[Overweight / 비중확대]",
        "outlook_header": "📢 섹터 비중 확대의 상세 사유",
        "outlook_reasons": [
            {"title": "수요 회복", "content": "글로벌 IT 가전 수요의 점진적 회복세 확인"},
            {"title": "공급 조절", "content": "메이저 업체들의 감산 효과로 인한 판가 상승"}
        ],
        "final_conclusion": "대형주 대비 밸류에이션 매력이 높은 중소형주 위주의 선별적 접근이 유효한 시점임."
    }
    
    automation.generate_report(mock_results)
