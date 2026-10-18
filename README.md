# Caesar Cipher GUI

A small desktop app (PyQt5) to encrypt and decrypt text with the Caesar cipher.

- Live result: the output updates while you type or change the shift.
- Shift selector with `-` / `+` buttons (hold a button to repeat), range `00`-`26`.
- Encrypt page: optional random shift.
- Reset and one-click Copy on both pages.

Made by Fadil Nurmaulid.

## Run

```bash
pip install -r requirements.txt
python app.py
```

## Test

```bash
python -m unittest discover
```

GUI tests run headless (`QT_QPA_PLATFORM=offscreen`), so no window is opened.

## Project structure

```
app.py                       entry point: loads font + stylesheet, shows the window
Caesar_Cipher_GUI.py         original single-file version, kept for reference
src/
  core/caesar_cipher.py      cipher logic (no Qt dependency)
  controllers/               connect each page to the cipher (live updates, reset, random shift)
  ui/
    main_window.py           page navigation (home / encrypt / decrypt)
    home_page.py, encrypt_page.py, decrypt_page.py   widgets only, no cipher logic
    components.py            reusable ShiftWidget and CopyrightLabel
  styles/style.qss           the whole theme
  utils/                     clipboard helper, resource paths
assets/                      font, icon, screenshots (screenshots show the older UI)
tests/                       unit tests for the cipher, widgets and controllers
```

Pages only build widgets and expose them; controllers own the behaviour; all
styling lives in `style.qss`.

## Known limitations

- Decrypt shifts letters **forward** by the selected value, exactly like the
  original app, so text encrypted with shift `N` is decrypted with `26 - N`.
- The "use manual shift" checkbox on the Decrypt page is not wired to anything yet.
- With "use random shift" the shift that was picked is not shown.
