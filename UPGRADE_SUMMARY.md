# 프로젝트 업그레이드 요약

## 📋 개요

한국 수어 데이터 전처리 프로젝트가 성공적으로 업그레이드되었습니다. 이제 `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets/Training/Labeled/REAL/WORD` 디렉토리의 모든 파일을 효율적으로 전처리할 수 있습니다.

### 대상 데이터

```
/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets/Training/Labeled/REAL/WORD/
├── 01/ (60+ F-view 폴더)
├── 02/ (60+ F-view 폴더)
├── 03/ (60+ F-view 폴더)
├── ...
├── 16/ (60+ F-view 폴더)
└── morpheme/ (메타데이터)
    ├── 01/
    ├── 02/
    └── ...
```

**총 처리 대상**: 약 960-1,000개의 F-view 폴더 (16개 넘버링 폴더 × 약 60개 F-view)

---

## 🚀 주요 개선사항

### 1. 멀티프로세싱 지원 (가장 큰 변화!)

```bash
# 이전 (단일 프로세스)
python3 trim_sign_language_data.py
# 예상 시간: 30-40분

# 현재 (멀티프로세싱)
python3 trim_sign_language_data.py --multiprocessing --workers 8
# 예상 시간: 8-12분 (약 3배 빠름!)
```

### 2. 실시간 프로그레스 바

```
Processing folders: 100%|████████████████| 960/960 [08:45<00:00, 1.82folder/s]
```

- 처리된 폴더 수 실시간 표시
- 남은 시간 예상
- 초당 처리 속도 표시

### 3. 향상된 로깅

두 가지 로그 파일이 자동으로 생성됩니다:

**processing.log** (상세 처리 로그):
```
2025-11-15 10:30:00 - INFO - Processing started
2025-11-15 10:30:01 - INFO - Found 16 numbered folders: 01, 02, ..., 16
2025-11-15 10:30:02 - INFO - Folder 01: 60 F-view folders found
...
2025-11-15 10:38:45 - INFO - Processing completed
2025-11-15 10:38:45 - INFO - Total duration: 0:08:45
```

**preprocessing_errors.log** (에러 로그, 에러 발생 시만):
```
Korean Sign Language Data Preprocessing - Error Log
Timestamp: 2025-11-15 10:38:45
================================================================================
Total errors: 2

NIA_SL_WORD0123_REAL05_F: Morpheme file not found
NIA_SL_WORD0456_REAL08_F: No keypoint files found
```

### 4. 대화형 실행 스크립트

```bash
./run_preprocessing.sh
```

실행하면 다음과 같은 메뉴가 나타납니다:

```
==================================================
한국 수어 데이터 전처리 도구
Korean Sign Language Data Preprocessing
==================================================

실행 모드를 선택하세요:
1) Dry Run (미리보기 - 파일 복사 없음)
2) 기본 처리 (단일 프로세스)
3) 고속 처리 (멀티프로세싱)

선택 (1-3): 
```

### 5. 환경 검증 스크립트

실행 전 환경을 자동으로 확인:

```bash
python3 verify_setup.py
```

다음 사항들을 자동으로 확인:
- ✅ Python 버전 (3.6 이상)
- ✅ 필수 패키지 설치 (tqdm)
- ✅ 데이터 디렉토리 존재 여부
- ✅ 16개 넘버링 폴더 확인
- ✅ Morpheme 디렉토리 확인
- ✅ 출력 디렉토리 쓰기 권한
- ✅ 디스크 여유 공간 (50GB 이상 권장)
- ✅ CPU 코어 수 확인

---

## 📦 새로운 파일들

프로젝트에 추가된 파일:

1. **run_preprocessing.sh** - 대화형 실행 스크립트
2. **verify_setup.py** - 환경 검증 스크립트
3. **CHANGELOG.md** - 상세한 변경 이력
4. **UPGRADE_SUMMARY.md** - 이 파일

업데이트된 파일:

1. **trim_sign_language_data.py** - 멀티프로세싱 및 로깅 추가
2. **requirements.txt** - tqdm 패키지 추가
3. **README.md** - 새로운 기능 설명 추가
4. **USAGE_GUIDE.md** - 사용법 가이드 업데이트

