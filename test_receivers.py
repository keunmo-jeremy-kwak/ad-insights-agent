"""
수신처 설정 테스트 스크립트
"""
import os
import requests
from email.mime.text import MIMEText
import smtplib

def test_slack():
    """슬랙 수신처 테스트"""
    webhook = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook:
        print("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        return False
    
    print(f"📤 슬랙 테스트 메시지 전송 중...")
    print(f"   Webhook: {webhook[:50]}...")
    
    try:
        response = requests.post(
            webhook,
            json={"text": "🎉 테스트 성공! 광고 인사이트 에이전트가 준비되었습니다."}
        )
        
        if response.status_code == 200:
            print("✅ 슬랙 전송 성공! 채널을 확인하세요.")
            return True
        else:
            print(f"❌ 슬랙 전송 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def test_email():
    """이메일 수신처 테스트"""
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    if not all([from_email, to_email, password]):
        print("❌ 이메일 설정이 완료되지 않았습니다.")
        print(f"   FROM_EMAIL: {'✅' if from_email else '❌'}")
        print(f"   TO_EMAIL: {'✅' if to_email else '❌'}")
        print(f"   EMAIL_PASSWORD: {'✅' if password else '❌'}")
        return False
    
    print(f"📧 이메일 테스트 메시지 전송 중...")
    print(f"   보내는 주소: {from_email}")
    print(f"   받는 주소: {to_email}")
    
    try:
        msg = MIMEText("🎉 테스트 성공! 광고 인사이트 에이전트가 준비되었습니다.")
        msg['Subject'] = "광고 인사이트 에이전트 테스트"
        msg['From'] = from_email
        msg['To'] = to_email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        
        print("✅ 이메일 전송 성공! 받은편지함을 확인하세요.")
        return True
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🧪 광고 인사이트 에이전트 - 수신처 테스트")
    print("="*60 + "\n")
    
    # 슬랙 테스트
    slack_ok = test_slack()
    print()
    
    # 이메일 테스트
    email_ok = test_email()
    print()
    
    # 결과 요약
    print("="*60)
    print("📊 테스트 결과")
    print("="*60)
    print(f"슬랙:   {'✅ 성공' if slack_ok else '❌ 실패 또는 미설정'}")
    print(f"이메일: {'✅ 성공' if email_ok else '❌ 실패 또는 미설정'}")
    print()
    
    if slack_ok or email_ok:
        print("✨ 최소 1개 이상 성공! 에이전트를 사용할 수 있습니다.")
    else:
        print("⚠️  슬랙 또는 이메일 중 하나는 설정해주세요.")
    print()


if __name__ == "__main__":
    main()
