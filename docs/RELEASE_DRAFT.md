# Release draft: Genius 3D Chess & Autonomous Diary

Tag: v1.0.0 (placeholder)
Title: Genius 3D Chess & Autonomous Diary v1.0.0

Summary
-------

This release bundles two Windows desktop applications built with PyInstaller:

- `Genius3DChess.exe` — Battle chess with 8 celebrity opponents, offline AI, Tkinter UI.
- `AutonomousDiary.exe` — Offline AI-powered personal diary with sentiment analysis and a chatbot assistant.

Highlights
----------

- Full chess engine with move validation and 8 AI personalities.
- Local JSON persistence for diary entries; includes sentiment analytics and chat assistant.
- Both apps are packaged as single-file Windows executables (`.exe`) using PyInstaller.

Installation
------------

1. Download the `.exe` for the app you want.
2. Double-click to run. Windows SmartScreen or antivirus may require an explicit "Run anyway".
3. Diary data is stored at `diary_data/entries.json` relative to the installation directory when run from source; for the packed exe, entries are saved to the working directory.

Known issues
------------

- Some antivirus/SmartScreen warnings can occur for unsigned executables. Scanning before running is recommended.
- This initial release is single-user, local-only (no cloud sync).

Changelog (summary)
-------------------

- Initial public release: packaged chess and diary apps, documentation and web downloads page.

Notes for release assets
------------------------

Include these files as release assets:

- `dist/Genius3DChess.exe`
- `dist/AutonomousDiary.exe`

Suggested `gh` CLI command
--------------------------

If you have the GitHub CLI installed and authenticated (`gh auth login`), run:

```powershell
gh release create v1.0.0 dist/Genius3DChess.exe dist/AutonomousDiary.exe \
  --title "Genius 3D Chess & Autonomous Diary v1.0.0" \
  --notes-file docs/RELEASE_DRAFT.md
```

If you prefer the web UI: Go to the repository → Releases → Draft a new release. Set the tag, title, paste release notes, and upload the `.exe` files.

License / Legal
---------------

Ensure you have the rights to distribute any likenesses or personalities used in the game opponents. Consider replacing or licensing likenesses before public release if necessary.
