#!/bin/bash
[[ $BASE_URL ]] && { cd /app/ui && npm run build; cd /app; }
/opt/venv/bin/uvicorn --host="0.0.0.0" recipes:app 
