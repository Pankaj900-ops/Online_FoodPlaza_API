
# Optional Dockerfile for local testing
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "online_foodplaza.wsgi:application", "--bind", "0.0.0.0:8000"]
