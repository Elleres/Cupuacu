# Portal - LABES
 Esse projeto é um software que foi desenvolvido para a disciplina Laboratório de Engenharia de Software 

Esse readme irá conter algumas informações sobre a organização do projeto.
## O que deve ficar em cada pasta?

### alembic
Contém os scripts de migração de banco de dados.
Arquivos gerados pelo Alembic (versions/ com os scripts de migração) e env.py. Não coloque lógica de aplicação aqui.

### api
Contém as rotas (endpoints) da aplicação. As pastas dentro contém versões da API e dentro das versões divide por 
recurso, ex: user.py, auth.py, items.py. Cada arquivo define rotas com @router.get, @router.post, etc. Um __init__.py 
para montar os routers em um main.py.

### db
Contém configurações do banco de dados. Conexão com o banco (ex: SessionLocal, engine, Base). Inicialização do banco. 
Dependência de get_db.

### models
Contém os modelos ORM (SQLAlchemy). Cada arquivo pode conter um modelo, ex: user.py, item.py. Os modelos herdam de Base 
e mapeiam tabelas.

### repositories
Contém a lógica de acesso ao banco de dados. Funções que realizam CRUD usando os modelos e sessões do SQLAlchemy. 
Ex: get_user_by_email, create_user, list_items, etc. Repositórios são usados nos serviços.
### schemas
Contém os schemas do Pydantic. Define as formas de entrada e saída de dados (validação). Ex: UserCreate, UserRead, 
ItemUpdate. Evita expor diretamente os modelos ORM.

### services

Contém a lógica de negócio. Regras de negócio que usam os repositórios. Ex: envio de e-mail, verificação de senha, 
cálculo de preços. Pode ser dividido por contexto (ex: user_service.py).