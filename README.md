# Scientific AI Systems for Biology — Code Companion

**상태: 공개 전 권리 확인 대기 (Apache-2.0 적용 후보).**

이 저장소는 13개 Chapter의 코드 부속자료로, 저작물의 출판 기준은 Microsoft Word 원고입니다.

## 코드 유형
- `examples/`: 독립 실행 프로그램. 실행 성공은 과학적 타당성이나 원고와의 완전 일치를 보증하지 않습니다.
- `snippets/`: 설명용 코드 조각이며 독립 실행이 **보장되지 않고**, 개별 실행 **검증을 하지 않았을 수 있습니다**.
- `pseudocode/`: 의사코드로 **실행용 Python이 아닙니다**.

이 배포 후보에는 원고의 **손상 코드 및 자동 추출한 미확인 후보를 넣지 않았습니다.** 이러한 자료는 별도의 내부 감사 폴더에 보존됩니다.

## 실행 환경
Python 3.11 가상환경 권장. `requirements.txt`의 패키지 설치 후 `python tools/verify_examples.py` 실행. Windows PowerShell에서도 동일하게 실행할 수 있습니다. 그래픽 출력이나 시스템에 따라 세부 차이가 있을 수 있습니다.

## 공개 승인 조건
1. 각 코드의 작성권 및 외부 코드·데이터 출처 확인
2. **Apache License 2.0 채택 및 LICENSE 전문 포함 완료**. 단, 제3자 자료에 적용할 권한은 별도 확인 필요
3. **Windows Anaconda 환경에서 10/10 PASS (사용자 제공 실행 화면, 2026-10-17)**. Python 3.11 별도 설치 방식의 검증은 아님
4. README·코드 스니펫 내용의 최종 검토

**현재 GitHub push, tag, release를 하지 마십시오.**


## 공개 승인 상태

이 저장소는 **검토 후보(HOLD)**이며 공개 승인이 아닙니다. 세부 조건은 `PUBLICATION_GATE.md`에 있습니다. 실행 시 생성되는 결과물은 저장소에 포함하지 않았습니다.
