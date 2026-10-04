#!/usr/bin/env python3
"""Generate karabiner.json: Omarchy's keyboard on a MacBook.

Physical keys left of space, and what each becomes (Linux layout order):

    MacBook built-in:  [fn] [control] [option] [command]
    becomes:           Ctrl   Fn      SUPER     Alt
    (a PC keyboard already reads Ctrl, SUPER(Win), Alt and is left as is)

SUPER sends left Cmd, so Super+C/V/X/Q/H are native macOS. Super+W closes
the whole window, as on Omarchy (native Cmd+W would only close a tab). Every Omarchy
window-manager chord in BINDINGS below is caught here and runs `wm`.

Ctrl works like Linux: outside terminals it sends right Cmd, so Ctrl+F/T/S/L
are find/new tab/save/address bar. Inside terminals it stays a real Control
(Ctrl+C interrupts). Left vs right Cmd is how the two never collide.

Run:  ./generate.py            (writes karabiner.json and keybindings.txt)
"""
import json
from pathlib import Path

WM = '"$HOME/.local/bin/wm"'

TERMINALS = [
    r"^com\.mitchellh\.ghostty$",
    r"^com\.apple\.Terminal$",
    r"^com\.googlecode\.iterm2$",
    r"^net\.kovidgoyal\.kitty$",
    r"^org\.alacritty$",
    r"^dev\.warp\.Warp",
]
IN_TERM = {"type": "frontmost_application_if", "bundle_identifiers": TERMINALS}
NOT_TERM = {"type": "frontmost_application_unless", "bundle_identifiers": TERMINALS}
BUILT_IN = {"type": "device_if", "identifiers": [{"is_built_in_keyboard": True}]}
EXTERNAL = {"type": "device_unless", "identifiers": [{"is_built_in_keyboard": True}]}

# Logical modifier -> modifier as seen after the remap rules at the bottom.
# CTRL is right_command outside terminals and left_control inside them, so a
# chord using CTRL is emitted twice, once per meaning.
MOD = {"SUPER": "left_command", "ALT": "left_option", "SHIFT": "shift"}

KEY = {
    "LEFT": "left_arrow", "RIGHT": "right_arrow", "UP": "up_arrow", "DOWN": "down_arrow",
    "TAB": "tab", "RETURN": "return_or_enter", "SPACE": "spacebar",
    "MINUS": "hyphen", "EQUAL": "equal_sign", "BACKSPACE": "delete_or_backspace",
    "ESCAPE": "escape", "COMMA": "comma", "SLASH": "slash",
}


def wm(*args):
    return {"shell_command": " ".join([WM, *args])}


def open_app(app, *args):
    extra = (" --args " + " ".join(args)) if args else ""
    return {"shell_command": f"open -na '{app}'{extra}"}


def keys(key, *mods):
    return {"key_code": key, "modifiers": list(mods)}


