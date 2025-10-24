# 🎯 멀티 수신자 설정 가이드

여러 슬랙 채널과 이메일 주소로 동시에 리포트를 받는 방법입니다.

---

## 📦 사용할 파일

- `multi_recipient_agent.py` - 멀티 수신자 지원 에이전트
- `.github/workflows/multi-recipient-insights.yml` - GitHub Actions 워크플로우

---

## 🎨 설정 방법 (2가지 선택)

### 방법 1: 쉼표로 구분 (간단!)

**장점:** 설정이 간단함  
**단점:** Secrets가 길어질 수 있음

#### GitHub Secrets 설정:

```
ANTHROPIC_API_KEY = sk-ant-api03-여러분의키

# 여러 슬랙 채널 (쉼표로 구분)
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/AAA,https://hooks.slack.com/services/BBB,https://hooks.slack.com/services/CCC

# 여러 이메일 주소 (쉼표로 구분)
TO_EMAIL = person1@company.com,person2@company.com,person3@company.com

# 이메일 발송 설정
FROM_EMAIL = sender@gmail.com
EMAIL_PASSWORD = 16자리앱비밀번호
```

---

### 방법 2: 개별 Secrets (추천!)

**장점:** 관리가 명확함, 나중에 추가/삭제 쉬움  
**단점:** Secrets 개수가 많아짐

#### GitHub Secrets 설정:

```
ANTHROPIC_API_KEY = sk-ant-api03-여러분의키

# 슬랙 채널 1 (예: 팀 채널)
SLACK_WEBHOOK_1 = https://hooks.slack.com/services/TEAM_AAA

# 슬랙 채널 2 (예: 보고용 채널)
SLACK_WEBHOOK_2 = https://hooks.slack.com/services/REPORT_BBB

# 슬랙 채널 3 (예: 경영진 채널)
SLACK_WEBHOOK_3 = https://hooks.slack.com/services/EXEC_CCC

# 이메일 수신자 1
TO_EMAIL_1 = team.lead@company.com

# 이메일 수신자 2
TO_EMAIL_2 = manager@company.com

# 이메일 수신자 3
TO_EMAIL_3 = analyst@company.com

# 이메일 발송 설정
FROM_EMAIL = sender@gmail.com
EMAIL_PASSWORD = 16자리앱비밀번호
```

---

## 🔧 두 방법 함께 사용 가능!

쉼표 구분 + 개별 Secrets를 동시에 사용할 수도 있어요:

```
# 기본 팀은 쉼표로
TO_EMAIL = person1@company.com,person2@company.com

# 추가 VIP는 개별로
TO_EMAIL_1 = ceo@company.com
TO_EMAIL_2 = cfo@company.com
```

→ 총 4명에게 전송됩니다!

---

## 📋 실제 설정 예시

### 시나리오: 광고팀 전체 + 경영진 + 외부 컨설턴트

#### 슬랙 설정:
```
SLACK_WEBHOOK_1 = https://hooks.slack.com/services/XXX  # #광고팀 채널
SLACK_WEBHOOK_2 = https://hooks.slack.com/services/YYY  # #경영진 채널
```

#### 이메일 설정:
```
# 광고팀
TO_EMAIL = ad.team1@company.com,ad.team2@company.com,ad.team3@company.com

# 경영진
TO_EMAIL_1 = cmo@company.com

# 외부 컨설턴트
TO_EMAIL_2 = consultant@agency.com
```

→ **2개 슬랙 채널 + 5명 이메일**로 전송!

---

## ⚙️ GitHub Secrets 설정 단계

### 1. 저장소 페이지 이동
GitHub 저장소 → `Settings` 클릭

### 2. Secrets 페이지 이동
왼쪽 메뉴 → `Secrets and variables` → `Actions`

### 3. Secret 추가
`New repository secret` 버튼 클릭

### 4. 각 Secret 입력

**필수:**
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-api03-...`

**슬랙 (방법 1):**
- Name: `SLACK_WEBHOOK_URL`
- Value: `https://hooks.slack.com/services/AAA,https://hooks.slack.com/services/BBB`

**슬랙 (방법 2):**
- Name: `SLACK_WEBHOOK_1`, Value: `https://hooks.slack.com/services/AAA`
- Name: `SLACK_WEBHOOK_2`, Value: `https://hooks.slack.com/services/BBB`
- Name: `SLACK_WEBHOOK_3`, Value: `https://hooks.slack.com/services/CCC`

