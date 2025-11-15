# KSL-pre-processing

한국 수어(Korean Sign Language) 데이터 전처리 도구

## 개요

이 도구는 한국 수어 영상 데이터를 전처리하는 스크립트입니다. 동작이 시작되기 직전 10프레임과 끝나고 나서 10프레임을 제거하여 실제 동작 구간만 추출합니다.

**처리 대상**: Front(F) 뷰 데이터만 처리합니다.

## 데이터 구조

입력 데이터는 다음과 같은 구조를 가져야 합니다:

```
SignLanguageSets/
└── Training/
    └── Labeled/
        └── REAL/
            └── WORD/
                ├── 02/
                │   ├── NIA_SL_WORD0001_REAL02_F/
                │   │   ├── NIA_SL_WORD0001_REAL02_F_000000000000_keypoints.json
                │   │   ├── NIA_SL_WORD0001_REAL02_F_000000000001_keypoints.json
                │   │   └── ...
                │   └── ...
                └── morpheme/
                    └── 02/
                        ├── NIA_SL_WORD0001_REAL02_F_morpheme.json
                        └── ...
```

## 주요 기능

✨ **2025년 업데이트된 기능들**:
- 🚀 **멀티프로세싱 지원**: CPU 코어를 활용한 병렬 처리로 2-3배 빠른 속도
- 📊 **실시간 프로그레스 바**: 처리 진행 상황을 시각적으로 확인
- 📝 **상세 로깅**: 처리 과정과 에러를 파일로 기록
- ⚡ **향상된 성능**: 대용량 데이터셋 처리 최적화
- 🎯 **더 나은 에러 처리**: 명확한 에러 메시지와 자동 복구

## 설치

Python 3.6 이상이 필요합니다.

```bash
git clone <repository-url>
cd KSL-pre-processing

# 의존성 패키지 설치
pip3 install -r requirements.txt
```

## 사용법

### 빠른 시작 (추천)

대화형 스크립트로 간편하게 실행:

```bash
./run_preprocessing.sh
```

이 스크립트는:
- 자동으로 의존성 패키지 확인 및 설치
- 3가지 실행 모드 선택 가능 (Dry Run / 기본 / 고속)
- 사용자 친화적인 인터페이스 제공

### 수동 실행

#### 1. Dry Run (미리보기)

실제로 파일을 복사하지 않고 어떤 작업이 수행될지 미리 확인:

```bash
python3 trim_sign_language_data.py --dry-run
```

#### 2. 기본 처리

F 뷰 데이터를 전처리하여 출력 디렉토리에 저장:

```bash
python3 trim_sign_language_data.py
```

#### 3. 고속 처리 (멀티프로세싱)

여러 CPU 코어를 활용한 병렬 처리:

```bash
python3 trim_sign_language_data.py --multiprocessing --workers 6
```

#### 4. 사용자 정의 경로

입력 및 출력 경로를 직접 지정:

```bash
python3 trim_sign_language_data.py \
  --data-root /path/to/SignLanguageSets \
  --output /path/to/output \
  --multiprocessing
```

## 옵션

### 기본 옵션
- `--data-root`: 입력 데이터셋의 루트 디렉토리 (기본값: `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets`)
- `--output`: 전처리된 데이터가 저장될 디렉토리 (기본값: `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed`)
- `--dry-run`: 실제로 파일을 복사하지 않고 미리보기만 수행

### 성능 옵션
- `--multiprocessing`: 멀티프로세싱을 활성화하여 병렬 처리 (2-3배 빠름)
- `--workers N`: 사용할 워커 프로세스 수 (기본값: CPU 코어 수 - 1)

### 로깅 옵션
- `--log-file`: 처리 로그를 저장할 파일 경로 (기본값: `preprocessing.log`)
- `--error-log`: 에러 로그를 저장할 파일 경로 (기본값: `preprocessing_errors.log`)

모든 옵션 보기:
```bash
python3 trim_sign_language_data.py --help
```

## 처리 과정

1. morpheme JSON 파일에서 동작의 시작(`start`)과 끝(`end`) 시간을 읽습니다
2. 비디오의 FPS를 계산합니다 (총 프레임 수 / duration)
3. 시작/끝 시간을 프레임 번호로 변환합니다
4. 시작 프레임에서 10프레임을 빼고, 끝 프레임에 10프레임을 더한 범위를 계산합니다
5. 해당 범위의 프레임만 복사하고 순차적으로 번호를 매깁니다

## 성능

### 처리 시간 예상

실제 데이터셋 기준 (약 3,000개 F-view 폴더):

| 모드 | 워커 수 | 예상 시간 | 속도 향상 |
|------|---------|-----------|-----------|
| 단일 프로세스 | 1 | 20-40분 | 1x (기준) |
| 멀티프로세싱 | 4 | 10-18분 | ~2x |
| 멀티프로세싱 | 8 | 8-12분 | ~3x |

**💡 팁**: SSD 사용 시 더 빠른 처리 속도를 경험할 수 있습니다.

## 출력 예시

```
================================================================================
Korean Sign Language Data Preprocessing
================================================================================
Data root:       /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets
Output:          /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed
Mode:            PROCESSING
Multiprocessing: Enabled
Workers:         6
Log file:        preprocessing.log
Error log:       preprocessing_errors.log

================================================================================
Processing folders: 100%|████████████████████| 960/960 [08:45<00:00, 1.82folder/s]

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

Total processing time: 0:08:45
```

## 라이선스

MIT License
KSL from AIHub pre processing
