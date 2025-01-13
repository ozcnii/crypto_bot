FROM python:alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python run.py"]

EXPOSE 5000
