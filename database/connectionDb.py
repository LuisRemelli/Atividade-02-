import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class ConnectionDb:
    @staticmethod
    def get_db():
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
