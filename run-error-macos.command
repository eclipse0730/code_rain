#!/bin/bash
cd "$(dirname "$0")"

if [ ! -x "./CodeRain_Error" ]; then
  echo "CodeRain_Error 실행 파일을 찾을 수 없거나 실행 권한이 없습니다."
  echo "CodeRain_Error와 run-error-macos.command를 같은 폴더에 두세요."
  read -r -p "Enter 키를 누르면 종료합니다..."
  exit 1
fi

./CodeRain_Error --speed 0.003 --loop
