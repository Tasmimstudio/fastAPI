import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from neomodel import config

# Load variables from .env
load_dotenv()

NEO4J_URI = os.getenv("neo4j+s://cd3d134b.databases.neo4j.io")
NEO4J_USER = os.getenv("neo4j")
NEO4J_PASSWORD = os.getenv("hXIk1yeZPYikOlfvyKpIUcvX7HoEYPadIOdw7T05MjI")

if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
    raise ValueError("❌ Missing Neo4j environment variables (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)")

# URL-encode password for safety
encoded_password = quote_plus(NEO4J_PASSWORD)

config.DATABASE_URL = f"neo4j+s://{NEO4J_USER}:{encoded_password}@{NEO4J_URI.split('://')[1]}"

print("[INFO] Connecting to Neo4j at:", config.DATABASE_URL)
