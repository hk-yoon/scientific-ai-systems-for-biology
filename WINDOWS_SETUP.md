# Windows 새 가상환경 검사 절차 (아직 실행 확인 전)

PowerShell에서 저장소 루트로 이동하여:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python tools/verify_examples.py
```

실행 오류가 나면 오류 로그를 보존하고 공개 전 해결하세요. PowerShell 실행 정책 때문에 가상환경 활성화가 막힌다면 `.venv\Scripts\python.exe -m pip ...` 방식으로 직접 호출할 수 있습니다. 실제 Windows 테스트는 아직 수행하지 않았습니다.
