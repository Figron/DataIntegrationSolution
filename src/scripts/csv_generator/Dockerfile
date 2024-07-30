FROM python:3.10-slim

WORKDIR /

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY . /

ENV PYTHONPATH=/

CMD ["python", "src/scripts/csv_generator/generate_csv_source_files.py"]
