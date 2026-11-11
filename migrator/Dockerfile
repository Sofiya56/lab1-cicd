FROM python:3.12-slim
WORKDIR /src
ENV PYTHONPATH=/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY migrator ./migrator
CMD ["python", "migrator/migrate.py"]