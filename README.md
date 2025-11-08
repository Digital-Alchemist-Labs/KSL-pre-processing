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

## 설치

Python 3.6 이상이 필요합니다. 외부 라이브러리는 필요하지 않습니다.

```bash
git clone <repository-url>
cd KSL-pre-processing
```

## 사용법

### 1. Dry Run (미리보기)

실제로 파일을 복사하지 않고 어떤 작업이 수행될지 미리 확인:

```bash
python trim_sign_language_data.py --dry-run
```

### 2. 실제 처리

F 뷰 데이터를 전처리하여 출력 디렉토리에 저장:

```bash
python trim_sign_language_data.py
```

### 3. 사용자 정의 경로

입력 및 출력 경로를 직접 지정:

```bash
python trim_sign_language_data.py \
  --data-root /path/to/SignLanguageSets \
  --output /path/to/output
```

## 옵션

- `--data-root`: 입력 데이터셋의 루트 디렉토리 (기본값: `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets`)
- `--output`: 전처리된 데이터가 저장될 디렉토리 (기본값: `/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed`)
- `--dry-run`: 실제로 파일을 복사하지 않고 미리보기만 수행
- `--error-log`: 에러 로그를 저장할 파일 경로 (기본값: `preprocessing_errors.log`)

## 처리 과정

1. morpheme JSON 파일에서 동작의 시작(`start`)과 끝(`end`) 시간을 읽습니다
2. 비디오의 FPS를 계산합니다 (총 프레임 수 / duration)
3. 시작/끝 시간을 프레임 번호로 변환합니다
4. 시작 프레임에서 10프레임을 빼고, 끝 프레임에 10프레임을 더한 범위를 계산합니다
5. 해당 범위의 프레임만 복사하고 순차적으로 번호를 매깁니다

## 출력 예시

```
Korean Sign Language Data Preprocessing
Data root: /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets
Output:    /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed
Mode:      PROCESSING

Found 16 numbered folders to process
================================================================================

Processing folder 02: 60 F-view folders
  ✓ NIA_SL_WORD0001_REAL02_F: 173 → 135 frames (trimmed 38)
  ✓ NIA_SL_WORD0002_REAL02_F: 150 → 120 frames (trimmed 30)
  ...

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
```

## 라이선스

MIT License
KSL from AIHub pre processing
