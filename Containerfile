FROM python:3.11-slim

LABEL Maintainer="Olof Haglund"


WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/bot.py"]
