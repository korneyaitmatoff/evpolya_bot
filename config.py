from dotenv import load_dotenv, get_key

load_dotenv()

TOKEN = get_key('.env', 'TOKEN')
PROVIDER_TOKEN = get_key('.env', 'PROVIDER_TOKEN')

DB_USER = get_key('.env', 'DB_USER')
DB_PASSWORD = get_key('.env', 'DB_PASSWORD')
DB_NAME = get_key('.env', 'DB_NAME')

API_ID = get_key('.env', 'API_ID')
API_HASH = get_key('.env', 'API_HASH')
PHONE = get_key('.env', 'PHONE')

# GROUP_ID = -1002879039601 # MY TEST GROUP
# # GROUP_ID = -1002429508007 # EVP TEST GROUP
GROUP_ID = -1002501553452 # PROD GROUP