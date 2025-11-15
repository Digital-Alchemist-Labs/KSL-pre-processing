#!/bin/bash
# Korean Sign Language Data Preprocessing - Quick Start Script

echo "=================================================="
echo "한국 수어 데이터 전처리 도구"
echo "Korean Sign Language Data Preprocessing"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3가 설치되어 있지 않습니다."
    echo "   Python 3를 먼저 설치해주세요."
    exit 1
fi

# Check if required packages are installed
echo "📦 의존성 패키지 확인 중..."
python3 -c "import tqdm" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  tqdm 패키지가 설치되어 있지 않습니다."
    echo "   패키지를 설치하시겠습니까? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "📦 패키지 설치 중..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ 패키지 설치 실패"
            exit 1
        fi
        echo "✅ 패키지 설치 완료"
    else
        echo "❌ 필수 패키지가 없어 실행할 수 없습니다."
        exit 1
    fi
fi

echo ""
echo "실행 모드를 선택하세요:"
echo "1) Dry Run (미리보기 - 파일 복사 없음)"
echo "2) 기본 처리 (단일 프로세스)"
echo "3) 고속 처리 (멀티프로세싱)"
echo ""
read -p "선택 (1-3): " mode

case $mode in
    1)
        echo ""
        echo "🔍 Dry Run 모드로 실행합니다..."
        python3 trim_sign_language_data.py --dry-run
        ;;
    2)
        echo ""
        echo "⚙️  기본 처리 모드로 실행합니다..."
        python3 trim_sign_language_data.py
        ;;
    3)
        echo ""
        read -p "워커 수를 입력하세요 (권장: 4-8, 기본값: 자동): " workers
        if [ -z "$workers" ]; then
            echo "🚀 고속 처리 모드로 실행합니다 (자동 워커 수)..."
            python3 trim_sign_language_data.py --multiprocessing
        else
            echo "🚀 고속 처리 모드로 실행합니다 ($workers 워커)..."
            python3 trim_sign_language_data.py --multiprocessing --workers "$workers"
        fi
        ;;
    *)
        echo "❌ 잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "처리 완료!"
echo "=================================================="
echo ""
echo "📄 생성된 파일:"
echo "   - processing.log (처리 로그)"
echo "   - preprocessing_errors.log (에러 로그, 에러 발생 시)"
echo ""
echo "📁 출력 디렉토리:"
echo "   /Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed"
echo ""

