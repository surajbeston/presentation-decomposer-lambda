#!/bin/bash
set -e

# Set environment variables
export S3_ACCESS_KEY="bed6c1f5cc02c9fe3ea7be791865fcbd"
export S3_SECRET_KEY="257a4eb75fc508395084dd522335885e97dedeae82f083f5027a9e6034dc2137"
export CLOUDFLARE_API_TOKEN="0qNnxn5gAzH1x7qX9iTueqqLmRLQkfQz-3JGorRA"
export S3_BUCKET_URL="https://66f903215ee11cb820883e93cff8c6d6.r2.cloudflarestorage.com"
export S3_BUCKET_NAME="present-for-me"
export PUBLIC_DOMAIN_URL="https://pub-ae5a83dfee0146d886142453235c2605.r2.dev/"

echo "=== STARTING LIBREOFFICE ==="

# Start LibreOffice in headless mode
/usr/bin/libreoffice --headless --accept="socket,host=127.0.0.1,port=2002;urp;" --norestore --nologo --nofirststartwizard --impress --nodefault &

sleep 6

echo "=== LIBREOFFICE STARTED ==="

/usr/bin/python3 -m awslambdaric processor.process_slide.handler