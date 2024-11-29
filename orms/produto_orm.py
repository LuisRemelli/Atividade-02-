from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor
import logging

# Configuração do logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Função para inserir um produto
def inserir_produto(nome, sigla):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO produto.entidade (nome, sigla)
                    VALUES (%s, %s)
                    RETURNING id, nome, sigla;
                """
                cursor.execute(query, (nome, sigla))
                produto = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": produto}
    except Exception as e:
        logger.error(f"Erro ao inserir produto: {e}")
        return {"message": "Erro ao inserir produto", "status": 400, "error": str(e)}

# Função para listar produtos
def listar_produtos():
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id, nome, sigla FROM produto.entidade;
                """
                cursor.execute(query)
                produtos = cursor.fetchall()
                return {"message": "OK", "status": 200, "data": produtos}
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        return {"message": "Erro ao listar produtos", "status": 400, "error": str(e)}

# Função para atualizar um produto
def atualizar_produto(id, nome, sigla):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    UPDATE produto.entidade
                    SET nome = %s, sigla = %s
                    WHERE id = %s
                    RETURNING id, nome, sigla;
                """
                cursor.execute(query, (nome, sigla, id))
                produto_atualizado = cursor.fetchone()

                if not produto_atualizado:
                    return {"message": "Produto não encontrado", "status": 404}

                conn.commit()
                return {"message": "OK", "status": 200, "data": produto_atualizado}
    except Exception as e:
        logger.error(f"Erro ao atualizar produto: {e}")
        return {"message": "Erro ao atualizar produto", "status": 400, "error": str(e)}

# Funções para Safra
def inserir_safra(nome, sigla):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO produto.safra (nome, sigla)
                    VALUES (%s, %s)
                    RETURNING id, nome, sigla;
                """
                cursor.execute(query, (nome, sigla))
                safra = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": safra}
    except Exception as e:
        logger.error(f"Erro ao inserir safra: {e}")
        return {"message": "Erro ao inserir safra", "status": 500, "error": str(e)}

def listar_safras():
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id, nome, sigla FROM produto.safra;
                """
                cursor.execute(query)
                safras = cursor.fetchall()
                return {"message": "OK", "status": 200, "data": safras}
    except Exception as e:
        logger.error(f"Erro ao listar safras: {e}")
        return {"message": "Erro ao listar safras", "status": 500, "error": str(e)}

def atualizar_safra(id, nome, sigla):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    UPDATE produto.safra
                    SET nome = %s, sigla = %s
                    WHERE id = %s
                    RETURNING id, nome, sigla;
                """
                cursor.execute(query, (nome, sigla, id))
                safra_atualizada = cursor.fetchone()

                if not safra_atualizada:
                    return {"message": "Safra não encontrada", "status": 404}

                conn.commit()
                return {"message": "OK", "status": 200, "data": safra_atualizada}
    except Exception as e:
        logger.error(f"Erro ao atualizar safra: {e}")
        return {"message": "Erro ao atualizar safra", "status": 500, "error": str(e)}

# Funções para relação entre Produto e Safra
def relacionar_produto_safra(entidade_id, safra_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO produto.entidade_safra (entidade_id, safra_id)
                    VALUES (%s, %s)
                    RETURNING entidade_id, safra_id;
                """
                logger.debug(f"Relacionando entidade_id={entidade_id}, safra_id={safra_id}")
                cursor.execute(query, (entidade_id, safra_id))
                relacao = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": relacao}
    except Exception as e:
        logger.error(f"Erro ao relacionar produto com safra: {e}")
        return {"message": "Erro ao relacionar produto com safra", "status": 400, "error": str(e)}

def remover_relacao_produto_safra(entidade_id, safra_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    DELETE FROM produto.entidade_safra
                    WHERE entidade_id = %s AND safra_id = %s
                    RETURNING entidade_id, safra_id;
                """
                logger.debug(f"Removendo relação entidade_id={entidade_id}, safra_id={safra_id}")
                cursor.execute(query, (entidade_id, safra_id))
                relacao_removida = cursor.fetchone()

                if not relacao_removida:
                    return {"message": "Relação não encontrada", "status": 404}

                conn.commit()
                return {"message": "OK", "status": 200, "data": relacao_removida}
    except Exception as e:
        logger.error(f"Erro ao remover relação: {e}")
        return {"message": "Erro ao remover relação", "status": 400, "error": str(e)}
