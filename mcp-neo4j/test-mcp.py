#\!/usr/bin/env python3
import os
from neo4j import GraphDatabase

uri = os.getenv('NEO4J_URL', 'bolt://localhost:7687')
username = os.getenv('NEO4J_USERNAME', 'neo4j')
password = os.getenv('NEO4J_PASSWORD', 'password123')

print(f"Connecting to {uri} as {username}")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        print(f"Connection successful\! Test query returned: {record['test']}")
    driver.close()
except Exception as e:
    print(f"Failed to connect: {e}")
