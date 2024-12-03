import os

# S3 Bucket
endpoint_url_bucket = 'https://app.aenolabs.com'
region_bucket = 'eu-central-1'
access_key_bucket = os.environ.get('MINIO_ROOT_USER')
secret_access_key_bucket = os.environ.get('MINIO_ROOT_PASSWORD')
bucket_name = 'aenolabsfiles'

# SECRETS & VARS DATA
max_requests = 600
max_time_request_seconds = 60

# SECRETS Keys
SECRET_KEY = 'verysecretkeyforjwt'
ALGORITHM = 'HS256'
TELEGRAM_API_TOKEN = "6438571775:AAGkiDR-83pqe-p3xsxXzZ5KP6I1nN4QOUU"
BOT_ID = '7210647842'
BOT_LINK = "https://t.me/aenolabsbot"
COINMARKETCAP_API_KEY = "e6d7a3b7-2b3a-4a9a-9f3a-8c7b9a6c5b3a"

# other
default_avatar = '9d5340dd1a8dc12373cef4f4da140a202df4c2f9865a31b7de42c689d0f68c3d.jpg'
coin_to_usdt_rate = 0.01

# ID secrets
client_id = ["1", "2"]

# APIs Keys
VIRUSTOTAL_API_KEY = ""

# EMAILs DATA
smtp_server = "smtp.example.ru"
imap_server = "imap.example.ru"

auth_email = "auth@example.ru"
auth_email_password = "hda-32"

# DATABASE

DATABASE_URL = "postgresql+asyncpg://postgres:password@postgresql:5432/cryptodatabase"