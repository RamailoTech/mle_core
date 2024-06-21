from neo4j import GraphDatabase
import json
import os

class Neo4jConnector:
    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri or os.environ.get('NEO4J_URI')
        self.user = user or os.environ.get('NEO4J_USERNAME')
        self.password = password or os.environ.get('NEO4J_PASSWORD')

        if not self.uri or not self.user or not self.password:
            raise ValueError("URI, username, and password must be provided either as arguments or environment variables.")
        
        self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self._driver.close()

    def query(self, cypher_query, parameters=None, db=None):
        with self._driver.session(database=db) if db else self._driver.session() as session:
            try:
                result = session.run(cypher_query, parameters)
                data = json.dumps([record.data() for record in result], indent=4)
                return data 
            except Exception as error:
                print('Query error:', error)
                return None
