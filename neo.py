import os
import strawberry
from typing import List, Optional
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Configuração do Driver Neo4j
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PWD))

@strawberry.type
class Livro:
    titulo: str
    autor: str

@strawberry.type
class Query:
    @strawberry.field
    def livros(self) -> List[Livro]:
        with driver.session() as session:
            # Buscando o que a gente criar (Label: Livro)
            result = session.run("MATCH (l:Livro) RETURN l.titulo AS titulo, l.autor AS autor")
            return [
                Livro(titulo=record["titulo"], autor=record["autor"]) 
                for record in result
            ]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def criar_livro(self, titulo: str, autor: str) -> Livro:
        with driver.session() as session:
            # Cypher para criar o nó no Neo4j
            session.run(
                "CREATE (l:Livro {titulo: $titulo, autor: $autor})",
                titulo=titulo, autor=autor
            )
            return Livro(titulo=titulo, autor=autor)

# IMPORTANTE: Adicionar a Mutation no Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Acesse /graphql para usar a interface"}

app.include_router(GraphQLRouter(schema), prefix="/graphql")