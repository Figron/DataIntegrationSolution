FROM python:3.10-slim

WORKDIR /

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY . /

ENV PYTHONPATH=/

CMD ["python", "src/scripts/minio_watcher/minio_watcher.py"]
