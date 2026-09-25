import pytest
from src.graph.connection import Neo4jConnection
from src.graph.builder import GraphBuilder
from src.scanner.engine import AttackPathScanner

@pytest.fixture(scope="module")
def neo4j_db():
    """Testler için veritabanı bağlantısı açar ve işi bitince kapatır."""
    db = Neo4jConnection(password="erebuspassword")
    yield db
    db.close()

@pytest.fixture(autouse=True)
def setup_test_graph(neo4j_db):
    """
    Her testten önce veritabanını temizler ve kontrol etmek istediğimiz
    örnek (sahte) bir graf yapısı kurar.
    """
    builder = GraphBuilder(neo4j_db)
    builder.clear_database()

    # Örnek Test Düğümleri
    builder.create_node("EC2Instance", {"id": "test-ec2", "name": "TestServer", "exposed_to_internet": True})
    builder.create_node("IAMRole", {"id": "role-1", "name": "TestRole1", "admin": False})
    builder.create_node("IAMRole", {"id": "role-admin", "name": "AdminRole", "admin": True})
    builder.create_node("S3Bucket", {"id": "s3-leak", "name": "leak-bucket", "public_access": True, "contains_sensitive_data": True})

    # Örnek Test İlişkileri
    builder.create_relationship("test-ec2", "HAS_IAM_ROLE", "role-1")
    builder.create_relationship("role-1", "CAN_ASSUME_ROLE", "role-admin")

def test_find_internet_to_admin_paths(neo4j_db):
    """1. Test: Tarayıcının 'Admin Yetki Yükseltme' yolunu bulup bulmadığını kontrol eder."""
    scanner = AttackPathScanner(neo4j_db)
    paths = scanner.find_internet_to_admin_paths()

    # Beklentilerimiz (Assertions)
    assert len(paths) == 1
    assert paths[0]["start"] == "TestServer"
    assert paths[0]["target"] == "AdminRole"
    assert paths[0]["steps_count"] == 2

def test_find_public_s3_data_leaks(neo4j_db):
    """2. Test: Tarayıcının 'S3 Veri Sızıntısını' bulup bulmadığını kontrol eder."""
    scanner = AttackPathScanner(neo4j_db)
    leaks = scanner.find_public_s3_data_leaks()

    # Beklentilerimiz (Assertions)
    assert len(leaks) == 1
    assert leaks[0]["target"] == "leak-bucket"