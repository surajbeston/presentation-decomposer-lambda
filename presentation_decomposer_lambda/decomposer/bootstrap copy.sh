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
echo "HOME set to: $HOME"

echo "=== CREATING DIRECTORIES ==="
mkdir -p /tmp/.config
mkdir -p /tmp/.cache
mkdir -p /tmp/LibreOffice_Conversion
echo "Directories created in /tmp"

echo "=== LOCATING LIBREOFFICE ==="
# Define possible LibreOffice paths
POSSIBLE_PATHS=(
    "/opt/libreoffice7.5/program/soffice",
    "/opt/libreoffice*/program/soffice"
    "/usr/lib64/libreoffice/program/soffice"
    "/usr/bin/libreoffice"
    "/usr/bin/soffice"
)

# Find the first working LibreOffice path
LIBREOFFICE_PATH=""
for path in "${POSSIBLE_PATHS[@]}"; do
    # Use ls to expand wildcards if present
    expanded_path=$(ls $path 2>/dev/null || true)
    if [ ! -z "$expanded_path" ] && [ -x "$expanded_path" ]; then
        LIBREOFFICE_PATH="$expanded_path"
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
sleep 5

# echo "=== CHECKING LIBREOFFICE PROCESS ==="
# if ! kill -0 $LIBREOFFICE_PID 2>/dev/null; then
#     echo "ERROR: LibreOffice failed to start"
#     echo "=== LIBREOFFICE LOG ==="
#     cat /tmp/libreoffice.log
#     echo "=== SYSTEM MEMORY ==="
#     cat /proc/meminfo || echo "Memory info not available"
#     echo "=== PROCESS LIST ==="
#     ps aux || ps -ef || echo "Process list not available"
#     exit 1
# fi

# echo "LibreOffice process verified running"

# echo "=== SETTING UP PYTHON ENVIRONMENT ==="
# export PYTHONPATH="${LAMBDA_TASK_ROOT}:${PYTHONPATH}"
# echo "Updated PYTHONPATH: $PYTHONPATH"

# echo "=== STARTING LAMBDA HANDLER ==="
# echo "Lambda handler argument: $1"
exec python3 -m awslambdaric $1

echo "=== BOOTSTRAP END ==="
