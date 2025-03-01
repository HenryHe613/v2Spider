FROM python:3.12.7-slim-bookworm
LABEL authors="nanyancc"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "main.py"]