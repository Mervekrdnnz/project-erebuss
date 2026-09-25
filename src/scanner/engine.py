from src.graph.connection import Neo4jConnection

class AttackPathScanner:
    """
    Project Erebus - Graf Üzerinde Bulut Saldırı Yollarını Analiz Eden Tarayıcı Motoru
    """
    def __init__(self, connection: Neo4jConnection):
        self.db = connection

    def find_internet_to_admin_paths(self):
        """
        1. İnternete açık varlıklardan Admin rollerine uzanan yolları arar.
        """
        query = """
        MATCH path = (source)-[*1..5]->(target)
        WHERE (source.exposed_to_internet = true OR source.public_ip IS NOT NULL)
          AND target.admin = true
        RETURN path
        """
        return self._execute_path_query(query, "Admin Privilege Escalation")

    def find_public_s3_data_leaks(self):
        """
        2. İnternete açık ve hassas veri barındıran S3 Bucket'larını arar.
        """
        query = """
        MATCH (b:S3Bucket)
        WHERE b.public_access = true AND b.contains_sensitive_data = true
        RETURN b
        """
        results = []
        with self.db.connect().session() as session:
            res = session.run(query)
            for record in res:
                node = record["b"]
                results.append({
                    "type": "S3 Public Exposure",
                    "target": node.get("name"),
                    "description": f"İnternete açık S3 Bucket üzerinde hassas veri tespiti: [{node.get('name')}]"
                })
        return results

    def _execute_path_query(self, query: str, path_type: str):
        results = []
        with self.db.connect().session() as session:
            res = session.run(query)
            for record in res:
                path = record["path"]
                nodes = [node.get("name") or node.get("id") for node in path.nodes]
                relationships = [rel.type for rel in path.relationships]
                
                results.append({
                    "type": path_type,
                    "start": nodes[0],
                    "target": nodes[-1],
                    "steps_count": len(relationships),
                    "path_description": " -> ".join(
                        f"{nodes[i]} -[{relationships[i]}]->" for i in range(len(relationships))
                    ) + f" {nodes[-1]}"
                })
        return results