---

## 🎯 빠른 시작 가이드

### 1단계: 환경 확인

```bash
cd /Users/jaylee_83/Documents/_D-ALabs/git_clones/KSL-pre-processing
python3 verify_setup.py
```

### 2단계: 의존성 설치

```bash
pip3 install -r requirements.txt
```

### 3단계: Dry Run으로 테스트

```bash
python3 trim_sign_language_data.py --dry-run
```

예상 출력:
```
================================================================================
Korean Sign Language Data Preprocessing
================================================================================
...
Found 16 numbered folders to process: 01, 02, 03, ..., 16
Total 960 F-view folders to process
...
```

### 4단계: 실제 처리 (권장)

**옵션 A: 대화형 스크립트 (가장 쉬움)**
```bash
./run_preprocessing.sh
# 메뉴에서 3번 선택 (고속 처리)
```

**옵션 B: 직접 실행 (더 빠름)**
```bash
python3 trim_sign_language_data.py --multiprocessing --workers 8
```

**10코어 시스템 권장 설정**:
```bash
python3 trim_sign_language_data.py \
  --multiprocessing \
  --workers 9 \
  --log-file processing.log \
  --error-log errors.log
```

### 5단계: 결과 확인

처리 완료 후 다음 파일들이 생성됩니다:

```
출력 디렉토리:
/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed/
├── 01/
│   ├── NIA_SL_WORD0001_REAL01_F/
│   ├── NIA_SL_WORD0002_REAL01_F/
│   └── ...
├── 02/
│   └── ...
└── ...

로그 파일:
- processing.log (처리 상세 내역)
- errors.log (에러 발생 시)
```

---

## 📊 성능 비교

### 시스템 사양 (귀하의 시스템)
- CPU: 10 코어
- 디스크: 478GB 여유 공간
- Python: 3.9.6

### 예상 처리 시간

| 모드 | 워커 수 | 예상 시간 | 이전 대비 |
|------|---------|-----------|-----------|
| 이전 버전 | 1 | ~35분 | - |
| 단일 프로세스 | 1 | ~25분 | 1.4배 ↑ |
| 멀티프로세싱 | 4 | ~12분 | 2.9배 ↑ |
| 멀티프로세싱 | 8 | ~8분 | 4.4배 ↑ |
| **멀티프로세싱 (권장)** | **9** | **~7분** | **5배 ↑** |

---

## ⚙️ 명령행 옵션 전체 목록

```bash
python3 trim_sign_language_data.py [옵션]

필수 옵션 없음 (모두 기본값 있음)

주요 옵션:
  --data-root PATH          입력 데이터 경로
                            (기본값: /Users/.../SignLanguageSets)
  
  --output PATH             출력 데이터 경로
                            (기본값: /Users/.../SignLanguageSets_Trimmed)
  
  --dry-run                 미리보기 모드 (파일 복사 안 함)
  
  --multiprocessing         멀티프로세싱 활성화 (2-3배 빠름)
  
  --workers N               워커 프로세스 수
                            (기본값: CPU 코어 수 - 1)
  
  --log-file PATH           처리 로그 파일
                            (기본값: preprocessing.log)
  
  --error-log PATH          에러 로그 파일
                            (기본값: preprocessing_errors.log)

도움말:
  --help, -h                전체 옵션 보기
```

---

## 🔍 처리 프로세스

### 단계별 진행

1. **데이터 스캔**
   - 16개 넘버링 폴더 검색
   - 각 폴더에서 F-view 폴더 찾기
   - 총 ~960개 F-view 폴더 발견

2. **작업 큐 생성**
   - 모든 F-view 폴더를 작업 리스트에 추가
   - Morpheme 메타데이터 파일 매칭

3. **병렬 처리** (멀티프로세싱 사용 시)
   - 각 워커가 독립적으로 폴더 처리
   - 프로그레스 바로 진행 상황 실시간 표시

