# FlowManager Python

This is a Python3 + FastAPI port of the original Node.js FlowManager application with **full HTTPS support**.

## Quick Start

1. **Setup virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Generate SSL certificates:**
   ```bash
   ./generate_ssl_simple.sh    # Works with all OpenSSL versions
   ```

3. **Run the server:**
   ```bash
   ./run_production.py         # HTTPS: https://localhost:7183
   ./run_dev.py               # HTTP: http://localhost:7183 (development)
   ```

## HTTPS Support ✅

**Full HTTPS implementation with automatic SSL detection:**

- ✅ **Auto-detects SSL certificates**
- ✅ **HTTPS when certificates exist**: `https://localhost:7183`
- ✅ **HTTP fallback**: `http://localhost:7183` (if no certificates)
- ✅ **Multiple certificate generation options**

### Certificate Generation Options:

```bash
./generate_ssl_simple.sh    # ✅ Fixed bash script (works with all OpenSSL)
python generate_ssl_python.py    # ✅ Pure Python (no OpenSSL dependency)
```

## Scripts Overview

| Script | Purpose | Protocol |
|--------|---------|----------|
| `./run_production.py` | Production server | HTTPS (auto-detect) |
| `./run_dev.py` | Development server | HTTP only |
| `./start.sh` | Auto-setup + production | HTTPS (auto-detect) |

## API Endpoints

- `GET /hello` - Test endpoint (returns encrypted response)
- `POST /backup` - Save backup files  
- `GET /projects` - List all project keys
- `GET /targets` - List all projects with names
- `GET /import` - Import latest backup
- `POST /build?project=<n>` - Build project from flow data
- `POST /save/to/project?project=<n>` - Save flow to project
- `POST /save/markdown?project=<n>` - Save markdown documentation
- `POST /save/module?project=<n>` - Save module data

All endpoints maintain **100% API compatibility** with the original Node.js version.
