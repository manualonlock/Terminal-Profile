/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install:
# hack nerdfonts for terminal font
# oh-my-posh for a powerline styled prompt
# vivid for a colorful prompt
# lsd for a modern ls command
# fzf for a fuzzy finder
# neofetch for to spice up the terminal
# bat for a modern cat command
brew install font-hack-nerd-font \
    brew install jandedobbeleer/oh-my-posh/oh-my-posh \
    vivid \
    lsd \
    fzf \
    neofetch \
    bat \
    virtualenv

# ----- END BREW INSTALLATION -----


# COPY ZSHRC FILE
export ZSHRC_FILE_NAME=".zshrc"
export ZSHRC_FILE_PATH="$HOME/$ZSHRC_FILE_NAME"

if [ -f "$ZSHRC_FILE_PATH" ]; then
    echo "$ZSHRC_FILE_NAME file already exists, only manual editing is allowed"
else
    echo "Creating $ZSHRC_FILE_NAME file..."
    cp $ZSHRC_FILE_NAME $ZSHRC_FILE_PATH
    echo "$ZSHRC_FILE_NAME file created successfully"
fi
# ----- END ZSHRC COPY -----

# COPY POSH CONFIG FILE
export CONFIG_DIR="$HOME/.config"

if [ ! -d "$CONFIG_DIR" ]; then
    mkdir "$CONFIG_DIR"
    echo "Created $CONFIG_DIR directory."
fi

export POSH_DIR = "$CONFIG_DIR/posh"

if [ -d "$POSH_DIR" ]; then
    echo "$POSH_DIR already exists. Skipping creation."
else
    mkdir "$POSH_DIR"
    echo "Created $POSH_DIR directory."
fi

POSH_CONFIG_FILE_NAME="posh.json"
cp posh_config.json $POSH_DIR/$POSH_CONFIG_FILE_NAME

# ----- END POSH CONFIG FILE COPY -----


# Install macOS applications
./install_macos_applications.sh