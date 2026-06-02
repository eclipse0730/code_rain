#!/bin/bash
cd "$(dirname "$0")"

if [ ! -x "./CodeRain" ]; then
  echo "CodeRain 실행 파일을 찾을 수 없거나 실행 권한이 없습니다."
  echo "CodeRain과 run-macos.command를 같은 폴더에 두세요."
  read -r -p "Enter 키를 누르면 종료합니다..."
  exit 1
fi

./CodeRain --theme ai --speed 0.0015 --loop --noise
