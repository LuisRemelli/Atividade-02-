from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def inserir_grupo_producao(nome, ativo):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO grupo_producao.entidade (nome, ativo)
                    VALUES (%s, %s)
                    RETURNING id, nome, ativo;
                """
                cursor.execute(query, (nome, ativo))
                grupo = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": grupo}
    except Exception as e:
        logger.error(f"Erro ao inserir grupo de produção: {e}")
        return {"message": "Erro ao inserir grupo de produção", "status": 400, "error": str(e)}

def listar_grupos_producao():
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT id, nome, ativo FROM grupo_producao.entidade;"
                cursor.execute(query)
                grupos = cursor.fetchall()
                return {"message": "OK", "status": 200, "data": grupos}
    except Exception as e:
        logger.error(f"Erro ao listar grupos de produção: {e}")
        return {"message": "Erro ao listar grupos de produção", "status": 400, "error": str(e)}

def listar_grupo_por_id(grupo_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT id, nome, ativo FROM grupo_producao.entidade WHERE id = %s;"
                cursor.execute(query, (grupo_id,))
                grupo = cursor.fetchone()
                if grupo:
                    return {"message": "OK", "status": 200, "data": grupo}
                else:
                    return {"message": "Grupo de produção não encontrado", "status": 404}
    except Exception as e:
        logger.error(f"Erro ao listar grupo de produção por ID: {e}")
        return {"message": "Erro ao listar grupo de produção", "status": 400, "error": str(e)}

def atualizar_grupo_producao(grupo_id, nome, ativo):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    UPDATE grupo_producao.entidade
                    SET nome = %s, ativo = %s
                    WHERE id = %s
                    RETURNING id, nome, ativo;
                """
                cursor.execute(query, (nome, ativo, grupo_id))
                grupo = cursor.fetchone()
                conn.commit()
                if grupo:
                    return {"message": "OK", "status": 200, "data": grupo}
                else:
                    return {"message": "Grupo de produção não encontrado", "status": 404}
    except Exception as e:
        logger.error(f"Erro ao atualizar grupo de produção: {e}")
        return {"message": "Erro ao atualizar grupo de produção", "status": 400, "error": str(e)}
