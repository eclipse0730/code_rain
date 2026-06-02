# CodeRain GitHub Actions Build

맥북에서 Windows용 CodeRain.exe를 만들기 위한 GitHub Actions 프로젝트입니다.

## 사용 흐름

1. GitHub에 새 저장소 생성
2. 이 폴더 내용을 저장소에 업로드
3. `main` 브랜치에 push
4. GitHub Actions가 Windows 서버에서 EXE 자동 빌드
5. Actions 결과물에서 `CodeRain_Final.zip` 다운로드
6. 상대방에게 `CodeRain_Final.zip` 전달

## 맥북에서 실행할 명령어

```bash
git init
git add .
git commit -m "init coderain"
git branch -M main
git remote add origin git@github.com:eclipse0730/code_rain.git
git push -u origin main
```

## GitHub에서 EXE 다운로드

1. GitHub 저장소 접속
2. 상단 `Actions` 클릭
3. `Build Windows EXE` 클릭
4. 가장 최근 실행 결과 클릭
5. 아래쪽 `Artifacts`에서 `CodeRain-Windows-EXE` 다운로드
6. 압축을 풀면 `CodeRain_Final.zip`이 들어있음

## 최종 사용자에게 전달할 파일

`CodeRain_Final.zip`

안에는 아래 파일이 들어있습니다.

```text
CodeRain.exe
run.bat
USER_GUIDE.txt
```

상대방은 `run.bat`만 더블클릭하면 됩니다.
