from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor

# Função para inserir um cliente
def insert_cliente(grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO cliente.entidade (grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz))
                cliente_id = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": cliente_id}
    except Exception as e:
        return {"message": "Erro ao inserir cliente", "status": 400, "error": str(e)}


# Função para atualizar um cliente
def update_cliente(id, grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    UPDATE cliente.entidade
                    SET grupo_producao_entidade_id = %s, tipo_pessoa = %s, razao_social = %s, nome_fantasia = %s, documento = %s, matriz = %s
                    WHERE id = %s
                    RETURNING id, grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz;
                """
                cursor.execute(query, (grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz, id))
                updated_cliente = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 200, "data": updated_cliente}
    except Exception as e:
        return {"message": "Erro ao atualizar cliente", "status": 400, "error": str(e)}


# Função para listar todos os clientes
def get_clientes():
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id, grupo_producao_entidade_id, tipo_pessoa, razao_social, nome_fantasia, documento, matriz
                    FROM cliente.entidade;
                """
                cursor.execute(query)
                clientes = cursor.fetchall()
                return {"message": "OK", "status": 200, "data": clientes}
    except Exception as e:
        return {"message": "Erro ao listar clientes", "status": 400, "error": str(e)}


# Função para inserir contato de cliente
def insert_cliente_contato(entidade_id, pessoa_entidade_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO cliente.contato (entidade_id, pessoa_entidade_id)
                    VALUES (%s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (entidade_id, pessoa_entidade_id))
                contato_id = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": contato_id}
    except Exception as e:
        print(f"Erro ao inserir contato de cliente: {str(e)}")
        return {"message": "Erro ao inserir contato de cliente", "status": 400, "error": str(e)}

# Função para validar se um ID de entidade existe no banco de dados
def validate_entidade_id(entidade_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT 1 FROM cliente.entidade WHERE id = %s;"
                cursor.execute(query, (entidade_id,))
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao validar entidade_id: {str(e)}")
        return False

