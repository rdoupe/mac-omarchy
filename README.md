# mac-omarchy

Make a MacBook work like the Omarchy laptop: Linux key positions, Omarchy's
Super shortcuts, and a scrolling tiling layout. No SIP changes.

```bash
git clone https://github.com/rdoupe/mac-omarchy ~/mac-omarchy && ~/mac-omarchy/bootstrap.sh
```

Run it again after OmniWM's first launch; it then configures OmniWM. The
script ends with the permission prompts you have to click through yourself.

## Keys

| Position left of space | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| MacBook prints | fn | control | option | command |
| Behaves as | Ctrl | Fn | Super | Alt |

- **Super** sends ⌘, so Super+C/V/X/Q/H are native. Super+W closes the window.
  Every other Omarchy Super chord drives the tiler (Super+K lists them).
- **Ctrl** is the app-shortcut key, as on Linux: Ctrl+F/T/L/S/R, Ctrl+Tab,
  Ctrl+arrows (word jump), Ctrl+Backspace. In terminals it stays a real Control.
- **Fn**+arrows are Home/End/PgUp/PgDn; Home/End go to line start/end.
- A PC keyboard (Ctrl, Win, Alt) needs no swap and gets the same shortcuts.

## Pieces

| Path | What |
|---|---|
| `karabiner/generate.py` | The bindings table. Edit it, run it, and it writes `karabiner.json` and `keybindings.txt`. |
| `bin/wm` | One verb set (`wm focus left`, `wm workspace 3`, ...) for OmniWM or Paneru. |
| `tiler/paneru.toml` | Paneru config, used when the Mac can't run OmniWM. |
| `ghostty/config` | Ghostty matched to the laptop. |

**Tiler:** OmniWM on macOS 26+ with Apple Silicon, otherwise Paneru. Paneru has no
fullscreen (Super+F becomes full width), no scratchpad and no former-workspace
key, and Super+Shift+Alt+arrows moves the window, not the workspace, to the
next display.

**Lost macOS shortcuts:** ⌘Tab (Super+Tab is next workspace; Alt+Tab switches
windows), ⌘1–9 browser tabs (use Ctrl+1–9), ⌘⇧3/4/5 screenshots (Super+Ctrl+C
opens Screenshot), and Ctrl+arrow Mission Control.
