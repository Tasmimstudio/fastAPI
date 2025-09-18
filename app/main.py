from fastapi import FastAPI
from app.config import config  # <-- make sure this is imported first
from neomodel import db
from neo4j.exceptions import AuthError, ServiceUnavailable
from app.routers import person

app = FastAPI(title="FastAPI + Neo4j")

app.include_router(person.router)

@app.on_event("startup")
def startup_db_check():
    try:
        db.cypher_query("RETURN 1")
        print("[✅] Neo4j connection successful!")
    except AuthError:
        print("[❌] Authentication failed: Check username/password.")
        raise
    except ServiceUnavailable:
        print("[❌] Cannot connect: Is Neo4j running?")
        raise
    except Exception as e:
        print(f"[❌] Neo4j connection failed: {e}")
        raise
