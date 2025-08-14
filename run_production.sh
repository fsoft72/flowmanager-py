#!/bin/bash
# FlowManager Python production startup with virtual environment

echo "Starting FlowManager Python (Production)..."

# Check for SSL certificates
CERT_FILE="certs/CA/localhost/localhost.crt"
KEY_FILE="certs/CA/localhost/localhost.decrypted.key"

if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "🔒 SSL certificates found - starting HTTPS server on port 7183"
    echo "URL: https://localhost:7183"
    python -c "
import uvicorn
from main import app, cfg
uvicorn.run('main:app', host='localhost', port=cfg['port'], ssl_keyfile='$KEY_FILE', ssl_certfile='$CERT_FILE', reload=False)
"
else
    echo "⚠️  SSL certificates not found - starting HTTP server on port 7183"
    echo "Expected: $CERT_FILE and $KEY_FILE"
    echo "URL: http://localhost:7183"
    python -c "
import uvicorn
from main import app, cfg
uvicorn.run('main:app', host='localhost', port=cfg['port'], reload=False)
"
fi
