from src.graph.connection import Neo4jConnection

class GraphBuilder:
    """
    AWS Varlıklarını ve İlişkilerini Neo4j Grafik Veritabanına Yükleyen Sınıf
    """
    def __init__(self, connection: Neo4jConnection):
        self.db = connection

    def clear_database(self):
        """Tüm grafiği temizler (Geliştirme / Test aşaması için)"""
        query = "MATCH (n) DETACH DELETE n"
        with self.db.connect().session() as session:
            session.run(query)
        print("[*] Veritabanı temizlendi.")

    def create_node(self, label: str, properties: dict):
        """Genel bir düğüm (Node) oluşturur veya günceller (MERGE)"""
        # Node kimliği olarak 'arn' veya 'id' kullanıyoruz
        node_id = properties.get("arn") or properties.get("id")
        
        query = f"""
        MERGE (n:{label} {{id: $node_id}})
        SET n += $properties
        RETURN n
        """
        with self.db.connect().session() as session:
            session.run(query, node_id=node_id, properties=properties)

    def create_relationship(self, source_id: str, rel_type: str, target_id: str, properties: dict = None):
        """İki düğüm arasında yönlü bir ilişki (Relationship / Attack Step) oluşturur"""
        properties = properties or {}
        query = f"""
        MATCH (a {{id: $source_id}})
        MATCH (b {{id: $target_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $properties
        RETURN r
        """
        with self.db.connect().session() as session:
            session.run(query, source_id=source_id, target_id=target_id, properties=properties)


if __name__ == "__main__":
    # Test Senaryosu: Bir Saldırı Yolu Simülasyonu
    db = Neo4jConnection(password="erebuspassword")
    builder = GraphBuilder(db)

    # 1. Veritabanını Temizle
    builder.clear_database()

    # 2. Örnek Düğümler (Nodes) Oluştur
    print("[+] Örnek AWS Varlıkları Oluşturuluyor...")
    builder.create_node("AWSAccount", {"id": "123456789012", "name": "Prod-Account"})
    
    # İnternete açık bir EC2 Sunucusu
    builder.create_node("EC2Instance", {
        "id": "i-0abc123def456", 
        "name": "Web-Server", 
        "public_ip": "1.2.3.4", 
        "exposed_to_internet": True
    })
    
    # EC2 üzerinde ekli IAM Rolü
    builder.create_node("IAMRole", {
        "id": "arn:aws:iam::123456789012:role/WebServerRole", 
        "name": "WebServerRole"
    })
    
    # Yüksek Yetkili Admin Rolü
    builder.create_node("IAMRole", {
        "id": "arn:aws:iam::123456789012:role/AdministratorRole", 
        "name": "AdministratorRole",
        "admin": True
    })

    # 3. İlişkileri (Edges / Saldırı Adımlarını) Bağla
    print("[+] Saldırı Yolu İlişkileri Bağlanıyor...")
    
    # EC2 sunucusu IAM Rolüne sahip
    builder.create_relationship(
        "i-0abc123def456", 
        "HAS_IAM_ROLE", 
        "arn:aws:iam::123456789012:role/WebServerRole"
    )
    
    # WebServerRole, AdministratorRole yetkisini devralabiliyor (Privilege Escalation / Privilege Misconfiguration)
    builder.create_relationship(
        "arn:aws:iam::123456789012:role/WebServerRole", 
        "CAN_ASSUME_ROLE", 
        "arn:aws:iam::123456789012:role/AdministratorRole",
        {"reason": "sts:AssumeRole misconfiguration"}
    )

    db.close()
    print("[+] Test grafiği başarıyla oluşturuldu!")