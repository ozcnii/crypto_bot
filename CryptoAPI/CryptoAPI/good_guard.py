import os

# S3 Bucket
endpoint_url_bucket = os.environ.get('MINIO_ENDPOINT')
region_bucket = os.environ.get('MINIO_REGION')
access_key_bucket = os.environ.get('MINIO_ROOT_USER')
secret_access_key_bucket = os.environ.get('MINIO_ROOT_PASSWORD')
bucket_name = os.environ.get('BUCKET_NAME')

# SECRETS & VARS DATA
max_requests = 600
max_time_request_seconds = 60

# SECRETS Keys
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
BOT_ID = os.environ.get('BOT_ID')
BOT_LINK = os.environ.get('BOT_LINK')
COINMARKETCAP_API_KEY = os.environ.get('COINMARKETCAP_API_KEY')

# other
default_avatar = os.environ.get('DEFAULT_AVATAR')
coin_to_usdt_rate = 0.01

# ID secrets
client_id = ["1", "2"]

# APIs Keys
VIRUSTOTAL_API_KEY = os.environ.get('VIRUSTOTAL_API_KEY')

# EMAILs DATA
smtp_server = os.environ.get('SMTP_SERVER')
imap_server = os.environ.get('IMAP_SERVER')

auth_email = os.environ.get('AUTH_EMAIL')
auth_email_password = os.environ.get('AUTH_EMAIL_PASSWORD')

# DATABASE

DATABASE_URL = os.environ.get('DATABASE_URL')