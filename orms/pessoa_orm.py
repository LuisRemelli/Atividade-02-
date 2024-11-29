from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor

# Função para inserir um contato
def insert_contato(entidade_id, tipo_contato_id, contato):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO pessoa.contato (entidade_id, public_tipo_contato_id, contato)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (entidade_id, tipo_contato_id, contato))
                contato_id = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": contato_id}
    except Exception as e:
        return {"message": "Erro ao inserir contato", "status": 400, "error": str(e)}


# Função para inserir um endereço
def insert_endereco(entidade_id, tipo_endereco_id, cidade_id, cep, logradouro, numero, bairro, complemento=None):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO pessoa.endereco (
                        entidade_id, public_tipo_endereco_id, public_cidade_id, 
                        cep, logradouro, numero, bairro, complemento
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (entidade_id, tipo_endereco_id, cidade_id, cep, logradouro, numero, bairro, complemento))
                endereco_id = cursor.fetchone()
                conn.commit()
                return {"message": "OK", "status": 201, "data": endereco_id}
    except Exception as e:
        return {"message": "Erro ao inserir endereço", "status": 400, "error": str(e)}


# Função para listar todas as pessoas
def get_pessoas():
    from datetime import date  # Import necessário para verificar o tipo de dado

    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        e.id AS entidade_id, e.nome, e.cpf, e.data_nascimento, e.ativo,
                        c.id AS contato_id, c.public_tipo_contato_id, c.contato,
                        en.id AS endereco_id, en.public_tipo_endereco_id, en.public_cidade_id,
                        en.cep, en.logradouro, en.numero, en.bairro, en.complemento
                    FROM pessoa.entidade e
                    LEFT JOIN pessoa.contato c ON e.id = c.entidade_id
                    LEFT JOIN pessoa.endereco en ON e.id = en.entidade_id;
                """
                cursor.execute(query)
                results = cursor.fetchall()

                pessoas = {}
                for row in results:
                    entidade_id = row["entidade_id"]
                    if entidade_id not in pessoas:
                        pessoas[entidade_id] = {
                            "ativo": "true" if row["ativo"] else "false",
                            "nome": row["nome"],
                            "cpf": row["cpf"],
                            "data_nascimento": (
                                row["data_nascimento"].isoformat()
                                if isinstance(row["data_nascimento"], date)
                                else None
                            ),
                            "contatos": [],
                            "enderecos": [],
                        }
                    if row["contato_id"]:
                        pessoas[entidade_id]["contatos"].append({
                            "id": row["contato_id"],
                            "tipo_contato": row["public_tipo_contato_id"],
                            "contato": row["contato"],
                        })
                    if row["endereco_id"]:
                        pessoas[entidade_id]["enderecos"].append({
                            "id": row["endereco_id"],
                            "tipo_endereco": row["public_tipo_endereco_id"],
                            "cidade_id": row["public_cidade_id"],
                            "cep": row["cep"],
                            "logradouro": row["logradouro"],
                            "numero": row["numero"],
                            "bairro": row["bairro"],
                            "complemento": row["complemento"],
                        })

                return {"message": "OK", "status": 200, "data": list(pessoas.values())}
    except Exception as e:
        return {"message": "Erro ao consultar pessoas", "status": 400, "error": str(e)}

# Função para buscar uma pessoa por ID
def get_pessoa_by_id(pessoa_id):
    from datetime import date  # Import necessário para verificar o tipo de dado

    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        e.id AS entidade_id, e.nome, e.cpf, e.data_nascimento, e.ativo,
                        c.id AS contato_id, c.public_tipo_contato_id, c.contato,
                        en.id AS endereco_id, en.public_tipo_endereco_id, en.public_cidade_id,
                        en.cep, en.logradouro, en.numero, en.bairro, en.complemento
                    FROM pessoa.entidade e
                    LEFT JOIN pessoa.contato c ON e.id = c.entidade_id
                    LEFT JOIN pessoa.endereco en ON e.id = en.entidade_id
                    WHERE e.id = %s;
                """
                cursor.execute(query, (pessoa_id,))
                results = cursor.fetchall()

                # Verifica se encontrou a pessoa
                if not results:
                    return {"message": "Pessoa não encontrada", "status": 404}

                # Consolida os dados
                pessoa = {
                    "ativo": "true" if results[0]["ativo"] else "false",
                    "nome": results[0]["nome"],
                    "cpf": results[0]["cpf"],
                    "data_nascimento": (
                        results[0]["data_nascimento"].isoformat()
                        if isinstance(results[0]["data_nascimento"], date)
                        else None
                    ),
                    "contatos": [],
                    "enderecos": [],
                }

                for row in results:
                    if row["contato_id"]:
                        pessoa["contatos"].append({
                            "id": row["contato_id"],
                            "tipo_contato": row["public_tipo_contato_id"],
                            "contato": row["contato"],
                        })
                    if row["endereco_id"]:
                        pessoa["enderecos"].append({
                            "id": row["endereco_id"],
                            "tipo_endereco": row["public_tipo_endereco_id"],
                            "cidade_id": row["public_cidade_id"],
                            "cep": row["cep"],
                            "logradouro": row["logradouro"],
                            "numero": row["numero"],
                            "bairro": row["bairro"],
                            "complemento": row["complemento"],
                        })

                return {"message": "OK", "status": 200, "data": pessoa}
    except Exception as e:
        return {"message": "Erro ao buscar pessoa", "status": 500, "error": str(e)}


