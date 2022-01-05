[[ $BASE_URL ]] && { cd /app/static/ui && npm run build; cd /app; }
/opt/venv/bin/uvicorn recipes:app
