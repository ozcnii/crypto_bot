FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 777 /app

CMD ["sh", "-c", "python CryptoAPI/settings.py && alembic -c CryptoAPI/alembic.ini upgrade head && python CryptoAPI/main.py"]

EXPOSE 8080