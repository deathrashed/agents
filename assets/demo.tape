# Terminal recording of the health check, styled like my Ghostty setup (Breeze palette,
# JetBrains Mono, fast-syntax-highlighting). build-media.sh crops it and adds the window bar. Recorded at 2x so it stays sharp on retina screens. The prompt is kept minimal on
# purpose: the folder and a chevron, no clock, duration, git state or language marker.
# Rebuild: bash assets/build-media.sh. Run from the repo root so scripts/agents-check resolves.
Output assets/demo.mp4

Require zsh

Set Shell "bash"
Set Theme { "name": "Ghostty Breeze", "black": "#31363b", "red": "#ed1515", "green": "#11d116", "yellow": "#f67400", "blue": "#1d99f3", "magenta": "#9b59b6", "cyan": "#1abc9c", "white": "#eff0f1", "brightBlack": "#7f8c8d", "brightRed": "#c0392b", "brightGreen": "#1cdc9a", "brightYellow": "#fdbc4b", "brightBlue": "#3daee9", "brightMagenta": "#8e44ad", "brightCyan": "#16a085", "brightWhite": "#fcfcfc", "background": "#1e1e1e", "foreground": "#eff0f1", "selection": "#31363b", "cursor": "#eff0f1" }
Set FontSize 36
Set Width 1680
Set Height 880
Set Padding 28
Set TypingSpeed 45ms

# Same shell tooling as my terminal: zsh with fast-syntax-highlighting, a blue folder name and a
# purple chevron. FORCE_COLOR makes agents-check colour its status tags when piped.
Hide
Type "exec zsh -f"
Enter
Type "source /opt/homebrew/share/zsh-fast-syntax-highlighting/fast-syntax-highlighting.plugin.zsh"
Enter
Type `PROMPT=$'%{\e[38;2;29;154;243m%}rd-agents%{\e[0m%}\n%{\e[1;38;2;149;87;176m%}›%{\e[0m%} '`
Enter
Type "export FORCE_COLOR=1"
Enter
Type "clear"
Enter
Show

Sleep 600ms
Type "scripts/agents-check | sed -n '1,14{s/  (.*//;s/, ignored.*//;p;}'"
Sleep 400ms
Enter
# The check takes several seconds; the wait is not recorded, the output is real.
Hide
Wait+Screen@60s /token_tools/
Show
Sleep 4s
