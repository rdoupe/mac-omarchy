# Agent notes

Read [DESIGN.md](DESIGN.md) first. Its **Requirements** section is the brief
for this repo. Treat those points as settled decisions. Don't re-ask the user
about them or trade them away without asking: same physical key positions as
Linux, Omarchy's Super bindings unchanged, Super+W closes the window, Super+F
fills the screen, scrolling layout, no SIP changes, usability over looks.

## Working on the Mac

- Install with `./bootstrap.sh`. Re-run it after OmniWM's first launch.
- Change bindings in `karabiner/generate.py`, run it, then re-run
  `bootstrap.sh` (or copy `karabiner/karabiner.json` to
  `~/.config/karabiner/`). Never hand-edit `karabiner.json`.
- `bin/wm` is the only place that knows tiler command names. Test a verb
  directly, e.g. `~/.local/bin/wm focus left`.
- OmniWM's `~/.config/omniwm/settings.toml` has a strict schema. Edit values
  in place; never write it from scratch (a missing key rejects the whole file).
- The machine is corporate-managed. Don't disable SIP or other protections,
  and don't change MDM, VPN, firewall or network settings.

## Verify first (written blind, never run on a Mac)

1. Karabiner-EventViewer: with the option key (Super position) held, the
   window-manager rules must see `left_command`. With the fn key (Ctrl position)
   held outside a terminal, they must see `right_command`. Everything depends on this.
2. The built-in fn/🌐 key can be remapped. If macOS grabs it, set System
   Settings > Keyboard > "Press 🌐 key to" > Do Nothing.
3. Super+1–9, Super+arrows, Super+F, Super+W, Super+Enter and
   Super+Shift+Enter all work, and the speed is acceptable. Each runs a shell
   command; if it feels sluggish, move focus/workspace keys into OmniWM's own
   hotkeys.
4. Super+Enter needs `karabiner_console_user_server` to have Accessibility
   permission.
5. Two columns sit side by side and the rest scroll off-screen.

Record anything learned on the hardware in DESIGN.md, under "Not yet verified
on hardware", and remove items once they are confirmed.
