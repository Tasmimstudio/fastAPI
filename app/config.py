import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from neomodel import config

load_dotenv()

NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # no quotes needed
NEO4J_URI = os.getenv("NEO4J_URI")  # neo4j://localhost:7687

config.DATABASE_URL = f"{NEO4J_URI.replace('neo4j+s://', 'neo4j+s://')}"
if NEO4J_USER and NEO4J_PASSWORD:
    # URL-encode password
    encoded_password = quote_plus(NEO4J_PASSWORD)
    config.DATABASE_URL = f"neo4j+s://{NEO4J_USER}:{encoded_password}@{NEO4J_URI.split('://')[1]}"

print("[INFO] Connecting to Neo4j at:", config.DATABASE_URL)
