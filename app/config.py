import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from neomodel import config

load_dotenv()

NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # no quotes needed
NEO4J_URI = os.getenv("NEO4J_URI")  # neo4j://localhost:7687

# URL-encode password (optional here)
encoded_password = quote_plus(NEO4J_PASSWORD)

config.DATABASE_URL = f"neo4j://{NEO4J_USER}:{encoded_password}@{NEO4J_URI.split('://')[1]}"

print("[ℹ️] Connecting to Neo4j at:", config.DATABASE_URL)
