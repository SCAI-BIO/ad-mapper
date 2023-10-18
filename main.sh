BACKEND_URL=$1

export BACKEND_URL=$BACKEND_URL

export PYTHONPATH=$PYTHONPATH:/app/backend

uvicorn backend.main:app --host 0.0.0.0 --port 8000 & 

echo "VUE_APP_API=$BACKEND_URL" >> frontend/variable-mapper/.env.production
echo "VUE_APP_API=$BACKEND_URL" >> frontend/variable-mapper/.env.development

cd frontend/variable-mapper

npm run production & 