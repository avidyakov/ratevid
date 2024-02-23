FROM python:3.12.2-slim

WORKDIR /app/
EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD alembic upgrade head && python src/main.py
