from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor
def get_unidades_medida():
    conn = ConnectionDb.get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT id, nome, sigla FROM public.unidade_medida;"
        cursor.execute(query)
        unidades = cursor.fetchall()
        return {"message": "OK", "data": unidades}
    except Exception as e:
        print(f"Erro: {e}")
        return {"message": "Falha ao consultar unidades de medida", "status": 400}
    finally:
        cursor.close()
        conn.close()
