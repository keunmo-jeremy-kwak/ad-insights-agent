"""
Advanced Ad Insights Agent with Multiple Recipients
여러 슬랙 채널과 이메일 주소로 동시 전송
"""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MultiRecipientAdInsightsAgent:
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        
        # 검색 쿼리 정의
        self.search_queries = [
            # 시장 트렌드
            "디지털 광고 시장 트렌드 2025",
            "performance marketing 최신 동향",
            "retail media 성장",
            "쿠키리스 광고 대응",
            
            # 플랫폼 동향
            "네이버 광고 신규 상품",
            "카카오 광고 업데이트",
            "구글 애즈 변경사항",
            "메타 광고 뉴스",
            "틱톡 광고 한국",
            
            # 기술 트렌드
            "AI 광고 자동화",
            "생성형 AI 마케팅 활용",
            "광고 측정 attribution",
            
            # 규제
            "개인정보보호 광고 규제",
            "온라인 플랫폼 법안",
        ]
        
        self.results = []
    
    def search_with_claude(self, query: str) -> Dict:
        """Claude API를 사용하여 웹 검색 및 요약"""
        
        prompt = f"""
오늘 날짜는 {self.today}입니다.

다음 주제에 대해 최신 정보를 웹에서 검색하고 핵심 인사이트를 정리해주세요:
"{query}"

다음 형식으로 JSON 응답해주세요:
{{
    "query": "검색어",
    "key_findings": ["핵심 발견사항 1", "핵심 발견사항 2", "핵심 발견사항 3"],
    "summary": "2-3문장 요약",
    "impact": "광고사업개발 담당자에게 미치는 영향",
    "actionable_insight": "실행 가능한 인사이트",
    "sources": ["출처1", "출처2"]
}}

검색 결과가 없거나 관련 정보가 없다면 해당 내용을 명시해주세요.
"""
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 2000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            
            if response.status_code == 200:
                content = response.json()['content'][0]['text']
                try:
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0].strip()
                    
                    result = json.loads(content)
                    result['timestamp'] = self.today
                    return result
                except json.JSONDecodeError:
                    print(f"JSON 파싱 실패: {query}")
                    return self._create_fallback_result(query, content)
            else:
                print(f"API 오류 ({query}): {response.status_code}")
                return None
                
        except Exception as e:
            print(f"검색 오류 ({query}): {e}")
            return None
    
    def _create_fallback_result(self, query: str, content: str) -> Dict:
        """JSON 파싱 실패시 대체 결과 생성"""
        return {
            "query": query,
            "key_findings": [content[:200]],
            "summary": content[:300],
            "impact": "상세 분석 필요",
            "actionable_insight": "추가 조사 권장",
            "sources": [],
            "timestamp": self.today
        }
    
    def collect_all_insights(self):
        """모든 쿼리에 대해 인사이트 수집"""
        print(f"\n🚀 {self.today} 광고 시장 인사이트 수집 시작\n")
        print(f"총 {len(self.search_queries)}개 주제 검색 예정...\n")
        
        for i, query in enumerate(self.search_queries, 1):
            print(f"[{i}/{len(self.search_queries)}] 🔍 검색 중: {query}")
            
            result = self.search_with_claude(query)
            if result:
                self.results.append(result)
                print(f"   ✅ 완료\n")
            else:
                print(f"   ⚠️  결과 없음\n")
        
        print(f"✨ 수집 완료! 총 {len(self.results)}개 인사이트 확보\n")
    
    def generate_comprehensive_report(self) -> str:
        """포괄적인 리포트 생성"""
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║         🎯 광고 시장 Daily Brief - {self.today}         ║
╚══════════════════════════════════════════════════════════╝

안녕하세요! 오늘의 광고 시장 핵심 인사이트를 정리했습니다.

