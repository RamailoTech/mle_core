import os

class Neo4jSanityCheck:
    def __init__(self, connection):
        self.connection = connection

    def run_checks(self):
        with self.connection._driver.session() as session:
            try:
                self.check_accessibility(session)
                self.check_node_count(session)
                self.check_relationship_count(session)
                self.run_consistency_checks(session)
                self.check_orphaned_nodes(session)
                self.check_broken_relationships(session)
                self.check_duplicate_nodes(session)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def check_accessibility(self, session):
        try:
            result = session.run("RETURN 1")
            if result.single()[0] == 1:
                print("Database is accessible.")
        except Exception as e:
            print(f"Error accessing database: {e}")

    def check_node_count(self, session):
        try:
            result = session.run("MATCH (n) RETURN count(n) AS node_count")
            count = result.single()["node_count"]
            print(f"Node count: {count}")
        except Exception as e:
            print(f"Error checking node count: {str(e)}")

    def check_relationship_count(self, session):
        try:
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS rel_count")
            count = result.single()["rel_count"]
            print(f"Relationship count: {count}")
        except Exception as e:
            print(f"Error checking relationship count: {str(e)}")

    def run_consistency_checks(self, session):
        queries = {
            "Orphaned Nodes": "MATCH (n) WHERE NOT (n)--() RETURN COUNT(n)",
            "Broken Relationships": "MATCH ()-[r]->() WHERE NOT EXISTS(r) RETURN COUNT(r)",
            "Duplicate Nodes": """
                MATCH (n)
                WITH n.name AS name, COUNT(n) AS count
                WHERE count > 1
                RETURN name, count
            """
        }
        
        results = {}
        for check_name, query in queries.items():
            result = session.run(query)
            results[check_name] = result.single()[0] if result.single() else 0
        
        for check, result in results.items():
            print(f"{check}: {result}")

    def check_orphaned_nodes(self, session):
        try:
            result = session.run("MATCH (n) WHERE NOT (n)--() RETURN COUNT(n)")
            count = result.single()[0]
            print(f"Orphaned Nodes: Count(n): {count}")
        except Exception as e:
            print(f"Error checking orphaned nodes: {str(e)}")

    def check_broken_relationships(self, session):
        try:
            result = session.run("MATCH ()-[r]->() WHERE NOT EXISTS(r) RETURN COUNT(r)")
            count = result.single()[0]
            print(f"Broken Relationships: {count}")
        except Exception as e:
            print(f"Error checking broken relationships: {str(e)}")

    def check_duplicate_nodes(self, session):
        try:
            result = session.run("""
                MATCH (n)
                WITH n.name AS name, COUNT(n) AS count
                WHERE count > 1
                RETURN name, count
            """)
            duplicates = result.data()
            if duplicates:
                print("Duplicate Nodes found:")
                for record in duplicates:
                    print(f"Name: {record['name']}, Count: {record['count']}")
            else:
                print("No duplicate nodes found.")
        except Exception as e:
            print(f"Error checking duplicate nodes: {str(e)}")
