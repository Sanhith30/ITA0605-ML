# Chrome extension

Manifest V3 browser extension for inspecting the active tab and presenting phishing-risk information. `background.js` manages extension-wide badge/background behaviour, while `popup.html` and `popup.js` implement the user-facing diagnostic panel. `manifest.json` declares permissions and entrypoints; `icons/` contains the extension icons.

Load this folder through Chrome’s **Load unpacked** option while the backend API is running.
