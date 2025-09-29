from neo4j import GraphDatabase

# Direct connection (no .env for now)
NEO4J_URI = "neo4j+s://a9c8236c.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Babymoana05"

print(f"Connecting to: {NEO4J_URI}")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

try:
    with driver.session() as session:
        result = session.run("RETURN '✅ Connection successful!' AS msg")
        print(result.single()["msg"])
except Exception as e:
    print("❌ Connection failed:", e)
finally:
    driver.close()
