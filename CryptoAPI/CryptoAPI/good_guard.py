import os

# S3 Bucket
endpoint_url_bucket = os.environ.get('endpoint_url_bucket')
region_bucket = os.environ.get('region_bucket')
access_key_bucket = os.environ.get('access_key_bucket')
secret_access_key_bucket = os.environ.get('secret_access_key_bucket')
bucket_name = os.environ.get('bucket_name')

# SECRETS & VARS DATA
max_requests = 600
max_time_request_seconds = 60

# SECRETS Keys
SECRET_KEY = 'HDA-32'
TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
BOT_ID = '7210647842'
BOT_LINK = "https://t.me/aenolabsbot"
COINMARKETCAP_API_KEY = os.environ.get('COINMARKETCAP_API_KEY')

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

DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@postgresql:5432/{os.environ.get("POSTGRES_DB")}'