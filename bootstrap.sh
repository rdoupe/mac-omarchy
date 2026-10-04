#!/bin/bash
# Make this Mac work like the Omarchy laptop: Linux key positions, Omarchy
# shortcuts, scrolling tiling. Safe to re-run. Anything replaced is backed up
# as <file>.bak.<timestamp>.
set -euo pipefail
cd "$(dirname "$0")"
stamp=$(date +%s)
todo=()

say() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }

install_file() { # src dest [mode]
  mkdir -p "$(dirname "$2")"
  if [[ -e $2 ]] && ! cmp -s "$1" "$2"; then cp "$2" "$2.bak.$stamp"; fi
  install -m "${3:-644}" "$1" "$2"
}

if ! command -v brew >/dev/null; then
  echo "Install Homebrew first (https://brew.sh), then re-run this script." >&2
  exit 1
fi

macos_major=$(sw_vers -productVersion | cut -d. -f1)
if [[ $macos_major -ge 26 && $(uname -m) == arm64 ]]; then tiler=omniwm; else tiler=paneru; fi

say "Installing Karabiner-Elements, Ghostty, JetBrains Mono Nerd Font, $tiler"
brew install --cask karabiner-elements ghostty font-jetbrains-mono-nerd-font
[[ -d "/Applications/Google Chrome.app" ]] || todo+=("Super+Shift+Enter opens Google Chrome, which isn't installed.")
if [[ $tiler == omniwm ]]; then
  brew install --cask omniwm
else
  brew install paneru
fi

say "Installing configs"
python3 karabiner/generate.py
install_file karabiner/karabiner.json "$HOME/.config/karabiner/karabiner.json"
install_file karabiner/keybindings.txt "$HOME/.config/mac-omarchy/keybindings.txt"
install_file ghostty/config "$HOME/.config/ghostty/config"
install_file bin/wm "$HOME/.local/bin/wm" 755

say "macOS settings"
# Tilers need one set of Spaces per display ("Displays have separate Spaces").
defaults write com.apple.spaces spans-displays -bool false
# Ctrl+arrows are Mission Control shortcuts that would fire in terminals (where
# Ctrl stays a real Control): move a space left/right, Mission Control, app windows.
for id in 32 33 34 35 79 80 81 82; do
  defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add "$id" '<dict><key>enabled</key><false/></dict>'
done
/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings -u 2>/dev/null || true
# Don't rearrange Spaces by recent use; workspace numbers must stay put.
defaults write com.apple.dock mru-spaces -bool false
killall Dock

if [[ $tiler == omniwm ]]; then
  settings="$HOME/.config/omniwm/settings.toml"
  if [[ -f $settings ]]; then
    say "Configuring OmniWM (in place; its schema is strict)"
    cp "$settings" "$settings.bak.$stamp"
    sed -i '' \
      -e 's/^hotkeysEnabled = .*/hotkeysEnabled = false/' \
      -e 's/^ipcEnabled = .*/ipcEnabled = true/' \
      -e 's/^defaultLayoutType = .*/defaultLayoutType = "niri"/' \
      -e 's/^visibleContainerCount = .*/visibleContainerCount = 2/' \
      -e '/^\[gaps\]/,/^\[/ s/^size = .*/size = 5.0/' \
      "$settings"
    sed -i '' -E '/^\[gaps\.outer\]/,/^\[/ s/^(left|right|top|bottom) = .*/\1 = 10.0/' "$settings"
    grep -q '^hotkeysEnabled = false' "$settings" && grep -q '^ipcEnabled = true' "$settings" ||
      todo+=("OmniWM: in its menu-bar Settings, turn off hotkeys and turn on IPC.")
  else
    todo+=("Open OmniWM once (grant Accessibility + Input Monitoring, turn on Start at Login), quit it, then re-run ./bootstrap.sh to configure it.")
  fi
else
  say "Configuring Paneru"
  install_file tiler/paneru.toml "$HOME/.paneru.toml"
  paneru install >/dev/null 2>&1 || true
  paneru restart >/dev/null 2>&1 || paneru start
  todo+=("Paneru: allow it under System Settings > Privacy & Security > Accessibility.")
fi

todo+=(
  "Karabiner-Elements: open it and approve the driver extension, Input Monitoring and Login Items prompts. If IT blocks the driver extension, the Linux key positions and every shortcut are lost; ask IT to allow Karabiner's driver."
  "Karabiner-Elements: allow karabiner_console_user_server under Accessibility (Super+Enter uses it to open a new Ghostty window)."
  "Log out and back in once (separate Spaces per display only applies after that)."
)

say "Done. Still to do by hand:"
for i in "${!todo[@]}"; do printf '  %d. %s\n' $((i + 1)) "${todo[$i]}"; done
echo
echo "Super+K shows every shortcut."
