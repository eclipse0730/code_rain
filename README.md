# CodeRain GitHub Actions Build

GitHub Actions로 Windows용 `CodeRain.exe`와 macOS용 `CodeRain` 실행 파일을 만드는 프로젝트입니다.

## 사용 흐름

1. GitHub에 새 저장소 생성
2. 이 폴더 내용을 저장소에 업로드
3. `main` 브랜치에 push
4. GitHub Actions가 Windows/macOS 서버에서 실행 파일 자동 빌드
5. Actions 결과물에서 필요한 ZIP 다운로드
6. 상대방에게 ZIP 전달

## 맥북에서 실행할 명령어

```bash
git init
git add .
git commit -m "init coderain"
git branch -M main
git remote add origin git@github.com:eclipse0730/code_rain.git
git push -u origin main
```

## GitHub에서 다운로드

1. GitHub 저장소 접속
2. 상단 `Actions` 클릭
3. `Build Desktop Apps` 클릭
4. 가장 최근 실행 결과 클릭
5. 아래쪽 `Artifacts`에서 필요한 파일 다운로드

## Windows용 파일

`CodeRain-Windows-EXE`를 다운로드합니다.

압축을 풀면 `CodeRain_Final.zip`이 들어있습니다.

안에는 아래 파일이 들어있습니다.

```text
CodeRain.exe
run.bat
USER_GUIDE.txt
```

Windows 사용자는 `run.bat`를 더블클릭하면 됩니다.

## macOS용 파일

`CodeRain-macOS`를 다운로드합니다.

압축을 풀면 `CodeRain_macOS.zip`이 들어있습니다.

안에는 아래 파일이 들어있습니다.

```text
CodeRain
run-macos.command
USER_GUIDE_MAC.txt
```

맥 사용자는 `run-macos.command`를 더블클릭하면 됩니다.

macOS 보안 경고가 나오면 `run-macos.command`를 Control 키를 누른 채 클릭한 뒤 `열기`를 선택하세요.
