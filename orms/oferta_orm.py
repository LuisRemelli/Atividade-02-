from database.connectionDb import ConnectionDb
from psycopg2.extras import RealDictCursor

def insert_oferta(entidade_id, endereco=None, produtos=None, contatos=None, bids=None):
    try:
        with ConnectionDb.get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Insere a entidade principal com apenas os campos existentes
                query_entidade = """
                    INSERT INTO oferta.entidade (id, situacao)
                    VALUES (%s, %s)
                    RETURNING id;
                """
                # Define valores padrão para `situacao`
                situacao = 1  # Exemplo: 1 para "ativo"
                cursor.execute(query_entidade, (entidade_id, situacao))
                oferta_id = cursor.fetchone()["id"]

                # Insere o endereço, se fornecido
                if endereco:
                    query_endereco = """
                        INSERT INTO oferta.endereco (
                            entidade_id, public_cidade_id, tipo_endereco, cep, logradouro, numero, bairro, complemento
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """
                    cursor.execute(query_endereco, (
                        oferta_id,
                        endereco.get("public_cidade_id"),
                        endereco.get("tipo_endereco"),
                        endereco.get("cep"),
                        endereco.get("logradouro"),
                        endereco.get("numero"),
                        endereco.get("bairro"),
                        endereco.get("complemento")
                    ))
                    endereco_id = cursor.fetchone()["id"]

                # Insere os produtos, se fornecidos
                if produtos:
                    query_produto = """
                        INSERT INTO oferta.produto (
                            entidade_id, produto_entidade_id, produto_safra_id, volume, public_unidade_medida_id, 
                            public_moeda_id, preco, public_tipo_preco
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """
                    for produto in produtos:
                        cursor.execute(query_produto, (
                            oferta_id,
                            produto.get("produto_entidade_id"),
                            produto.get("produto_safra_id"),
                            produto.get("volume"),
                            produto.get("public_unidade_medida_id"),
                            produto.get("public_moeda_id"),
                            produto.get("preco"),
                            produto.get("public_tipo_preco")
                        ))

                # Insere os contatos, se fornecidos
                if contatos:
                    query_contato = """
                        INSERT INTO oferta.contato (
                            entidade_id, pessoa_entidade_id
                        ) VALUES (%s, %s)
                        RETURNING id;
                    """
                    for contato in contatos:
                        cursor.execute(query_contato, (
                            oferta_id,
                            contato.get("pessoa_entidade_id")
                        ))

                # Insere os bids, se fornecidos
                if bids:
                    query_bid = """
                        INSERT INTO oferta.bid (
                            entidade_id, pessoa_entidade_id, valor
                        ) VALUES (%s, %s, %s)
                        RETURNING id;
                    """
                    for bid in bids:
                        cursor.execute(query_bid, (
                            oferta_id,
                            bid.get("pessoa_entidade_id"),
                            bid.get("valor")
                        ))

                conn.commit()
                return {"message": "Oferta criada com sucesso", "status": 201, "data": {"oferta_id": oferta_id}}
    except Exception as e:
        return {"message": "Erro ao criar oferta", "status": 400, "error": str(e)}

