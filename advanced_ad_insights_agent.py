"""
Advanced Ad Insights Agent with Real Web Search
Claude API를 활용하여 실제 웹에서 광고 시장 인사이트를 수집
"""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AdvancedAdInsightsAgent:
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
                # JSON 파싱
                try:
                    # 마크다운 코드 블록 제거
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
        
        # 카테고리별로 분류
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
        
        # 카테고리별 리포트 작성
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
        
        # 종합 인사이트
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
    
    def send_to_slack(self, report: str, webhook_url: str):
        """슬랙으로 전송"""
        try:
            # 슬랙 블록으로 변환 (더 보기 좋게)
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
            
            # 상위 5개 인사이트만 슬랙에 표시
            for i, result in enumerate(self.results[:5], 1):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{i}. {result['query']}*\n{result['summary'][:200]}..."
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
                print("✅ 슬랙 전송 완료!")
            else:
                print(f"❌ 슬랙 전송 실패: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ 슬랙 전송 오류: {e}")
    
    def send_to_email(self, report: str, config: Dict):
        """이메일 전송 (HTML 포맷)"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 광고 시장 Daily Brief - {self.today}"
            msg['From'] = config['from_email']
            msg['To'] = config['to_email']
            
            # HTML 변환
            html_report = self._convert_to_html(report)
            
            text_part = MIMEText(report, 'plain', 'utf-8')
            html_part = MIMEText(html_report, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # 전송
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls()
                server.login(config['from_email'], config['password'])
                server.send_message(msg)
            
            print("✅ 이메일 전송 완료!")
            
        except Exception as e:
            print(f"❌ 이메일 전송 오류: {e}")
    
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
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .insight {{
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
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
        .emoji {{ font-size: 1.2em; }}
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
    
    def run(self, slack_webhook: str = None, email_config: Dict = None):
        """에이전트 전체 실행"""
        print("\n" + "="*60)
        print("🤖 Advanced Ad Insights Agent 시작!")
        print("="*60 + "\n")
        
        # 1. 인사이트 수집
        self.collect_all_insights()
        
        # 2. 리포트 생성
        report = self.generate_comprehensive_report()
        
        # 3. 슬랙 전송
        if slack_webhook:
            print("\n📤 슬랙 전송 중...")
            self.send_to_slack(report, slack_webhook)
        
        # 4. 이메일 전송
        if email_config and all(email_config.values()):
            print("📧 이메일 전송 중...")
            self.send_to_email(report, email_config)
        
        print("\n" + "="*60)
        print("✨ 모든 작업 완료!")
        print("="*60 + "\n")
        
        return report


def main():
    """메인 함수"""
    
    # 설정 로드
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    
    email_config = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'from_email': os.getenv('FROM_EMAIL'),
        'to_email': os.getenv('TO_EMAIL'),
        'password': os.getenv('EMAIL_PASSWORD')
    }
    
    # API 키 확인
    if not anthropic_api_key:
        print("⚠️  경고: ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        print("환경변수를 설정하거나 .env 파일을 확인해주세요.\n")
        return
    
    # 에이전트 실행
    agent = AdvancedAdInsightsAgent(anthropic_api_key)
    agent.run(slack_webhook, email_config)


if __name__ == "__main__":
    main()
