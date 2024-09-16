import dotenv
import os

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_URL = os.getenv('ADMIN_URL')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
FILE_PATH = os.getenv('FILE_PATH')