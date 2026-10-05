# Design

Why this setup is the way it is. It is for someone who moves between an
Omarchy (Hyprland) Linux machine and a Mac every day, and wants the same hands
on both.

## Requirements

1. **Usability over looks.** Matching muscle memory matters; theming is a bonus.
   There is no custom bar, border styling or animation work.
2. **Same physical key positions.** The four keys left of space should do the
   same job on both machines. A typical Linux laptop reads Ctrl, Fn, Super, Alt;
   a MacBook reads fn, control, option, command. Fn is rarely used on Linux, so
   losing the Mac's Fn position costs nothing.
3. **Omarchy's window-management keys, unchanged.** Super+arrows,
   Super+1–9, Super+Shift+1–9, Super+Shift+Alt+1–9, Super+Tab,
   Super+Enter for a terminal, Super+Shift+Enter for a browser, and the rest of
   Omarchy's tiling bindings.
4. **Super+W closes the window**, not just a tab.
5. **Super+F makes the window take up the screen.** True fullscreen or
   "fill everything but the bar" are both fine.
6. **A scrolling layout, not dwindle.** Two windows side by side, the rest
   off-screen to the left and right, ideally with a sliver of the neighbours
   visible at the edge (like Hyprland's `scrolling` layout with
   `column_width = 0.49`).
7. **Works on a managed Mac.** Admin rights and installing apps are fine, but
   nothing that requires disabling SIP or other platform protections, since
   corporate machines don't allow it.

## Choices

### Tiler: OmniWM, falling back to Paneru

| | Scrolling | Needs SIP off | Notes |
|---|---|---|---|
| yabai | no (bsp) | for instant Space switching and moving windows between Spaces | Its SIP-off features break with macOS updates. |
| AeroSpace | no (i3 tree) | no | Excellent, but no scrolling layout. |
| **OmniWM** | **yes (niri)** | no | macOS 26+ on Apple Silicon. Full CLI, scratchpads, fullscreen, own workspaces. |
| Paneru | yes (niri) | no | Works on older macOS. No fullscreen or scratchpad; keeps a configurable sliver of off-screen windows. |
| PaperWM.spoon | yes | no | Hammerspoon/Lua; older approach. |

Requirement 6 rules out yabai and AeroSpace; requirement 7 rules out yabai's
full feature set anyway. OmniWM covers every action in requirement 3. Paneru
is the fallback for Macs that can't run it, and the better choice if a visible
sliver of off-screen windows matters more than fullscreen and scratchpads
(OmniWM parks off-screen windows with about a 1-pixel sliver).

### Keys: why Karabiner, and why Ctrl becomes right Cmd

Linux keeps two keys apart: **Ctrl** for app shortcuts (copy, find, new tab)
and **Super** for the window manager. macOS puts app shortcuts on **⌘**, so
naively binding the window manager to ⌘ collides with ⌘1–9, ⌘←→, ⌘F, ⌘T, ⌘S,
⌘L, ⌘Tab, ⌘Space and more.

The fix restores the Linux split instead of fighting it:

- The key in the Super position sends **left ⌘**. Super+C/V/X are copy,
  paste and cut, exactly as Omarchy's universal clipboard already behaves.
  Every Omarchy Super chord is caught by Karabiner and sent to the tiler.
- The key in the Ctrl position sends **right ⌘** outside terminals, so
  Ctrl+F/T/L/S/1–9 are the app shortcuts a Linux user expects. Karabiner tells
  left and right ⌘ apart, so the two layers never collide. In terminals it
  stays a real Control, so Ctrl+C interrupts.
- Ctrl+arrows/Backspace and Home/End are translated to their macOS
  equivalents (word jump, line start/end) outside terminals.

Karabiner needs a driver extension, which a managed Mac may need IT to allow.
It still beats the alternatives: macOS's Modifier Keys setting can swap keys but
can't separate the two ⌘ roles, and a Hammerspoon event tap can't reliably take
over ⌘Tab.

Bindings live in one table in `karabiner/generate.py`, the same idea as
Omarchy's `bindings.lua`; the generator writes `karabiner.json` and the Super+K
cheat sheet. `bin/wm` maps one verb set onto whichever tiler is installed, so
the bindings don't change if the tiler does.

## Trade-offs

- **macOS shortcuts given up:** ⌘Tab (Alt+Tab switches windows instead), ⌘⇧3/4/5
  screenshots (Super+Ctrl+C opens Screenshot), and the Ctrl+arrow Mission
  Control shortcuts (disabled so they don't fire in terminals).
- **Not ported:** dwindle-only bindings (Super+J, Super+P,
  Super+Ctrl+Backspace), Super+O pop-out, and Omarchy's own menus and panels.
  Super+Space is Spotlight.
- **Differences from Omarchy:** Super+Ctrl+F centres the column (no tiled
  fullscreen in OmniWM). Alt+Tab jumps back to the previous window rather than
  cycling. Super+Shift+Alt+arrows swaps workspaces between monitors rather than
  moving one.
- **Latency:** each Super chord runs a short shell command (tens of
  milliseconds). If it feels slow, frequent bindings can move into OmniWM's
  own hotkeys.

## Not yet verified on hardware

- Karabiner matching on remapped modifiers (left vs right ⌘) and remapping the
  built-in fn/🌐 key. macOS may need "Press 🌐 key to: Do Nothing".
- Super+Enter needs `karabiner_console_user_server` to have Accessibility
  permission (it sends ⌘N to the running Ghostty).
