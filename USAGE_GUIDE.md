# 한국 수어 데이터 전처리 사용 가이드

## 빠른 시작

### 1단계: Dry Run으로 확인

실제 파일을 복사하지 않고 어떤 작업이 수행될지 미리 확인합니다:

```bash
python trim_sign_language_data.py --dry-run
```

이 명령은 다음을 보여줍니다:
- 처리될 F 뷰 폴더의 수
- 각 폴더에서 몇 개의 프레임이 유지되고 제거될지
- 전체 통계 (원본/처리 후 프레임 수, 감소율)
- 에러가 발생한 파일 목록

### 2단계: 실제 처리

Dry run 결과가 만족스럽다면 실제 처리를 수행합니다:

```bash
python trim_sign_language_data.py
```

## 상세 옵션

### 데이터 경로 지정

기본 경로가 아닌 다른 경로를 사용하려면:

```bash
python trim_sign_language_data.py \
  --data-root /path/to/your/SignLanguageSets \
  --output /path/to/output/directory
```

### 에러 로그 저장

에러 로그를 특정 위치에 저장:

```bash
python trim_sign_language_data.py \
  --error-log /path/to/errors.log
```

### 전체 옵션 조합 예제

```bash
python trim_sign_language_data.py \
  --data-root /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets \
  --output /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Processed \
  --error-log processing_errors.log
```

## 처리 시간 예상

- 약 3,000개의 F 뷰 폴더 처리
- 각 폴더당 평균 100-200개의 JSON 파일
- 예상 처리 시간: 10-30분 (시스템 성능에 따라 다름)

## 출력 구조

처리된 데이터는 다음과 같은 구조로 저장됩니다:

```
SignLanguageSets_Trimmed/
└── 02/
    ├── NIA_SL_WORD0001_REAL02_F/
    │   ├── NIA_SL_WORD0001_REAL02_F_000000000000_keypoints.json
    │   ├── NIA_SL_WORD0001_REAL02_F_000000000001_keypoints.json
    │   └── ...
    └── ...
```

## 주의사항

1. **충분한 저장 공간 확보**: 처리된 데이터는 원본의 약 60%를 차지합니다.

2. **백업 권장**: 원본 데이터는 수정되지 않지만, 작업 전 중요 데이터는 백업하는 것이 좋습니다.

3. **에러 파일**: 일부 파일(약 56개)은 morpheme 메타데이터가 없어 처리되지 않습니다. 이는 정상적인 현상입니다.

4. **처리 중단**: 처리 중 Ctrl+C로 중단할 수 있으며, 이미 복사된 파일은 유지됩니다.

## 트러블슈팅

### "Morpheme file not found" 에러

일부 키포인트 폴더에 대응하는 morpheme JSON 파일이 없는 경우 발생합니다. 이는 정상적이며 해당 폴더는 건너뜁니다.

### "list index out of range" 에러

morpheme JSON 파일의 `data` 배열이 비어있는 경우 발생합니다. 이 파일도 건너뜁니다.

### 처리 속도가 느린 경우

- SSD 사용 권장
- 다른 프로그램을 종료하여 I/O 리소스 확보
- 충분한 디스크 공간 확보

## 도움말

모든 옵션 보기:

```bash
python trim_sign_language_data.py --help
```

## 문의

문제가 발생하면 `preprocessing_errors.log` 파일을 확인하여 에러 내용을 파악하세요.

