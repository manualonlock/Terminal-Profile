# Load Brew Shell Environment
eval "$(/opt/homebrew/bin/brew shellenv)"

# Setting up aliases
alias ls="lsd"
alias cat="bat"

# Setting up color scheme
export LS_COLORS=$(vivid generate snazzy)

neofetch

# Setting up prompt (Skipping for Apple Terminal as it doesn't support the nerd fonts encoding)
export POSH_CONFIG_FILE_PATH="$HOME/.config/posh/posh.json"
if [ "$TERM_PROGRAM" != "Apple_Terminal" ]; then
eval "$(oh-my-posh init zsh --config $POSH_CONFIG_FILE_PATH)"
fi