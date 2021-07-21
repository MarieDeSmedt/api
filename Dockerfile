# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0"]