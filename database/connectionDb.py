#  Conexao com o banco
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class ConnectionDb:
    
    def get_db():
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn