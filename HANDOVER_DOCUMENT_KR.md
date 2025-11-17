# QC Request Form Generator - 인수인계 문서

## 개요
이 애플리케이션은 Jira 티켓용 표준화된 QC(Quality Control) 요청 폼을 생성하는 Streamlit 기반 도구임. CSV 파일에서 테스트 케이스 데이터를 읽어와 사용자가 프로젝트, 컴포넌트, 테스트 범위를 선택하면 자동으로 포맷된 QC 요청 폼을 생성함.

---

## 빠른 시작

### 애플리케이션 접속
**운영 URL**: https://qc-generator.streamlit.app/

애플리케이션은 Streamlit Cloud에 배포되어 있으며 위 링크로 접속 가능함.

### 로컬 실행 (선택사항)
```bash
streamlit run qc-request/qc_form_generator.py
```

애플리케이션이 기본 웹 브라우저에서 `http://localhost:8501`로 실행됨.

### Streamlit Cloud 배포
앱은 현재 개인 GitHub 저장소에서 배포됨. 배포 업데이트 방법:
1. 연결된 GitHub 저장소에 변경사항 푸시
2. Streamlit Cloud가 자동으로 앱 재배포
3. 자세한 배포 방법은 Streamlit 공식 문서 참고

---

## 주요 구성 요소

### 1. 메인 애플리케이션 파일
- **파일**: `qc_form_generator.py`
- **목적**: QC 요청 폼 생성용 Streamlit UI
- **데이터 소스**: `processed-data/combined_project_test_cases.csv`에서 읽어옴

### 2. 데이터 처리 스크립트
- **파일**: `excel_tc_processor.py`
- **목적**: 새 테스트 케이스 파일을 올바른 형식으로 변환하고 combined CSV에 병합함

---

## 새 테스트 케이스 추가 방법 (중요)

### 입력 파일 요구사항

입력 Excel/CSV 파일은 **반드시** 다음 컬럼들을 포함해야 함:

| Column Name | Korean Name | Required | Description |
|-------------|-------------|----------|-------------|
| Purpose | Purpose | Yes | 타겟 플랫폼 (예: "WEB", "MOBILE", "CONNECTED TV", "SMARTTV") |
| 대분류 | 대분류 | Yes | 메인 카테고리 |
| 중분류 | 중분류 | No | 서브 카테고리 (비어있어도 됨) |
| 소분류 | 소분류 | No | 컴포넌트 (비어있어도 됨) |
| 테스트 항목 | 테스트 항목 | Yes | 테스트 케이스 설명 |

**추가 컬럼** (Section, 사전조건, 테스트 스텝, 기대결과 등)은 존재해도 되지만 무시됨.

### Purpose 컬럼 값
`Purpose` 컬럼은 테스트가 적용되는 디바이스를 결정함:
- **"WEB"** → Web = True로 설정
- **"MOBILE"** → Android Mobile & Apple Mobile = True로 설정
- **"CONNECTED TV"** → Android TV, Apple TV, Fire TV, Roku = True로 설정
- **"SMARTTV"** → Smart TV & Vizio TV = True로 설정

대소문자 구분 없으며 여러 키워드 포함 가능함.

---

## 단계별: 새 프로젝트 데이터 추가

### Step 1: 입력 파일 준비
1. Excel/CSV 파일을 `data/` 폴더에 배치
2. 위에 나열된 필수 컬럼이 있는지 확인
3. 파일명 예시: `KOCOWA 4.0 Requested Test_No114_20251024_Get_Started.csv`

### Step 2: 처리 스크립트 업데이트
`excel_tc_processor.py` 파일을 열고 다음 라인들을 수정:

```python
# Line 59: 입력 파일 경로 업데이트
project_file_path = PROJECT_DIR / "data" / f"YOUR_NEW_FILE.csv"

# Line 70: 프로젝트 이름 업데이트
project_name = "Your Project Name"
```

### Step 3: 처리 스크립트 실행
```bash
python qc-request/excel_tc_processor.py
```

