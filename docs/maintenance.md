[한국어](../README.md) | [English](../README.en.md) | [문제 해결](troubleshooting.md)

# 유지보수

## 기본 변환 도메인 변경

1. `ios/build_shortcut.py`의 `DEFAULT_DOMAIN` 값을 새 DNS 호스트명으로 바꿉니다.
2. `README.md`, `README.en.md`, `ios/README.md`, `android/README.md`, `docs/troubleshooting.md`의 URL 예시와 설정 안내를 함께 갱신합니다.
3. 다음 명령으로 단축어를 다시 생성하고 서명합니다.

   ```bash
   python3 ios/build_shortcut.py
   ```

   이 스크립트는 원본에서 추출해 보존한 `ios/upstream-template.wflow`를 바탕으로 작업 흐름을 생성하고, `shortcuts sign --mode anyone`을 호출해 `ios/Insta Preview Share.shortcut`을 만듭니다.

4. 자동화 테스트를 실행하고, 생성된 파일을 Mac용 단축어 앱에서 가져와 편집 가능한지 확인합니다. Apple은 `.shortcut` 파일을 앱에서 열거나 창으로 드래그해 가져오는 방법을 안내합니다. [가져오기 안내](https://support.apple.com/en-asia/guide/shortcuts-mac/apd02bffbaac/mac)를 참고하세요.
5. 공개 배포용 서명은 [Apple의 `shortcuts sign` 안내](https://support.apple.com/ko-kr/guide/shortcuts-mac/apd455c82f02/mac)에 따라 확인합니다. 서명 성공과 iPhone 설치 성공은 별개입니다.

단축어 편집기에서 직접 바꾸는 경우에는 서명된 바이너리를 직접 수정하지 마세요. Apple의 [파일로 내보내기 절차](https://support.apple.com/en-ie/guide/shortcuts-mac/apdf01f8c054/mac)를 거친 뒤 테스트와 재서명을 진행합니다. 이 저장소의 현재 빌드 경로는 Mac UI 편집이 아니라 원본 작업 흐름 템플릿과 생성 스크립트입니다.

`ios/upstream-template.wflow`는 포크 당시 원본 단축어에서 추출한 템플릿입니다. upstream이 바뀌면 원본 `.shortcut`과 템플릿을 함께 비교하고, 생성 스크립트의 입력 및 공유 흐름도 다시 검증합니다.

## 외부 미리보기 서비스 장애

- `oginstagram.com` 주소를 만드는 URL 테스트가 계속 통과하는지 확인합니다.
- 서비스 운영 상태와 카카오톡 미리보기 결과를 실제 기기에서 확인합니다.
- 도메인을 바꿀 때는 해당 서비스의 정책과 가용성을 확인하고, 게시물 식별자가 보존되는지 검증합니다.
- README와 Android 설정 예시를 함께 갱신합니다.
- 서비스 장애나 정책 변경이 확인되지 않았다면 썸네일 표시 성공을 일반화하지 않습니다.

## 파일 갱신과 배포 전 점검

- `python3 -B -m unittest discover -s ios/tests -v`를 실행합니다.
- `python3 ios/build_shortcut.py`로 서명 파일을 갱신합니다.
- Mac 단축어 앱에서 파일을 열고 가져오기 미리보기를 확인합니다.
- 단축어 편집과 실행을 확인하고, 가능한 경우 실제 iPhone에서 설치·공유 시트·클립보드 대체 동작을 검사합니다.
- Android 공식 FixupXer 설정 화면에서 사용자 지정 Instagram 도메인과 `Main/Share` 선택을 확인합니다.
- iPhone과 Android에서 각각 카카오톡으로 공유해 제목과 썸네일을 확인합니다.
- 확인하지 못한 기기 동작은 문서에서 미검증으로 남깁니다.

---

🤖 본 문서는 AI가 작성했습니다.