"""
        
        categories = {
            "🔥 오늘의 핵심 트렌드": [],
            "📱 주요 플랫폼 동향": [],
            "🤖 기술 & 혁신": [],
            "⚖️ 규제 & 정책": []
        }
        
        for result in self.results:
            query = result['query'].lower()
            
            if any(k in query for k in ['트렌드', '시장', '성장', 'retail']):
                categories["🔥 오늘의 핵심 트렌드"].append(result)
            elif any(k in query for k in ['네이버', '카카오', '구글', '메타', '틱톡']):
                categories["📱 주요 플랫폼 동향"].append(result)
            elif any(k in query for k in ['ai', '기술', '자동화', '측정']):
                categories["🤖 기술 & 혁신"].append(result)
            elif any(k in query for k in ['규제', '법', '정책', '보호']):
                categories["⚖️ 규제 & 정책"].append(result)
        
        for category, items in categories.items():
            if items:
                report += f"\n{'='*60}\n"
                report += f"{category}\n"
                report += f"{'='*60}\n\n"
                
                for item in items:
                    report += f"📌 {item['query']}\n"
                    report += f"   {item['summary']}\n\n"
                    
                    if item.get('key_findings'):
                        report += "   핵심 포인트:\n"
                        for finding in item['key_findings'][:3]:
                            report += f"   • {finding}\n"
                    
                    if item.get('actionable_insight'):
                        report += f"\n   💡 액션 아이템: {item['actionable_insight']}\n"
                    
                    report += "\n" + "-"*60 + "\n\n"
        
        report += f"\n{'='*60}\n"
        report += "📊 오늘의 종합 인사이트\n"
        report += f"{'='*60}\n\n"
        report += f"✅ 수집된 인사이트: {len(self.results)}건\n"
        report += f"📅 다음 브리핑: {self._get_next_day()}\n\n"
        
        report += """
💬 피드백이나 추가로 모니터링하고 싶은 주제가 있다면 알려주세요!

---
Powered by Advanced Ad Insights Agent 🤖
"""
        
        return report
    
    def _get_next_day(self) -> str:
        """다음 날짜 반환"""
        from datetime import datetime, timedelta
        next_day = datetime.now() + timedelta(days=1)
        return next_day.strftime("%Y-%m-%d")
    
    def send_to_multiple_slack(self, report: str, webhook_urls: List[str]):
        """여러 슬랙 채널로 전송"""
        print(f"\n📤 {len(webhook_urls)}개 슬랙 채널로 전송 중...")
        
        success_count = 0
        for i, webhook_url in enumerate(webhook_urls, 1):
            if not webhook_url or webhook_url.strip() == '':
                continue
                
            try:
                blocks = [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🎯 광고 시장 Daily Brief - {self.today}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{len(self.results)}개*의 핵심 인사이트를 수집했습니다!"
                        }
                    },
                    {
                        "type": "divider"
                    }
                ]
                
                for j, result in enumerate(self.results[:5], 1):
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{j}. {result['query']}*\n{result['summary'][:200]}..."
                        }
                    })
                
                blocks.append({
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "📧 전체 리포트는 이메일을 확인해주세요!"
                        }
                    ]
                })
                
                payload = {
                    "blocks": blocks,
                    "text": f"광고 시장 Daily Brief - {self.today}"
                }
                
                response = requests.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    print(f"   [{i}/{len(webhook_urls)}] ✅ 슬랙 채널 #{i} 전송 완료!")
                    success_count += 1
                else:
                    print(f"   [{i}/{len(webhook_urls)}] ❌ 슬랙 채널 #{i} 전송 실패: {response.status_code}")
                    
            except Exception as e:
                print(f"   [{i}/{len(webhook_urls)}] ❌ 슬랙 채널 #{i} 전송 오류: {e}")
        
        print(f"✅ 슬랙 전송 완료: {success_count}/{len(webhook_urls)}개 성공\n")
    
    def send_to_multiple_emails(self, report: str, email_configs: List[Dict]):
        """여러 이메일 주소로 전송"""
        print(f"\n📧 {len(email_configs)}개 이메일 주소로 전송 중...")
        
        success_count = 0
        for i, config in enumerate(email_configs, 1):
            if not config.get('to_email'):
                continue
                
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"📊 광고 시장 Daily Brief - {self.today}"
                msg['From'] = config['from_email']
                msg['To'] = config['to_email']
                
                html_report = self._convert_to_html(report)
                
                text_part = MIMEText(report, 'plain', 'utf-8')
                html_part = MIMEText(html_report, 'html', 'utf-8')
                
                msg.attach(text_part)
                msg.attach(html_part)
                
                with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                    server.starttls()
                    server.login(config['from_email'], config['password'])
                    server.send_message(msg)
                
                print(f"   [{i}/{len(email_configs)}] ✅ {config['to_email']} 전송 완료!")
                success_count += 1
                
            except Exception as e:
                print(f"   [{i}/{len(email_configs)}] ❌ {config.get('to_email', 'unknown')} 전송 오류: {e}")
        
        print(f"✅ 이메일 전송 완료: {success_count}/{len(email_configs)}개 성공\n")
    
    def _convert_to_html(self, text: str) -> str:
        """텍스트를 HTML로 변환"""
        html = text.replace('\n', '<br>')
        html = html.replace('═', '─')
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
            line-height: 1.8;
            color: #2c3e50;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f8f9fa;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e9ecef;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
        h2 {{ color: #667eea; margin-top: 0; }}
        strong {{ color: #495057; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin:0;">🎯 광고 시장 Daily Brief</h1>
            <p style="margin:10px 0 0 0; font-size:1.1em;">{self.today}</p>
        </div>
        
        <div style="white-space: pre-wrap; font-family: monospace;">
{html}
        </div>
        
        <div class="footer">
            <p>💌 매일 아침 최신 광고 시장 인사이트를 받아보세요</p>
            <p>Powered by Advanced Ad Insights Agent 🤖</p>
        </div>
    </div>
</body>
</html>
"""
        return html_template
    
    def run(self, slack_webhooks: List[str] = None, email_configs: List[Dict] = None):
        """에이전트 전체 실행"""
        print("\n" + "="*60)
        print("🤖 Multi-Recipient Ad Insights Agent 시작!")
        print("="*60 + "\n")
        
        # 1. 인사이트 수집
        self.collect_all_insights()
        
        # 2. 리포트 생성
        report = self.generate_comprehensive_report()
        
        # 3. 여러 슬랙 채널로 전송
        if slack_webhooks:
            self.send_to_multiple_slack(report, slack_webhooks)
        
        # 4. 여러 이메일로 전송
        if email_configs:
            self.send_to_multiple_emails(report, email_configs)
        
        print("\n" + "="*60)
        print("✨ 모든 작업 완료!")
        print("="*60 + "\n")
        
        return report


