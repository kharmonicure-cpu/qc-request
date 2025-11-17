# Streamlit Cloud 배포 가이드

## 사전 준비사항

배포하기 전에 필요한 것들:
1. GitHub 계정
2. GitHub 저장소에 올려진 QC Request Form Generator 코드
3. Streamlit Cloud 계정 (무료, GitHub 계정으로 연결됨)

---

## Step 1: GitHub 저장소 준비

### 1.1 새 저장소 생성 (또는 기존 저장소 사용)
```bash
# 프로젝트 폴더로 이동
cd qc-request

# git 초기화 (아직 안 했다면)
git init

# 파일 추가
git add .
git commit -m "Initial commit for QC Form Generator"

# GitHub에서 새 저장소 생성 (웹 인터페이스 사용)
# 그 다음 연결 및 푸시:
git remote add origin https://github.com/YOUR_USERNAME/qc-generator.git
git branch -M main
git push -u origin main
```

### 1.2 저장소에 필요한 파일들

저장소 루트 레벨에 **반드시** 포함되어야 하는 파일들:

```
qc-request/
├── qc_form_generator.py           # 메인 앱 파일
├── requirements.txt               # Python 의존성
├── .streamlit/
│   └── config.toml               # Streamlit 설정
└── processed-data/
    └── combined_project_test_cases.csv  # 데이터
```

**중요:** `qc_form_generator.py`의 경로는 상대경로여야 함:
```python
# qc_form_generator.py의 9번째 줄은 다음과 같아야 함:
df = pd.read_csv("qc-request/processed-data/combined_project_test_cases.csv")

# 또는 앱이 루트에 있다면:
df = pd.read_csv("processed-data/combined_project_test_cases.csv")
```

---

## Step 2: Streamlit Cloud에 배포

### 2.1 Streamlit Cloud 가입
1. https://share.streamlit.io/ 접속
2. "Sign up" 클릭 후 GitHub 계정으로 로그인
3. Streamlit이 GitHub 저장소에 접근하도록 권한 부여

### 2.2 새 앱 생성
1. "New app" 버튼 클릭
2. 배포 폼 작성:

   **Repository:** GitHub 저장소 선택 (예: `YOUR_USERNAME/qc-generator`)

   **Branch:** `main` (또는 기본 브랜치)

   **Main file path:** `qc-request/qc_form_generator.py`

   **App URL (선택사항):** 커스텀 서브도메인 선택 (예: `qc-generator`)

3. "Deploy!" 클릭

### 2.3 배포 대기
- 첫 배포는 2-5분 소요됨
- 의존성 설치 과정이 로그로 표시됨
- 완료되면 앱이 라이브로 올라감

---

## Step 3: 배포 확인

### 3.1 앱 확인
앱은 다음 주소에서 접속 가능:
```
https://YOUR_SUBDOMAIN.streamlit.app/
```

테스트 항목:
- [ ] 프로젝트가 드롭다운에 표시됨
- [ ] 다양한 디바이스에 컴포넌트가 로드됨
- [ ] 폼이 정상적으로 생성됨
- [ ] 앱에 에러가 없음

### 3.2 로그 확인
문제가 발생하면:
1. https://share.streamlit.io/ 접속
2. 앱 클릭
3. "Manage app" → "Logs" 클릭
4. 에러 메시지 확인

---

## Step 4: 앱 업데이트

### 자동 재배포
GitHub에 푸시하면 Streamlit Cloud가 자동으로 재배포함:

```bash
# 코드 수정
# 예시: combined_project_test_cases.csv 업데이트

# 커밋 및 푸시
git add processed-data/combined_project_test_cases.csv
git commit -m "Add new project test cases"
git push

# Streamlit Cloud가 자동으로 푸시를 감지하고 재배포함!
```

### 수동 재배포
강제로 재배포가 필요한 경우:
1. https://share.streamlit.io/ 접속
2. 앱 클릭
3. "Reboot app" 클릭 (점 세 개 메뉴)

---

## 일반적인 문제 & 해결방법

### 이슈 1: CSV 파일 "File not found" 에러
**문제:** 앱이 `combined_project_test_cases.csv`를 찾지 못함

**해결방법:**
- 파일이 GitHub에 커밋되었는지 확인 (`git status`)
- `qc_form_generator.py` 9번째 줄의 경로 확인
- 경로가 절대경로가 아닌 상대경로인지 확인
- 파일이 `processed-data/` 폴더에 있는지 확인

