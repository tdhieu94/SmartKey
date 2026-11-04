# SmartKey

SmartKey là bộ gõ tiếng Việt (Telex) cho Windows, macOS và Linux, dựa trên [Vikey](https://github.com/tonyminibot/Vikey) của Tony Dinh. Ngoài tự chuyển Anh/Việt như Vikey, SmartKey **tự sửa lỗi gõ Telex** khi gõ nhanh (hợp với dân lập trình): `rtinhf` → trình, `tooin` → tôi, `ddnag` → đang. Từ tiếng Anh và tên biến trong code được giữ nguyên.

**Tải về:** [bản mới nhất](https://github.com/tdhieu94/SmartKey/releases/latest). Windows và macOS tự cập nhật mỗi ngày; Linux báo khi có bản mới.

**Phát hành bản mới:** tăng `MARKETING_VERSION` trong `project.yml`, ghi thay đổi vào `RELEASE_NOTES.md`, rồi merge vào main. GitHub Actions build cả ba hệ điều hành, ký bản cập nhật (secret `SPARKLE_ED_KEY`) và tự đăng release kèm `appcast.xml` / `release.json`.

---

## Vikey (upstream)

Vietnamese typing for macOS, Windows, Linux, iOS and Android that switches between Vietnamese and English for you.

Made by [Tony Dinh](https://tonydinh.com) (Đinh Quang Trung, [@trungdq88](https://github.com/trungdq88)). Free and open source under GPL-3.0; based on [OpenKey](https://github.com/tuyenvm/OpenKey) by Tuyen Mai.

Type Telex as usual. When you type an English word in Vietnamese mode, or a Vietnamese word in English mode, Vikey fixes the word and switches the language. No more pressing the switch key every few words.

## Features

- **Telex** with modern or classic tone placement (hoà / hòa), spell checking, and keeping your keys as typed when a word isn't Vietnamese.
- **Auto switch:**
  - `more` → stays English;
  - `treen` → `trên`;
  - `truowfng`, `truongwf`, `truwownfg` → `trường`;
  - `this makes sense` comes out right in Vietnamese mode, because ambiguous words are fixed once the context is clear.
- **Typo fix:** `rtinhf` → `trình`, `tooin` → `tôi`, `ddnag` → `đang` (two keys swapped, an extra key or a neighbouring key), never on English words or code.
- **Programming-aware:**
  - `var`, `const`, `git push`, `obj.dir` and `my_var` are left alone.
- **Undo:** press Delete right after an automatic fix to undo it.
- **Remembers the language** for each app, and for each website in Chrome, Safari, Arc, Brave, Edge, Vivaldi and Opera.
- **Switch hotkey:** a key with modifiers, or modifiers alone (⌃⇧), with an optional beep.
- **Works with Dvorak and other layouts:** Vikey steps aside automatically for other input languages (Japanese, Chinese…).

## Build

Requires Xcode and [XcodeGen](https://github.com/yonaskolb/XcodeGen).

```sh
xcodegen generate
xcodebuild -project Vikey.xcodeproj -scheme Vikey -configuration Release build
```

Vikey needs Accessibility permission (to read and rewrite keystrokes). On first launch it walks you through granting it.

## Debug typing log

For tuning auto switch, turn on Gỡ lỗi → Ghi nhật ký gõ in the menu bar. It counts manual vs automatic switches and (optionally) records the keys of each word to `~/Library/Application Support/Vikey/typing-log.jsonl`, never in password fields, password managers or terminals. Off by default. Analyze with `Tools/autoswitch/analyze_log.py`.

## Engine tests

Every typing rule is locked down by tests: rule-tagged cases, golden snapshots of typing a mixed Vietnamese/English corpus, and every Vietnamese syllable.

```sh
Tools/autoswitch/check.sh
```

See [DECISIONS.md](DECISIONS.md) for every rule and why it exists.

## Contributing

Pull requests are welcome, AI-written code included. Show the problem with a screenshot or video, describe the
before and after, and add test cases. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License and credits

Vikey is based on [OpenKey](https://github.com/tuyenvm/OpenKey) by Tuyen Mai, and is distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
