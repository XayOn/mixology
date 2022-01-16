#!/bin/bash
echo "Starting with ${BASE_URL}"
[[ $BASE_URL ]] && { cd /app/ui && npm install && npm run build; cd /app; }
/opt/venv/bin/uvicorn --host="0.0.0.0" mixologist:app 
