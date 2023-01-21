from os import getenv as env
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

a = env('POSTGRES_HOST')
print(a)
