[한국어](../README.md) | [English](../README.en.md) | [Android 안내](../android/README.md) | [문제 해결](../docs/troubleshooting.md)

# iOS 설치 및 사용

## 단축어 파일

저장소의 [Insta Preview Share.shortcut](Insta%20Preview%20Share.shortcut) 파일을 사용합니다. 파일은 `shortcuts sign --mode anyone`으로 서명되어 있습니다. 서명은 가져오기 가능성을 위한 절차이며, 실제 iPhone에서 설치와 실행을 확인했다는 뜻은 아닙니다.

1. 저장소에서 단축어 파일을 내려받습니다.
2. 파일을 iPhone에서 열어 단축어 앱에 추가합니다. iOS가 추가 확인을 표시하면 내용을 확인한 뒤 진행합니다.
3. Instagram에서 게시물 또는 릴스를 공유하고 공유 시트에서 `Insta Preview Share`를 선택합니다.
4. 단축어가 변환한 URL을 복사하고 iOS 공유 메뉴를 엽니다. 받는 앱으로 카카오톡을 선택합니다.

Apple의 안내에 따르면 공개 배포용 서명은 누구나 단축어를 가져올 수 있게 하며, Apple은 변조를 방지하기 위한 확인용 사본을 받습니다. [Apple의 단축어 서명 안내](https://support.apple.com/ko-kr/guide/shortcuts-mac/apd455c82f02/mac)를 참고하세요.

## 클립보드 대체 사용법

Instagram에서 게시물 링크를 복사한 뒤 단축어 앱에서 `Insta Preview Share`를 실행합니다. 공유 시트 입력이 없으면 단축어가 클립보드 내용을 확인하도록 설정했습니다. 유효한 게시물 또는 릴스 링크를 찾지 못하면 안내를 표시합니다.

## 단축어가 공유 시트에 보이지 않을 때

이 단축어는 공유 시트에서 실행할 수 있도록 구성했습니다. Instagram에서 전달하는 입력 형식이나 iOS 버전에 따라 표시 방식이 달라질 수 있습니다. 먼저 링크를 복사한 다음 단축어 앱에서 실행하는 클립보드 방법을 사용해 보세요. 이 저장소에서는 iPhone 실기기에서 메뉴 경로와 표시 여부를 확인하지 않았습니다.

Mac에서는 Apple이 안내하는 방법으로 `.shortcut` 파일을 두 번 클릭하거나 단축어 앱 창으로 드래그해 가져올 수 있습니다. [Apple의 Mac 단축어 가져오기 안내](https://support.apple.com/en-asia/guide/shortcuts-mac/apd02bffbaac/mac)를 참고하세요.

## 검증 상태

- 자동화 테스트는 게시물·릴스 URL, 허용 호스트, 추적 쿼리 제거, 유사 도메인과 잘못된 경로를 확인합니다.
- 공개 배포용 서명은 Mac에서 성공했습니다.
- Mac에서 파일을 열면 `Insta Preview Share`와 `단축어 추가`가 보이는 가져오기 미리보기가 나타났습니다.
- Orca가 Shortcuts 창을 포커스하지 못해 실제 가져오기, 편집, 실행은 확인하지 못했습니다.
- iPhone 설치, Instagram 공유 시트 실행, 카카오톡 썸네일은 실기기에서 검증하지 않았습니다.

---

🤖 본 문서는 AI가 작성했습니다.
