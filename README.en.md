[한국어](README.md) | [English](README.en.md)

# Insta Preview Share

This project helps when Instagram post and Reel links do not show a preview image in KakaoTalk. It validates an Instagram URL, rewrites it to `oginstagram.com`, and opens the iOS share sheet. Android users can configure the existing FixupXer app instead of installing a new app.

A thumbnail is not guaranteed for every post, and the external preview service may change or become unavailable.

## Install

- [Install and use the iOS Shortcut (Korean guide)](ios/README.md)
- [Install and configure FixupXer on Android (Korean guide)](android/README.md)

## Use

1. Open the share menu for an Instagram post or Reel.
2. On iOS, choose `Insta Preview Share`. On Android, choose `FixupXer`, then share the processed link.
3. Choose KakaoTalk and send the link.

If the iOS Shortcut receives no input, it checks the clipboard. Unsupported URLs are not transformed and produce a guidance message.

## URL example

```text
Before: https://www.instagram.com/reel/AbC123/?igsh=tracking-value&utm_source=share
After:  https://oginstagram.com/reel/AbC123/
```

Post links keep the `/p/` path and Reel links keep `/reel/`. Query parameters, including `igsh`, `exln`, `psln`, and `utm_source`, are removed. Only `instagram.com` and `www.instagram.com` post and Reel URLs are accepted.

## KakaoTalk preview example

In some observed cases, a converted Reel link displayed a title and image in KakaoTalk. A link card may look like this:

```text
[Post title]
[Post thumbnail]
https://oginstagram.com/reel/AbC123/
```

This is an explanatory text example, not a screenshot. KakaoTalk may show only the link if the post or external preview service does not provide a title or image.

## Privacy and external services

- This project does not operate a backend, crawler, or URL store, and does not ask for Instagram login details.
- The Shortcut or FixupXer performs the URL transformation.
- Converted links use the `oginstagram.com` domain. The recipient and KakaoTalk receive the link, and an external request may be made to generate a preview.
- This project does not operate the external preview service or control its data practices or availability. Do not share sensitive links.

See [troubleshooting](docs/troubleshooting.md) for limitations and recovery steps.

## Support and limitations

- Prioritized paths: Instagram posts (`/p/`) and Reels (`/reel/`)
- Allowed hosts: `instagram.com` and `www.instagram.com`
- No login, project backend, or new Android app is required.
- Other Instagram paths, lookalike domains, and malformed URLs are not transformed.
- Previews depend on KakaoTalk, Instagram, and the external service.
- The signed Shortcut opened to an import preview on Mac. Editing and running it, installation on an iPhone, Android sharing, and KakaoTalk previews on physical devices have not been verified.

## Source and license

This project is forked from [alexander-zolkin/iOS-Instagram-share-shortcut](https://github.com/alexander-zolkin/iOS-Instagram-share-shortcut). It preserves the original Git history and Apache-2.0 license. The original shortcut remains unchanged at the repository root as `ShareFromInstagram.shortcut`. The original screenshots may show outdated behavior and are not used in current installation instructions.

---

🤖 본 문서는 AI가 작성했습니다.
