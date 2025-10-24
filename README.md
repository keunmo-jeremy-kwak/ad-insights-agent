# 🎯 광고 시장 인사이트 Daily 에이전트

매일 아침 광고/마케팅 시장의 최신 트렌드, 플랫폼 동향, 기술 혁신, 규제 변화를 자동으로 수집하여 슬랙과 이메일로 전송하는 AI 에이전트입니다.

## ✨ 주요 기능

- 🔍 **자동 웹 검색**: Claude AI를 활용하여 15개 이상의 핵심 주제를 매일 검색
- 📊 **인사이트 분석**: 수집된 정보를 카테고리별로 분류하고 요약
- 💬 **슬랙 알림**: 핵심 요약을 슬랙으로 즉시 전송
- 📧 **이메일 리포트**: 상세한 HTML 리포트를 이메일로 전송
- ⏰ **자동 스케줄링**: 매일 지정된 시간에 자동 실행

## 📋 수집하는 정보

### 시장 트렌드
- 디지털 광고 시장 전망
- Performance Marketing 동향
- Retail Media 성장
- 쿠키리스 대응 전략

### 플랫폼 동향
- 네이버, 카카오, 구글, 메타, 틱톡 등 주요 플랫폼의 신규 상품 및 업데이트

### 기술 혁신
- AI 광고 자동화
- 생성형 AI 마케팅 활용
- Attribution 측정 기술

### 규제 및 정책
- 개인정보보호 관련 규제
- 온라인 플랫폼 법안

## 🚀 설치 방법

### 1. 사전 준비

**필수 요구사항:**
- Python 3.8 이상
- Anthropic API Key (Claude API)

**선택 사항:**
- Slack Workspace (슬랙 알림을 받으려면)
- Gmail 계정 (이메일 리포트를 받으려면)

### 2. 설치

```bash
# 저장소 클론 (또는 파일 다운로드)
cd ad-insights-agent

# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 설정

#### 3.1 Anthropic API Key 발급

1. https://console.anthropic.com/ 접속
2. API Keys 메뉴에서 새 키 생성
3. 키를 안전하게 보관

#### 3.2 Slack Webhook 설정 (선택)

1. https://api.slack.com/apps 접속
2. "Create New App" → "From scratch"
3. App 이름과 Workspace 선택
4. "Incoming Webhooks" 활성화
5. "Add New Webhook to Workspace" 클릭
6. 채널 선택 후 Webhook URL 복사

#### 3.3 Gmail 앱 비밀번호 생성 (선택)

1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. https://myaccount.google.com/apppasswords 접속
4. 앱 비밀번호 생성 (16자리)

#### 3.4 환경변수 설정

```bash
# .env.template을 .env로 복사
cp .env.template .env

# .env 파일 편집
# 실제 API 키와 설정값 입력
```

`.env` 파일 예시:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=recipient@gmail.com
EMAIL_PASSWORD=your_16_digit_app_password
RUN_HOUR=9
RUN_MINUTE=0
```

## 💻 사용 방법

### 수동 실행 (테스트)

```bash
# 기본 에이전트 실행
python ad_insights_agent.py

# 고급 에이전트 실행 (웹 검색 포함)
python advanced_ad_insights_agent.py
```

### 자동 스케줄링

매일 지정된 시간에 자동으로 실행:

```bash
# 스케줄러 시작
python scheduler.py

# 즉시 실행 + 스케줄링
RUN_IMMEDIATELY=true python scheduler.py
```

**백그라운드 실행 (Linux/Mac):**
```bash
nohup python scheduler.py > agent.log 2>&1 &
```

**Windows 작업 스케줄러 등록:**
1. 작업 스케줄러 실행
2. "기본 작업 만들기"
3. Python 경로와 스크립트 설정
4. 트리거를 "매일"로 설정

## 📱 결과물 예시

### 슬랙 알림
```
🎯 광고 시장 Daily Brief - 2025-10-24

5개의 핵심 인사이트를 수집했습니다!

──────────────────────────────

1. 디지털 광고 시장 트렌드 2025
성능 마케팅에서 브랜드 중심으로 회귀하는 움직임이 감지됨...

2. AI 광고 자동화
생성형 AI를 활용한 크리에이티브 자동화가 급성장...

...

📧 전체 리포트는 이메일을 확인해주세요!
```

### 이메일 리포트
- 카테고리별 정리된 인사이트
- 핵심 포인트 및 액션 아이템
- 소스 링크 포함
- HTML 형식의 가독성 높은 리포트

## ⚙️ 커스터마이징

### 검색 키워드 수정

`advanced_ad_insights_agent.py` 파일에서 `search_queries` 리스트를 수정:

```python
self.search_queries = [
    "원하는 검색어 1",
    "원하는 검색어 2",
    # ... 추가
]
```

### 실행 시간 변경

`.env` 파일에서:
```env
RUN_HOUR=9    # 오전 9시
RUN_MINUTE=30 # 30분
```

### 리포트 형식 변경

`generate_comprehensive_report()` 메서드를 수정하여 원하는 형식으로 커스터마이징

## 🔧 문제 해결

### API 오류
- API Key가 올바른지 확인
- API 사용량 한도 확인
- 네트워크 연결 확인

### 슬랙 전송 실패
- Webhook URL이 유효한지 확인
- Slack App의 권한 확인

### 이메일 전송 실패
- Gmail 앱 비밀번호 재생성
- 2단계 인증 활성화 확인
- SMTP 설정 확인

### 검색 결과 없음
- 인터넷 연결 확인
- API 응답 로그 확인
- 검색 키워드가 너무 구체적인지 확인

## 📊 비용 예상

### Anthropic API
- 15개 검색 쿼리 × 2,000 토큰 = 약 30,000 토큰/일
- Claude Sonnet 4 기준: 약 $0.10/일
- 월 예상 비용: ~$3

### 기타
- Slack: 무료
- Gmail: 무료
- 서버: 로컬 또는 클라우드 ($5-10/월)

## 🎨 향후 개선 계획

- [ ] 웹 대시보드 추가
- [ ] 데이터베이스 연동 (트렌드 분석)
- [ ] 노션 통합
- [ ] 맞춤형 알림 설정
- [ ] 멀티 언어 지원
- [ ] PDF 리포트 생성
- [ ] 모바일 앱 알림

## 🤝 기여

개선 아이디어나 버그 리포트는 언제나 환영합니다!

## 📄 라이선스

MIT License

## 💡 Tips

1. **처음에는 수동 실행으로 테스트**하세요
2. 슬랙 알림만 또는 이메일만 설정해도 됩니다
3. 검색 키워드는 구체적이면서도 너무 좁지 않게
4. 실행 로그를 주기적으로 확인하세요
5. API 키는 절대 공개하지 마세요

## 📞 문의

문제가 있거나 도움이 필요하면 언제든 연락주세요!

---

**Happy Insights Hunting! 🚀**
