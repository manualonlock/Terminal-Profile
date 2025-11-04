# Install Warp terminal
virtualenv .venv
source .venv/bin/activate
pip install requests beautifulsoup4

install_dmg() {
    local file_name=$1
    local download_url=$2
    local dmg_name="${file_name}.dmg"

    curl -L -H "User-Agent: macos" $download_url --output $dmg_name
    hdiutil attach "$dmg_name"
    # Use find to get the actual mount path and quote the output to handle spaces
    export mount_point="$(find /Volumes -type d -maxdepth 1 -name "*$file_name*" | head -n 1)"
    export app_name="$(find "$mount_point" -type d -maxdepth 2 -mindepth 1 -name "*$file_name*" | head -n 1)"
    cp -R "$app_name" /Applications/
    hdiutil detach "$mount_point"
    rm $dmg_name
}

echo "Downloading Warp"
install_dmg "Warp" "https://app.warp.dev/download"
echo "Downloading Cursor IDE"
install_dmg "Cursor" $(python3 get_cursor_production_link.py)

echo "Downloading Rectangle Pro"
install_dmg "Rectangle" $(python3 get_rectangle_production_link.py)
echo "Downloading Better Display"
install_dmg "Better" $(python3 get_better_display_link.py)

deactivate
rm -rf .venv