# Função para inserir uma pessoa
def inserir_pessoa(pessoa):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO pessoa.entidade (ativo, nome, cpf, data_nascimento)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, ativo, nome, cpf, data_nascimento;
                """
                cursor.execute(query, (pessoa["ativo"], pessoa["nome"], pessoa["cpf"], pessoa["data_nascimento"]))
                nova_pessoa = cursor.fetchone()
                conn.commit()

                # Conversão de data_nascimento para string
                if nova_pessoa and "data_nascimento" in nova_pessoa:
                    nova_pessoa["data_nascimento"] = (
                        nova_pessoa["data_nascimento"].isoformat()
                        if nova_pessoa["data_nascimento"] else None
                    )

                return {"message": "OK", "status": 201, "data": nova_pessoa}
    except Exception as e:
        return {"message": "Erro ao inserir pessoa", "status": 400, "error": str(e)}

# Função para atualizar uma pessoa
def update_pessoa_orm(id, nome, cpf, data_nascimento, ativo):
    from datetime import date     
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    UPDATE pessoa.entidade
                    SET nome = %s, cpf = %s, data_nascimento = %s, ativo = %s
                    WHERE id = %s
                    RETURNING id, nome, cpf, data_nascimento, ativo;
                """
                
                cursor.execute(query, (nome, cpf, data_nascimento, ativo, id))
                updated_record = cursor.fetchone()

                if not updated_record:
                    return {"message": "Pessoa não encontrada", "status": 404}

                conn.commit()

                if isinstance(updated_record['data_nascimento'], date):
                    updated_record['data_nascimento'] = updated_record['data_nascimento'].strftime('%Y-%m-%d')

                return {"message": "OK", "status": 200, "data": updated_record}

    except Exception as e:
        return {"message": "Erro ao atualizar pessoa", "status": 500, "error": str(e)}


# Função para remover um endereço por ID
def delete_endereco_by_id(endereco_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Verifica se o endereço existe
                check_query = "SELECT id FROM pessoa.endereco WHERE id = %s"
                cursor.execute(check_query, (endereco_id,))
                if not cursor.fetchone():
                    return {"message": "Endereço não encontrado", "status": 404}

                # Remove o endereço
                delete_query = "DELETE FROM pessoa.endereco WHERE id = %s"
                cursor.execute(delete_query, (endereco_id,))
                conn.commit()
                return {"message": "OK", "status": 200}
    except Exception as e:
        return {"message": "Erro ao excluir endereço", "status": 400, "error": str(e)}
    
# Função para remover um contato
def delete_contato(contato_id):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    DELETE FROM pessoa.contato
                    WHERE id = %s
                    RETURNING id;
                """
                cursor.execute(query, (contato_id,))
                deleted_id = cursor.fetchone()

                if not deleted_id:
                    return {"message": "Contato não encontrado", "status": 400, "error": "ID não existe"}

                conn.commit()
                return {"message": "OK", "status": 200, "data": deleted_id}
    except Exception as e:
        # Log do erro no terminal ou logs
        print(f"Erro ao remover contato: {str(e)}")
        return {"message": "Erro ao remover contato", "status": 500, "error": str(e)}