# (chord, description, action) -- chords use Omarchy's names.
BINDINGS = [
    # Tiling: scrolling layout
    ("SUPER + LEFT", "Focus left window", wm("focus", "left")),
    ("SUPER + RIGHT", "Focus right window", wm("focus", "right")),
    ("SUPER + UP", "Focus window above", wm("focus", "up")),
    ("SUPER + DOWN", "Focus window below", wm("focus", "down")),
    ("SUPER + SHIFT + LEFT", "Swap window left", wm("swap", "left")),
    ("SUPER + SHIFT + RIGHT", "Swap window right", wm("swap", "right")),
    ("SUPER + SHIFT + UP", "Swap window up", wm("swap", "up")),
    ("SUPER + SHIFT + DOWN", "Swap window down", wm("swap", "down")),
    ("SUPER + W", "Close window", wm("close")),
    ("SUPER + T", "Toggle floating", wm("float")),
    ("SUPER + F", "Full screen", wm("fullscreen")),
    ("SUPER + ALT + F", "Full width", wm("maximize")),
    ("SUPER + CTRL + F", "Center column", wm("center")),
    ("SUPER + L", "Toggle workspace layout", wm("layout")),
    ("SUPER + S", "Toggle scratchpad", wm("scratchpad")),
    ("SUPER + ALT + S", "Move window to scratchpad", wm("scratchpad-move")),
    ("SUPER + MINUS", "Narrower", wm("resize", "width", "-100")),
    ("SUPER + EQUAL", "Wider", wm("resize", "width", "+100")),
    ("SUPER + SHIFT + MINUS", "Shorter", wm("resize", "height", "-100")),
    ("SUPER + SHIFT + EQUAL", "Taller", wm("resize", "height", "+100")),
    ("SUPER + ALT + MINUS", "Narrower a little", wm("resize", "width", "-25")),
    ("SUPER + ALT + EQUAL", "Wider a little", wm("resize", "width", "+25")),
    ("SUPER + CTRL + MINUS", "Narrower a lot", wm("resize", "width", "-300")),
    ("SUPER + CTRL + EQUAL", "Wider a lot", wm("resize", "width", "+300")),
    # Workspaces
    *[(f"SUPER + {n}", f"Workspace {n}", wm("workspace", str(n))) for n in range(1, 10)],
    *[(f"SUPER + SHIFT + {n}", f"Move window to workspace {n}", wm("move-to", str(n)))
      for n in range(1, 10)],
    *[(f"SUPER + SHIFT + ALT + {n}", f"Move window silently to workspace {n}",
       wm("move-to-silent", str(n))) for n in range(1, 10)],
    ("SUPER + TAB", "Next workspace", wm("workspace", "next")),
    ("SUPER + SHIFT + TAB", "Previous workspace", wm("workspace", "prev")),
    ("SUPER + CTRL + TAB", "Former workspace", wm("workspace", "last")),
    ("ALT + TAB", "Next window", wm("window", "next")),
    ("ALT + SHIFT + TAB", "Previous window", wm("window", "prev")),
    # Monitors
    ("CTRL + ALT + TAB", "Next monitor", wm("monitor", "next")),
    ("CTRL + ALT + SHIFT + TAB", "Previous monitor", wm("monitor", "prev")),
    ("SUPER + SHIFT + ALT + LEFT", "Workspace to left monitor", wm("workspace-to", "left")),
    ("SUPER + SHIFT + ALT + RIGHT", "Workspace to right monitor", wm("workspace-to", "right")),
    ("SUPER + SHIFT + ALT + UP", "Workspace to monitor above", wm("workspace-to", "up")),
    ("SUPER + SHIFT + ALT + DOWN", "Workspace to monitor below", wm("workspace-to", "down")),
    # Apps
    ("SUPER + RETURN", "Terminal", wm("terminal")),
    ("SUPER + SHIFT + RETURN", "Browser", open_app("Google Chrome", "--new-window")),
    ("SUPER + SHIFT + B", "Browser", open_app("Google Chrome", "--new-window")),
    ("SUPER + SHIFT + ALT + B", "Browser (private)", open_app("Google Chrome", "--incognito")),
    ("SUPER + SHIFT + F", "File manager", {"shell_command": "open ~"}),
    ("SUPER + SHIFT + N", "Editor", open_app("Ghostty", "-e", "nvim")),
    ("SUPER + CTRL + T", "Activity", open_app("Ghostty", "-e", "btop")),
    ("SUPER + CTRL + C", "Capture menu", {"shell_command": "open -a Screenshot"}),
    # System
    ("SUPER + CTRL + L", "Lock", keys("q", "left_control", "left_command")),
    ("SUPER + K", "Keybindings", {"shell_command": f"{WM} keybindings"}),
]


def chord_variants(chord):
    """'SUPER + CTRL + 1' -> [(key_code, [modifiers...]), ...]"""
    *mods, key = [p.strip() for p in chord.split("+")]
    key = KEY.get(key, key.lower())
    if "CTRL" not in mods:
        return [(key, [MOD[m] for m in mods])]
    rest = [MOD[m] for m in mods if m != "CTRL"]
    return [(key, rest + ["right_command"]), (key, rest + ["left_control"])]


def manipulator(key, mandatory, to, conditions=None):
    m = {
        "type": "basic",
        "from": {"key_code": key, "modifiers": {"mandatory": mandatory, "optional": ["caps_lock"]}},
        "to": [to],
    }
    if conditions:
        m["conditions"] = conditions
    return m


def wm_rules():
    out = []
    for chord, desc, action in BINDINGS:
        out.append({
            "description": f"Omarchy: {chord} - {desc}",
            "manipulators": [manipulator(k, mods, action) for k, mods in chord_variants(chord)],
        })
    return out