### 이슈 2: "Module not found" 에러
**문제:** Python 의존성 패키지 누락

**해결방법:**
- `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
- `requirements.txt`가 저장소 루트에 있는지 확인
- 현재 필요한 패키지:
  ```
  streamlit>=1.45.0
  pandas>=2.2.0
  ```

### 이슈 3: 앱에 이전 데이터가 표시됨
**문제:** CSV를 업데이트했지만 앱에 이전 테스트 케이스가 표시됨

**해결방법:**
- 브라우저 캐시 삭제
- Streamlit Cloud 대시보드에서 앱 강제 재부팅
- 캐시가 클리어될 때까지 1-2분 대기

### 이슈 4: Permission denied 또는 저장소를 찾을 수 없음
**문제:** Streamlit이 저장소에 접근할 수 없음

**해결방법:**
- 저장소가 public인지 확인 또는
- Streamlit Cloud에 private 저장소 접근 권한 부여:
  1. GitHub Settings 이동
  2. Applications → Streamlit
  3. 저장소에 대한 접근 권한 부여

### 이슈 5: 앱이 느리거나 타임아웃됨
**문제:** 큰 CSV 파일 또는 복잡한 작업

**해결방법:**
- CSV 파일 최적화 (불필요한 컬럼 제거)
- 데이터 로딩에 캐싱 추가:
  ```python
  @st.cache_data
  def load_data():
      return pd.read_csv("processed-data/combined_project_test_cases.csv")
  ```

---

## 여러 담당자 관리

### 옵션 1: 저장소 소유권 이전
1. 저장소 소유자가 GitHub 저장소 Settings로 이동
2. "Danger Zone"까지 스크롤
3. "Transfer ownership" 클릭
4. 새 소유자가 자신의 Streamlit Cloud 계정에서 재배포

### 옵션 2: Organization 계정 사용
1. GitHub Organization 생성
2. 저장소를 organization으로 이전
3. 팀 멤버에게 접근 권한 부여
4. Organization 계정에서 배포

### 옵션 3: 접근 권한 공유 (권장하지 않음)
- GitHub 계정 공유 (보안 위험)
- 옵션 1 또는 2 사용 권장

---

## 앱 설정 & 구성

### Streamlit Cloud 설정
Streamlit Cloud 대시보드에서 설정 가능한 항목:

**Secrets:** 민감한 데이터 저장 (이 앱에는 불필요)

**Resources:** 무료 플랜 포함 사항:
- 1 GB RAM
- 1 CPU 코어
- 이 앱에 충분함

**Custom Domain:** 자체 도메인 연결 (유료 플랜 필요)

### 테마 커스터마이징
`.streamlit/config.toml` 편집:

```toml
[theme]
primaryColor = "#FF6B6B"        # 강조 색상
backgroundColor = "#FFFFFF"      # 배경
secondaryBackgroundColor = "#F0F2F6"  # 사이드바
textColor = "#262730"           # 텍스트 색상
font = "sans serif"             # 폰트
```

---

## 모니터링 & 유지보수

### 앱 상태 확인
1. https://share.streamlit.io/ 접속
2. 앱 상태 확인
3. 분석 데이터 확인 (조회수, 사용자 수 등)

### 정기 유지보수 작업
1. **테스트 케이스 업데이트** - 새 CSV를 GitHub에 푸시
2. **로그 모니터링** - 주간 단위로 에러 확인
3. **의존성 업데이트** - requirements.txt 최신 상태 유지
4. **데이터 백업** - combined CSV 로컬 복사본 보관

---

## URL & 리소스

**Streamlit Cloud 대시보드:** https://share.streamlit.io/
**Streamlit 문서:** https://docs.streamlit.io/
**배포 문서:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
**트러블슈팅:** https://docs.streamlit.io/knowledge-base/deploy

---

## 빠른 참조 명령어

```bash
# GitHub에 업데이트 푸시 (자동 재배포 트리거)
git add .
git commit -m "Update test cases"
git push

# 추적 중인 파일 확인
git status

# 커밋 히스토리 확인
git log --oneline

# 테스트용 새 브랜치 생성
git checkout -b test-deployment
git push -u origin test-deployment
```

---

## 배포 관련 문의

- **Streamlit Community Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** 저장소의 Issues 탭 확인
- **Documentation:** 모든 공식 문서는 무료이며 포괄적임
