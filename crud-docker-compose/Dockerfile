FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt --no-cache-dir 

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]