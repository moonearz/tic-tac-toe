FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY tic_tac_toe ./tic_tac_toe
COPY web ./web

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web.app:app"]