**이메일:**
- Name: `FROM_EMAIL`, Value: `sender@gmail.com`
- Name: `EMAIL_PASSWORD`, Value: `16자리앱비밀번호`
- Name: `TO_EMAIL`, Value: `email1@co.com,email2@co.com` (방법 1)
- 또는 `TO_EMAIL_1`, `TO_EMAIL_2`, ... (방법 2)

---

## 🧪 테스트하기

### 1. 워크플로우 수동 실행

1. GitHub 저장소 → `Actions` 탭
2. `Daily Ad Insights (Multi Recipients)` 선택
3. `Run workflow` 버튼 클릭

### 2. 결과 확인

- **슬랙:** 각 채널에 메시지 도착 확인
- **이메일:** 각 주소로 이메일 도착 확인
- **로그:** Actions 페이지에서 전송 성공/실패 확인

---

## 📊 최대 수신자 수

**현재 설정:**
- 슬랙: 최대 10개 채널 (쉼표 구분 무제한 + 개별 1~10)
- 이메일: 최대 10개 주소 (쉼표 구분 무제한 + 개별 1~10)

**더 필요하면?**
코드에서 `range(1, 11)` → `range(1, 21)`로 변경

---

## 💡 실전 팁

### 1. 채널별로 이름 붙이기

Secrets 이름을 의미있게:
```
SLACK_WEBHOOK_TEAM = ...     # 팀 채널
SLACK_WEBHOOK_EXEC = ...     # 경영진 채널
SLACK_WEBHOOK_CLIENT = ...   # 클라이언트 채널
```

(단, 코드 수정 필요)

### 2. 테스트 수신자 먼저 설정

처음엔 본인 이메일/슬랙만 설정:
```
TO_EMAIL_1 = my.test@gmail.com
```

잘 작동하는지 확인 후 다른 사람 추가!

### 3. 중복 제거

같은 이메일을 여러 번 입력하면 중복 전송됩니다.  
조심하세요!

### 4. 외부 수신자 주의

외부 이메일/슬랙으로 보낼 때는 보안 정책 확인:
- 회사 기밀 정보 포함 여부
- 외부 공유 승인 여부

---

## 🔍 전송 현황 확인

코드 실행 시 로그에 표시됩니다:

```
📊 수신자 설정 정보:
   슬랙 채널: 3개
   이메일 주소: 5개

📤 3개 슬랙 채널로 전송 중...
   [1/3] ✅ 슬랙 채널 #1 전송 완료!
   [2/3] ✅ 슬랙 채널 #2 전송 완료!
   [3/3] ✅ 슬랙 채널 #3 전송 완료!
✅ 슬랙 전송 완료: 3/3개 성공

📧 5개 이메일 주소로 전송 중...
   [1/5] ✅ person1@company.com 전송 완료!
   [2/5] ✅ person2@company.com 전송 완료!
   ...
✅ 이메일 전송 완료: 5/5개 성공
```

---

## ❓ FAQ

**Q: 슬랙만 여러 개 설정하고 이메일은 하나만 할 수 있나요?**  
A: 네! 필요한 것만 설정하면 됩니다.

**Q: 나중에 수신자를 추가하려면?**  
A: GitHub Secrets에 새로운 Secret 추가하면 됩니다.

**Q: 특정 사람만 제외하고 싶어요**  
A: 해당 Secret을 삭제하거나 값을 비워두세요.

**Q: 비용이 늘어나나요?**  
A: Anthropic API 비용은 동일합니다. 수신자 수는 영향 없습니다.

**Q: 슬랙 무료 플랜으로 가능한가요?**  
A: 네! Incoming Webhooks는 무료 플랜에서도 사용 가능합니다.

---

## 🎯 체크리스트

설정 완료 확인:

```
✅ multi_recipient_agent.py 파일 업로드
✅ .github/workflows/multi-recipient-insights.yml 업로드
✅ requirements.txt 업로드
✅ ANTHROPIC_API_KEY Secret 설정
✅ 슬랙 Webhook Secrets 설정
✅ 이메일 Secrets 설정
✅ 수동 실행으로 테스트
✅ 모든 수신자에게 도착 확인
```

---

## 🚀 바로 시작하기

```bash
# 1. 파일 업로드
- multi_recipient_agent.py
- .github/workflows/multi-recipient-insights.yml

# 2. GitHub Secrets 설정
(위 가이드 참고)

# 3. Actions → Run workflow
(수동 테스트)

# 4. 수신 확인
(슬랙/이메일 체크)

# 5. 완료! 🎉
매일 오전 9시 자동 실행
```

---

**이제 팀 전체가 매일 광고 시장 인사이트를 받을 수 있습니다! 🎊**
