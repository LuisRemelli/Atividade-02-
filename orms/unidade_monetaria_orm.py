from psycopg2.extras import RealDictCursor
import hashlib
from database.connectionDb import ConnectionDb

def get_unidades_monetarias():
    conn = ConnectionDb.get_db() 
    cursor = conn.cursor()
    try:

        query = "SELECT id, nome, sigla FROM public.moeda;"
        cursor.execute(query)
        moedas = cursor.fetchall()

        # Estrutura da resposta
        data = [
            {"id": moeda[0], "nome": moeda[1], "sigla": moeda[2]}
            for moeda in moedas
        ]
        return {"message": "OK", "data": data}
    except:
        return {"message": "Falha ao consultar unidades monetarias", "status": 400}
    finally:
        # Fecha a conexão
        cursor.close()
        conn.close()