def linux_text_editing():
    """Ctrl (= right Cmd outside terminals) edits text the Linux way."""
    def m(frm, frm_mods, to, cond, shift=True):
        man = manipulator(frm, frm_mods, to, [cond])
        if shift:
            man["from"]["modifiers"]["optional"].append("shift")
        return man

    ms = [
        # Ctrl+arrows jump words, Ctrl+Backspace/Delete delete words.
        m("left_arrow", ["right_command"], keys("left_arrow", "left_option"), NOT_TERM),
        m("right_arrow", ["right_command"], keys("right_arrow", "left_option"), NOT_TERM),
        m("delete_or_backspace", ["right_command"], keys("delete_or_backspace", "left_option"), NOT_TERM, False),
        m("delete_forward", ["right_command"], keys("delete_forward", "left_option"), NOT_TERM, False),
        # Ctrl+Tab cycles browser/editor tabs, as on Linux.
        m("tab", ["right_command"], keys("tab", "left_control"), NOT_TERM),
        # Fn+arrows (the Linux Fn position) are Home/End/PgUp/PgDn.
        # Home/End go to line start/end, not document top/bottom.
        m("left_arrow", ["fn"], keys("left_arrow", "left_command"), NOT_TERM),
        m("right_arrow", ["fn"], keys("right_arrow", "left_command"), NOT_TERM),
        m("left_arrow", ["fn"], keys("home"), IN_TERM),
        m("right_arrow", ["fn"], keys("end"), IN_TERM),
        m("up_arrow", ["fn"], keys("page_up"), IN_TERM),
        m("down_arrow", ["fn"], keys("page_down"), IN_TERM),
        m("up_arrow", ["fn"], keys("page_up"), NOT_TERM),
        m("down_arrow", ["fn"], keys("page_down"), NOT_TERM),
        m("home", [], keys("left_arrow", "left_command"), NOT_TERM),
        m("end", [], keys("right_arrow", "left_command"), NOT_TERM),
    ]
    return [{"description": "Linux text editing: Ctrl+arrows/Backspace, Home/End", "manipulators": ms}]


def modifier_layout():
    def swap(frm, to, conds):
        return {
            "type": "basic",
            "from": {"key_code": frm, "modifiers": {"optional": ["any"]}},
            "to": [{"key_code": to}],
            "conditions": conds,
        }

    return [
        {
            "description": "Linux key positions: [fn][control][option][command] -> Ctrl Fn Super Alt",
            "manipulators": [
                swap("fn", "right_command", [BUILT_IN, NOT_TERM]),
                swap("fn", "left_control", [BUILT_IN, IN_TERM]),
                swap("left_control", "fn", [BUILT_IN]),
                swap("left_option", "left_command", [BUILT_IN]),
                swap("left_command", "left_option", [BUILT_IN]),
            ],
        },
        {
            "description": "PC keyboard: Ctrl is the app-shortcut key outside terminals",
            "manipulators": [swap("left_control", "right_command", [EXTERNAL, NOT_TERM])],
        },
    ]


def main():
    rules = wm_rules() + linux_text_editing() + modifier_layout()
    config = {
        "global": {"show_in_menu_bar": False},
        "profiles": [{
            "name": "Omarchy",
            "selected": True,
            "complex_modifications": {"rules": rules},
            "virtual_hid_keyboard": {"keyboard_type_v2": "ansi"},
        }],
    }
    here = Path(__file__).parent
    (here / "karabiner.json").write_text(json.dumps(config, indent=2) + "\n")
    rows = []
    for c, d, _ in BINDINGS:
        if c[-1].isdigit():  # collapse the 1..9 workspace rows into one
            if c[-1] != "1":
                continue
            c, d = c + "-9", d.replace(" 1", " 1-9")
        rows.append((c, d))
    width = max(len(c) for c, _ in rows)
    sheet = [f"{c.ljust(width)}  {d}" for c, d in rows]
    sheet += ["", "Super+C/V/X  copy/paste/cut    Super+Space  Spotlight",
              "Ctrl+F/T/L/S  find/tab/address/save (Linux style; real Ctrl in terminals)",
              "Ctrl+arrows  word jump        Fn+arrows  Home/End/PgUp/PgDn"]
    (here / "keybindings.txt").write_text("\n".join(sheet) + "\n")


if __name__ == "__main__":
    main()
