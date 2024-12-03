#!/bin/bash
set -e

# Enable debug logging
set -x

echo "=== BOOTSTRAP START ==="

# Function to log messages with timestamps
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /tmp/bootstrap.log
}

echo "=== SETTING UP ENVIRONMENT ==="
export HOME="/tmp"
export XDG_CONFIG_HOME="/tmp/.config"
export XDG_CACHE_HOME="/tmp/.cache"
export XDG_DATA_HOME="/tmp/.local/share"
export DCONF_PROFILE="/tmp/.config/dconf"

echo "=== CREATING DIRECTORIES ==="
mkdir -p /tmp/.config/dconf
mkdir -p /tmp/.cache
mkdir -p /tmp/.local/share
mkdir -p /tmp/LibreOffice_Conversion
chmod -R 777 /tmp/.config
chmod -R 777 /tmp/.cache
chmod -R 777 /tmp/.local
chmod -R 777 /tmp/LibreOffice_Conversion
echo "Directories created in /tmp"

echo "=== LOCATING LIBREOFFICE ==="
# Define possible LibreOffice paths
POSSIBLE_PATHS=(
    "/usr/bin/libreoffice"
    "/usr/bin/soffice"
    "/usr/lib/libreoffice/program/soffice"
)

# Find the first working LibreOffice path
LIBREOFFICE_PATH=""
for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -x "$path" ]; then
        LIBREOFFICE_PATH="$path"
        break
    fi
done

if [ -z "$LIBREOFFICE_PATH" ]; then
    echo "ERROR: LibreOffice executable not found"
    echo "Checking all possible locations:"
    find / -name soffice -type f 2>/dev/null
    find / -name libreoffice -type f 2>/dev/null
    exit 1
fi

echo "LibreOffice found at: $LIBREOFFICE_PATH"
echo "Checking LibreOffice version:"
$LIBREOFFICE_PATH --version || true

echo "=== STARTING LIBREOFFICE ==="
echo "Starting LibreOffice with command:"
echo "$LIBREOFFICE_PATH --headless --nologo --norestore --nodefault --accept=\"socket,host=127.0.0.1,port=2002;urp;\" -env:UserInstallation=file:///tmp/LibreOffice_Conversion"

$LIBREOFFICE_PATH --headless \
    --nologo \
    --norestore \
    --nodefault \
    --accept="socket,host=127.0.0.1,port=2002;urp;" \
    -env:UserInstallation=file:///tmp/LibreOffice_Conversion > /tmp/libreoffice.log 2>&1 &

LIBREOFFICE_PID=$!
echo "LibreOffice started with PID: $LIBREOFFICE_PID"

echo "=== WAITING FOR LIBREOFFICE ==="
sleep 3

echo "=== STARTING LAMBDA HANDLER ==="
exec python3 -m awslambdaric $1

echo "=== BOOTSTRAP END ==="
