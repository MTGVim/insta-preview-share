[한국어](../README.md) | [English](../README.en.md) | [iOS 안내](../ios/README.md) | [문제 해결](../docs/troubleshooting.md)

# Android 설치 및 설정

Android에서는 신규 앱을 만들지 않고 기존 [FixupXer](https://github.com/NeatCode-Labs/fixupxer)를 사용합니다. FixupXer는 URL을 기기에서 처리하며, 변환된 링크를 외부 앱이나 서비스로 전달하는 시점은 사용자가 공유나 열기를 선택한 뒤입니다. [공식 README](https://github.com/NeatCode-Labs/fixupxer#readme)에서 현재 안내를 확인하세요.

## 설치

공식 배포 경로 중 하나를 선택합니다.

- [Google Play](https://play.google.com/store/apps/details?id=com.fixupxer)
- [F-Droid](https://f-droid.org/packages/com.fixupxer/)
- [GitHub 최신 릴리스](https://github.com/NeatCode-Labs/fixupxer/releases/latest)

## 사용자 지정 Instagram 도메인

FixupXer 공식 README는 Instagram용 내장 또는 사용자 지정 프런트엔드를 지원한다고 설명합니다. 현재 공식 안내에 적힌 영어 설정 경로는 다음과 같습니다.

`Settings > Link processing > Alternative frontends`

1. 프런트엔드 선택기에서 Instagram을 찾습니다.
2. 사용자 지정 도메인으로 `oginstagram.com`을 추가합니다.
3. 채팅 미리보기를 위한 `Embed frontends` 영역에서 이 도메인을 선택합니다.
4. 공유에 사용할 `Main/Share` 선택과 브라우저용 `Browser` 선택은 별도입니다. 카카오톡에 보낼 링크만 바꾸려면 `Main/Share` 쪽을 확인합니다.

위 경로와 용어는 FixupXer 공식 README의 현재 안내를 옮긴 것입니다. 이 저장소에서는 Android 실기기의 화면과 한국어 번역을 확인하지 않았습니다. 앱 버전에 따라 화면이 달라지면 [공식 README](https://github.com/NeatCode-Labs/fixupxer#readme)와 앱의 현재 안내를 우선하세요.

## Instagram에서 카카오톡으로 공유하기

1. Instagram에서 게시물이나 릴스의 공유 메뉴를 엽니다.
2. 앱 목록에서 FixupXer를 선택합니다.
3. 처리 결과를 확인한 뒤 복사하거나 공유합니다.
4. 카카오톡을 선택해 전송합니다.

선택한 외부 프런트엔드가 작동하지 않으면 원본 링크를 유지하거나 다른 프런트엔드를 선택할 수 있습니다. 모든 게시물에서 카카오톡 미리보기가 표시되는 것은 아닙니다.

## 설정 백업과 개인정보

FixupXer [공식 README](https://github.com/NeatCode-Labs/fixupxer#readme)는 `Settings > Backup & restore`에서 Android 파일 선택기를 사용해 버전이 있는 JSON을 내보내고 복원한다고 안내합니다. 설명된 백업에는 허용된 설정, 사용자 규칙, 브라우저 대상이 포함됩니다. 이 저장소에서는 실제 Android 화면을 확인하지 않았으며, `oginstagram.com` 선택이 백업되는지도 검증하지 않았습니다. 이 저장소에는 검증되지 않은 설정 파일을 포함하지 않습니다. 백업 파일을 다른 사람에게 보내기 전에 내용을 확인하세요.

FixupXer는 링크 처리를 오프라인에서 수행한다고 안내하지만, 사용자가 변환한 링크를 공유하거나 열면 선택한 외부 앱·브라우저·미리보기 서비스가 네트워크 요청을 할 수 있습니다. FixupXer와 외부 서비스는 별도 운영 주체입니다.

---

🤖 본 문서는 AI가 작성했습니다.
