import os
import sys
import json
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
from datetime import datetime

def get_corp_code(api_key, ticker):
    """종목코드(6자리)를 OpenDART corp_code(8자리)로 변환"""
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        with zf.open('CORPCODE.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for list_tag in root.findall('list'):
                if list_tag.find('stock_code').text == ticker:
                    return list_tag.find('corp_code').text
    return None

def get_financial_data(api_key, corp_code, year=None, reprt_code='11011'):
    """단일회사 주요계정 조회 (11011: 사업보고서)"""
    if year is None:
        year = str(datetime.now().year - 1)
    url = f"https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={api_key}&corp_code={corp_code}&bsns_year={year}&reprt_code={reprt_code}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Ticker required"}))
        sys.exit(1)

    ticker = sys.argv[1]
    api_key = os.getenv("OPENDART_API_KEY")
    
    if not api_key:
        print(json.dumps({"error": "OPENDART_API_KEY environment variable not set"}))
        sys.exit(1)

    try:
        corp_code = get_corp_code(api_key, ticker)
        if not corp_code:
            print(json.dumps({"error": f"Could not find corp_code for ticker {ticker}"}))
            sys.exit(1)
            
        data = get_financial_data(api_key, corp_code)
        if data and data.get('status') == '000':
            # 필요한 지표만 필터링 (매출액, 영업이익, 당기순이익 등)
            results = {}
            for item in data.get('list', []):
                if item['account_nm'] in ['매출액', '영업이익', '당기순이익', '자산총계', '부채총계', '자본총계']:
                    results[item['account_nm']] = {
                        "amount": item['thstrm_amount'],
                        "unit": "KRW"
                    }
            print(json.dumps({"ticker": ticker, "corp_code": corp_code, "data": results}, ensure_ascii=False))
        else:
            print(json.dumps({"error": "API request failed", "details": data}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
