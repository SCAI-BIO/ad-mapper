FROM python:3.10-bookworm

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt

ENV BASEDIR="/app"

ENV BACKEND_URL="https://ad-mapper.scai.fraunhofer.de/api/"

RUN python3 /app/load_models.py

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8", "--root-path", "/api"]