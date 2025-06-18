from dotenv import load_dotenv, get_key

load_dotenv()

TOKEN = get_key('.env', 'TOKEN')
PROVIDER_TOKEN = get_key('.env', 'PROVIDER_TOKEN')

DB_USER = get_key('.env', 'DB_USER')
DB_PASSWORD = get_key('.env', 'DB_PASSWORD')
DB_NAME = get_key('.env', 'DB_NAME')