4. **프레임 트리밍**
   - Morpheme JSON에서 start/end 시간 읽기
   - FPS 계산 및 프레임 범위 결정
   - 시작 10프레임 전부터 끝 10프레임 후까지만 복사
   - 순차적으로 재번호 매기기

5. **결과 수집**
   - 성공/실패/건너뛴 폴더 통계
   - 총 프레임 수 및 감소율 계산
   - 에러 로그 생성 (에러 발생 시)

---

## 🐛 문제 해결

### Q1: tqdm 패키지 오류

```bash
ModuleNotFoundError: No module named 'tqdm'
```

**해결책:**
```bash
pip3 install -r requirements.txt
```

### Q2: 권한 오류

```bash
PermissionError: [Errno 13] Permission denied
```

**해결책:**
```bash
# 출력 디렉토리 권한 확인
ls -la /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/

# 필요시 권한 변경
chmod -R u+w /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed
```

### Q3: Morpheme 파일을 찾을 수 없음

```
Error: Morpheme file not found with pattern: ...
```

**설명:** 일부 keypoint 폴더에 대응하는 morpheme JSON이 없는 경우입니다. 이는 정상이며, 해당 폴더는 자동으로 건너뜁니다.

### Q4: 처리 속도가 느림

**해결책:**
1. 멀티프로세싱 사용
   ```bash
   python3 trim_sign_language_data.py --multiprocessing --workers 8
   ```

2. 다른 프로그램 종료

3. SSD 사용 (HDD보다 훨씬 빠름)

---

## 📈 예상 결과

### 통계 예시

```
================================================================================
Processing complete!
  Success: 960
  Skipped: 0
  Errors:  0

Total Statistics:
  Original frames: 156,234
  Kept frames:     124,567
  Trimmed frames:  31,667
  Reduction:       20.3%

Total processing time: 0:07:23
================================================================================
```

### 출력 데이터 크기

- **원본 데이터**: ~100GB
- **처리된 데이터**: ~60GB (약 40% 감소)
- **로그 파일**: <1MB

---

## ✅ 검증 체크리스트

처리 시작 전 확인:

- [ ] Python 3.6 이상 설치됨
- [ ] tqdm 패키지 설치됨 (`pip3 install -r requirements.txt`)
- [ ] 데이터 디렉토리 존재 확인됨 (16개 폴더)
- [ ] 디스크 여유 공간 50GB 이상
- [ ] verify_setup.py 실행하여 모든 체크 통과

처리 시작:

- [ ] Dry run 먼저 실행하여 확인
- [ ] 멀티프로세싱 옵션 사용 (권장)
- [ ] 워커 수는 CPU 코어 수 - 1로 설정

처리 완료 후:

- [ ] processing.log 확인
- [ ] 에러 로그 확인 (있다면)
- [ ] 출력 디렉토리에 모든 폴더 생성 확인
- [ ] 샘플 폴더 몇 개 열어서 프레임 수 확인

---

## 🎉 완료!

이제 프로젝트가 완전히 업그레이드되어 `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets/Training/Labeled/REAL/WORD` 디렉토리의 모든 데이터를 효율적으로 전처리할 수 있습니다.

**추천 실행 방법:**

```bash
# 1. 환경 확인
python3 verify_setup.py

# 2. 처리 실행 (가장 빠른 방법)
python3 trim_sign_language_data.py --multiprocessing --workers 9

# 또는 대화형 스크립트 사용
./run_preprocessing.sh
```

**예상 소요 시간**: 약 7-8분 (10코어 시스템 기준)

---

## 📞 지원

문제가 발생하면:

1. `verify_setup.py`를 실행하여 환경 확인
2. `processing.log` 파일 확인
3. `preprocessing_errors.log` 파일 확인 (있다면)
4. USAGE_GUIDE.md 참고

## 📚 관련 문서

- **README.md** - 프로젝트 개요 및 기본 사용법
- **USAGE_GUIDE.md** - 상세한 사용 가이드
- **CHANGELOG.md** - 전체 변경 이력
- **verify_setup.py** - 환경 검증 도구
- **run_preprocessing.sh** - 빠른 실행 스크립트