실행하면:
1. 입력 파일 처리됨
2. `processed-data/`에 날짜가 붙은 출력 파일 생성됨 (예: `20251028_Your Project Name.csv`)
3. 자동으로 `combined_project_test_cases.csv`에 병합됨

### Step 4: 출력 확인
`processed-data/combined_project_test_cases.csv`에 새 프로젝트 데이터가 다음 내용으로 포함되었는지 확인:
- 올바른 프로젝트 이름
- 적절한 디바이스 매핑 (True/False 값)
- scope별로 그룹화된 테스트 케이스
- 필수 컬럼 모두 존재

### Step 5: 애플리케이션에서 테스트
1. Streamlit 앱 실행
2. 드롭다운에서 새 프로젝트 선택
3. 컴포넌트와 테스트 케이스가 올바르게 나타나는지 확인

---

## 출력 형식 (combined_project_test_cases.csv)

처리된 파일은 다음 컬럼들을 가짐:
```
project_name, main_category, scope_of_dev, test_case, Fire TV, Roku,
Android TV, Apple TV, Web, Apple Mobile, Android Mobile, Smart TV, Vizio TV
```

- **project_name**: 프로젝트 식별자
- **main_category**: 최상위 카테고리화
- **scope_of_dev**: 중분류 또는 소분류에서 생성됨 (중분류가 우선순위)
- **test_case**: 여러 테스트 케이스가 줄바꿈(`\n`)으로 결합됨
- **Device 컬럼들**: Boolean (True/False) 플랫폼 적용 가능 여부 표시

---

## 문제 해결

### 이슈: 새 프로젝트가 드롭다운에 나타나지 않음
- **해결방법**: 처리 스크립트에서 `project_name`이 올바르게 설정되었는지 확인
- 데이터가 실제로 `combined_project_test_cases.csv`에 추가되었는지 확인

### 이슈: 특정 디바이스에 컴포넌트가 표시되지 않음
- **해결방법**: 입력 파일의 `Purpose` 컬럼 확인
- 디바이스 키워드가 올바르게 철자되었는지 확인 (대소문자 무관)
- 처리된 CSV에서 디바이스 컬럼이 `True` 값을 가지는지 확인

### 이슈: 테스트 케이스가 표시되지 않음
- **해결방법**: 입력 파일의 `테스트 항목` 컬럼이 비어있지 않은지 확인
- 특수 문자 사용 시 인코딩 이슈 확인

### 이슈: 처리 스크립트 실패
- **해결방법**: 입력 파일에 필수 컬럼이 모두 존재하는지 확인
- 컬럼명의 오타 확인 (한글 문자는 정확히 일치해야 함)
- 파일 경로가 올바른지 확인

---

## 지원 디바이스
애플리케이션은 다음 9가지 디바이스 타입을 지원함:
- Android Mobile
- Apple Mobile
- Android TV
- Apple TV
- Fire TV
- Roku
- Web
- Smart TV
- Vizio TV

---

## 유지보수 노트

### 파일 구조
```
qc-request/
├── qc_form_generator.py          # 메인 Streamlit 앱
├── excel_tc_processor.py         # 데이터 처리 스크립트
├── data/                          # 원본 입력 파일
└── processed-data/                # 처리된 CSV 파일
    └── combined_project_test_cases.csv  # 마스터 데이터 파일
```

### 정기 작업
1. **새 테스트 케이스 추가**: 위의 5단계 프로세스 따르기
2. **기존 프로젝트 업데이트**: 업데이트된 입력 파일로 프로세서 재실행
3. **데이터 백업**: `combined_project_test_cases.csv` 주기적으로 백업

### 중요 사항
- 처리 스크립트는 combined 파일에 새 데이터를 **추가함** (덮어쓰지 않음)
- 동일한 `project_name`, `main_category`, `scope_of_dev`를 가진 테스트 케이스는 함께 그룹화됨
- 디바이스 관련성은 `Purpose` 컬럼 키워드를 기반으로 함 (위 표 참고)

---

## 문의 및 지원
이 애플리케이션 관련 질문이나 이슈는 PM 팀에 연락하거나 `excel_tc_processor.py`와 `qc_form_generator.py`의 코드 주석 참고.
