import os
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

# COMMON
DEBUG = os.getenv("DEBUG") == "1"

# POSTGRES
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# RABBITMQ
AMQP_URI = os.getenv("AMQP_URI")

templates = Jinja2Templates(directory='templates/html')
static_files = StaticFiles(directory='templates/static')




