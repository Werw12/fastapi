# backend/core/config.py

#Jwt configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'magreta2412@gmail.com' # change this to prof email in production
MAIL_PASSWORD = 'mpwl bdve swmz qisz'
EMAIL_FROM = 'magreta2412@gmail.com'
EMAIL_FROM_NAME = 'Your App Name'

# Database configuration
DATABASE_URL = "postgresql://postgres:witalik11@localhost/Corporate_DB"