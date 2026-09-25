import os
from neo4j import GraphDatabase, Driver

class Neo4jConnection:
    """
    Project Erebus - Neo4j Veritabanı Sürücü Yönetici Sınıfı
    """
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")  # Neo4j Desktop'ta belirlediğin şifre
        self._driver: Driver = None

    def connect(self):
        if not self._driver:
            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()

    def verify_connectivity(self) -> bool:
        """
        Veritabanı bağlantısını test eder ve durum döner.
        """
        try:
            driver = self.connect()
            driver.verify_connectivity()
            print("[+] Neo4j veritabanına başarıyla bağlandı!")
            return True
        except Exception as e:
            print(f"[-] Neo4j bağlantı hatası: {e}")
            return False

if __name__ == "__main__":
    # Bağlantıyı test et
    # Not: 'password' yerine Neo4j Desktop'ta belirlediğin şifreyi gir!
    db = Neo4jConnection(password="erebuspassword") 
    db.verify_connectivity()
    db.close()