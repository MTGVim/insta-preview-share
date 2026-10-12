[한국어](README.md) | [English](README.en.md)

# Insta Preview Share

Instagram 게시물과 릴스 링크를 카카오톡에 보낼 때 미리보기 이미지가 표시되지 않는 경우를 줄이기 위한 프로젝트입니다. Instagram 공유 링크를 검증한 뒤 `oginstagram.com` 주소로 바꾸고, iOS에서는 공유 메뉴를 엽니다. Android에서는 새 앱을 만들지 않고 FixupXer의 사용자 지정 프런트엔드를 이용합니다.

모든 게시물에서 썸네일이 표시되거나 외부 서비스가 계속 운영된다고 보장하지는 않습니다.

## 설치

- [iOS 단축어 설치 및 사용](ios/README.md)
- [Android FixupXer 설치 및 설정](android/README.md)

## 사용 방법

1. Instagram에서 게시물 또는 릴스의 공유 메뉴를 엽니다.
2. iOS에서는 `Insta Preview Share`를 선택합니다. Android에서는 `FixupXer`를 선택한 뒤 변환된 링크를 공유합니다.
3. 카카오톡을 선택해 링크를 전송합니다.

iOS에서 공유 입력이 없으면 단축어는 클립보드의 내용을 확인합니다. 지원하지 않는 URL은 변환하지 않고 안내를 표시합니다.

## URL 예시

```text
변환 전: https://www.instagram.com/reel/AbC123/?igsh=tracking-value&utm_source=share
변환 후: https://oginstagram.com/reel/AbC123/
```

게시물은 `/p/` 경로로, 릴스는 `/reel/` 경로로 유지합니다. `igsh`, `exln`, `psln`, `utm_source`를 포함한 쿼리는 제거합니다. `instagram.com` 또는 `www.instagram.com`의 게시물·릴스 URL만 변환합니다.

## 카카오톡 미리보기 예시

일부 확인 사례에서는 변환된 릴스 링크를 카카오톡에 보냈을 때 제목과 이미지가 표시됐습니다. 예를 들어 카카오톡에는 다음과 같은 링크 카드가 나타날 수 있습니다.

```text
[게시물 제목]
[게시물 썸네일 이미지]
https://oginstagram.com/reel/AbC123/
```

위 내용은 설명용 예시이며 실제 화면을 캡처한 자료가 아닙니다. 카카오톡과 외부 미리보기 서비스가 해당 게시물의 제목이나 이미지를 제공하지 않으면 링크만 표시될 수 있습니다.

## 개인정보와 외부 서비스

- 이 프로젝트는 자체 백엔드, 크롤러, URL 저장소를 운영하지 않으며 Instagram 로그인 정보도 요구하지 않습니다.
- URL 변환은 단축어 또는 FixupXer에서 수행합니다.
- 변환된 URL에는 `oginstagram.com` 도메인이 포함됩니다. 링크를 공유하면 받는 사람과 카카오톡이 URL을 받으며, 미리보기를 만들기 위해 외부 서비스에 요청할 수 있습니다.
- 외부 미리보기 서비스의 운영 주체, 기록 정책, 가용성은 이 프로젝트가 관리하지 않습니다. 민감한 링크는 공유하지 마세요.

자세한 제한과 문제 해결 방법은 [문제 해결 안내](docs/troubleshooting.md)를 참고하세요.

## 지원 범위와 제한

- 우선 지원: Instagram 게시물(`/p/`)과 릴스(`/reel/`)
- 허용 호스트: `instagram.com`, `www.instagram.com`
- 로그인, 별도 백엔드, Android 신규 앱은 필요하지 않습니다.
- Instagram의 다른 경로, 유사 도메인, 잘못된 주소는 변환하지 않습니다.
- 미리보기는 KakaoTalk, Instagram, 외부 서비스의 정책과 가용성에 따라 달라질 수 있습니다.
- Mac에서 단축어 파일을 공개 배포용으로 서명하고 가져오기 미리보기를 확인했습니다. 편집 및 실행, iPhone 설치, Android 공유, 카카오톡 실기기 썸네일은 아직 검증하지 않았습니다.

## 출처와 라이선스

이 프로젝트는 [alexander-zolkin/iOS-Instagram-share-shortcut](https://github.com/alexander-zolkin/iOS-Instagram-share-shortcut)에서 포크했으며 기존 Git 이력과 Apache-2.0 라이선스를 보존합니다. 기존 스크린샷은 이전 동작을 보여 줄 수 있어 현재 설치 안내에는 사용하지 않습니다.

---

🤖 본 문서는 AI가 작성했습니다.