def parse_comma_separated(env_var: str) -> List[str]:
    """쉼표로 구분된 환경변수 파싱"""
    value = os.getenv(env_var, '')
    if not value:
        return []
    return [v.strip() for v in value.split(',') if v.strip()]


def main():
    """메인 함수"""
    
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not anthropic_api_key:
        print("⚠️  경고: ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        return
    
    # 슬랙 Webhooks 수집
    slack_webhooks = []
    
    # 방법 1: 쉼표로 구분된 값
    comma_webhooks = parse_comma_separated('SLACK_WEBHOOK_URL')
    slack_webhooks.extend(comma_webhooks)
    
    # 방법 2: 개별 환경변수 (SLACK_WEBHOOK_1, SLACK_WEBHOOK_2, ...)
    for i in range(1, 11):  # 최대 10개
        webhook = os.getenv(f'SLACK_WEBHOOK_{i}')
        if webhook:
            slack_webhooks.append(webhook)
    
    # 이메일 설정 수집
    email_configs = []
    
    # 기본 SMTP 설정
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    from_email = os.getenv('FROM_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    # 방법 1: 쉼표로 구분된 이메일 주소
    to_emails = parse_comma_separated('TO_EMAIL')
    for to_email in to_emails:
        if from_email and password:
            email_configs.append({
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'from_email': from_email,
                'to_email': to_email,
                'password': password
            })
    
    # 방법 2: 개별 환경변수 (TO_EMAIL_1, TO_EMAIL_2, ...)
    for i in range(1, 11):  # 최대 10개
        to_email = os.getenv(f'TO_EMAIL_{i}')
        if to_email and from_email and password:
            email_configs.append({
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'from_email': from_email,
                'to_email': to_email,
                'password': password
            })
    
    # 수신자 정보 출력
    print("\n📊 수신자 설정 정보:")
    print(f"   슬랙 채널: {len(slack_webhooks)}개")
    print(f"   이메일 주소: {len(email_configs)}개")
    print()
    
    # 에이전트 실행
    agent = MultiRecipientAdInsightsAgent(anthropic_api_key)
    agent.run(slack_webhooks, email_configs)


if __name__ == "__main__":
    main()
