# Agrinvest Brokers (AB) - Backend em Python 🌾

Este projeto é o backend do sistema da Agrinvest Brokers. Desenvolvido em Python, ele oferece funcionalidades completas para a operação da plataforma, integrando-se a bancos de dados SQL e permitindo o gerenciamento de dados de forma segura e eficiente.

## 👨🏻‍💻 Sobre o Projeto
O objetivo deste backend é fornecer suporte robusto e escalável para a Agrinvest Brokers, incluindo funcionalidades essenciais como autenticação, criptografia, integração com S3, webhooks e outras ferramentas necessárias para o funcionamento do sistema.

## 📦 Estrutura do Projeto
A estrutura a seguir foi organizada para facilitar a escalabilidade e manutenção do sistema:

```bash
├── Dockerfile                  # Configuração do Docker para execução em container
├── README.md                   # Documentação do projeto
├── app.py                      # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
├── blacklist.py                # Variável global para gerenciamento de tokens JWT em blacklist
├── auth                        # Autenticação e criptografia
│   ├── cryptdecrypt.py         # Gerenciamento de criptografia
│   └── managertk.py            # Gerenciamento de tokens
├── models                      # Modelos de dados da aplicação
├── routes                      # Definição das rotas da API
├── orm                         # Operações com banco de dados
├── controllers                 # Funcionalidades principais da aplicação
└── utils                       # Utilitários auxiliares para operações gerais
```

## ⬇️ Instalação
Certifique-se de ter o Python 3.12 (ou superior) instalado antes de iniciar.

1. Clone este repositório em seu ambiente local.
2. Acesse a pasta do projeto no terminal.
3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```
4. Execute a aplicação:
```bash
python3 app.py
```

## 🐳 Docker
Este projeto inclui um Dockerfile para facilitar o uso em containers. Para configurar e rodar a aplicação usando o Docker, siga os passos abaixo:

1. Certifique-se de ter o Docker instalado no ambiente.
2. No diretório do projeto, construa a imagem Docker:
```bash
docker build -t agrinvest-backend .
```
3. Inicie o contêiner com o seguinte comando:
```bash
docker run -d --restart=always --name agrinvestAPI -p 5001:5001 -v $(pwd):/api agrinvest-backend
```
Parâmetros importantes:
* -d: Executa o contêiner em segundo plano.
* --restart=always: Garante que o contêiner reinicie automaticamente em caso de falha.
*  --name agrinvestAPI: Define o nome do contêiner.
*  -p 5001:5001: Mapeia a porta 5001 do contêiner para o host local.
*  -v $(pwd):/api: Sincroniza o diretório do projeto com o contêiner, refletindo mudanças feitas no código.

## ⚙️ Configurações
As configurações de variáveis de ambiente, como credenciais de banco de dados e chaves de acesso, estão no arquivo .env. Configure essas variáveis conforme necessário para o ambiente de desenvolvimento e produção.

## 🔑 Configuração das Variáveis de Ambiente

É extremamente importante configurar as variáveis de ambiente abaixo para garantir o funcionamento correto e seguro da aplicação:
```bash
DATABASE_URL=
TOKEN_HOURS_VALIDATE=
BLOWFISH_KEY=
JWT_SECRET_KEY=
GRAYLOG_HOST=
GRAYLOG_PORT=
```

Descrição das variáveis:
* DATABASE_URL: String de conexão com o banco de dados. Este é um parâmetro essencial para o funcionamento da aplicação.
* TOKEN_HOURS_VALIDATE: Define a quantidade de horas que o token de autenticação é válido.
* BLOWFISH_KEY: Chave de criptografia usada para proteger dados sensíveis. Esta chave é indispensável para operações de segurança no sistema.
* JWT_SECRET_KEY: Chave secreta usada para gerar e validar tokens JWT. Sem esta chave, a autenticação via JWT não funcionará.

Para as variáveis de `GRAYLOG_HOST` e `GRAYLOG_PORT`, você pode deixá-las em branco inicialmente, pois ainda não estão integradas e não afetam o funcionamento do sistema no momento.

Entretanto, `DATABASE_URL`, `BLOWFISH_KEY`, `JWT_SECRET_KEY` e `TOKEN_HOURS_VALIDATE` são obrigatórias para a aplicação operar corretamente.
