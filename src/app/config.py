from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = os.environ.get("AUTHAPP_SECRET_KEY")
DATABASE = {
    "user": os.environ.get("AUTHAPP_DB_USER"),
    "password": os.environ.get("AUTHAPP_DB_PASSWORD"),
    "database": os.environ.get("AUTHAPP_DB_SCHEMA"),
}
