import os

class Neo4jSanityCheck:
    def __init__(self, connection):
        self.connection = connection

    def run_checks(self):
        results= {}
        with self.connection._driver.session() as session:
            try:
                results["accessibility"] = self.check_accessibility(session)
                results["node_count"] = self.check_node_count(session)
                results["relationship_count"] = self.check_relationship_count(session)
                results["orphaned_nodes"] = self.check_orphaned_nodes(session)
                results["broken_relationships"] = self.check_broken_relationships(session)
                results["duplicate_nodes"] = self.check_duplicate_nodes(session)
                return results
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def check_accessibility(self, session):
        try:
            result = session.run("RETURN 1")
            if result.single()[0] == 1:
                return "True"
        except Exception as e:
            print(f"Error accessing database: {e}")

    def check_node_count(self, session):
        try:
            result = session.run("MATCH (n) RETURN count(n) AS node_count")
            count = result.single()["node_count"]
            return count
        except Exception as e:
            print(f"Error checking node count: {str(e)}")

    def check_relationship_count(self, session):
        try:
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS rel_count")
            count = result.single()["rel_count"]
            return count
        except Exception as e:
            print(f"Error checking relationship count: {str(e)}")



    def check_orphaned_nodes(self, session):
        try:
            result = session.run("MATCH (n) WHERE NOT (n)--() RETURN COUNT(n)")
            count = result.single()[0]
            return count
        except Exception as e:
            print(f"Error checking orphaned nodes: {str(e)}")

    def check_broken_relationships(self, session):
        try:
            result = session.run("""
                MATCH (a)-[r]->(b)
                WHERE a IS NULL OR b IS NULL
                RETURN COUNT(r) AS brokenCount
            """)
            count = result.single()["brokenCount"]
            return count
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
            return duplicates
        except Exception as e:
            print(f"Error checking duplicate nodes: {str(e)}")