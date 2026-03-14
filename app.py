import strawberry
from typing import List
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# 1. Defina o seu Modelo de Dados (Type)
@strawberry.type
class Livro:
    titulo: str
    autor: str

# 2. Crie a Query (onde os dados são buscados)
@strawberry.type
class Query:
    @strawberry.field
    def livros(self) -> List[Livro]:
        # Simulando dados que viriam do seu Neo4j
        return [
            Livro(titulo="O Senhor dos Anéis", autor="J.R.R. Tolkien"),
            Livro(titulo="Duna", autor="Frank Herbert"),
        ]

# 3. Crie o Schema
schema = strawberry.Schema(query=Query)

# 4. Configure o FastAPI para servir o GraphQL
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Opcional: Uma rota simples para a raiz não ficar vazia
@app.get("/")
def read_root():
    return {"message": "Servidor GraphQL ativo! Vá para /graphql para testar."}