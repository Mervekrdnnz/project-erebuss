import argparse
from src.graph.connection import Neo4jConnection
from src.graph.builder import GraphBuilder
from src.ingestion.aws import AWSScanner
from src.scanner.engine import AttackPathScanner
from src.scanner.reporter import Reporter

def run_pipeline(report_format: str = "both", clear_db_only: bool = False):
    print("=== [PROJECT EREBUS - ATTACK PATH ENGINE] ===\n")
    
    # 1. Neo4j Bağlantısı
    db = Neo4jConnection(password="erebuspassword")
    if not db.verify_connectivity():
        print("[-] Veritabanı bağlantısı başarısız, işlem iptal ediliyor.")
        return

    builder = GraphBuilder(db)
    
    # Sadece veritabanı temizleme parametresi verildiyse
    if clear_db_only:
        builder.clear_database()
        print("[+] Graf veritabanı başarıyla temizlendi.")
        db.close()
        return

    # 2. Eski Verileri Temizle
    builder.clear_database()

    # 3. AWS Envanter Verisini Çek
    print("[*] AWS Envanteri Taranıyor...")
    aws_scanner = AWSScanner()
    data = aws_scanner.fetch_mock_aws_data()

    # 4. Verileri Neo4j Grafiğine Aktar
    print("[*] Varlıklar ve İlişkiler Grafiğe İşleniyor...")
    
    for role in data["roles"]:
        builder.create_node("IAMRole", {
            "id": role["arn"],
            "name": role["name"],
            "admin": role.get("admin", False)
        })

    for role in data["roles"]:
        for target_arn in role.get("can_assume", []):
            builder.create_relationship(
                role["arn"],
                "CAN_ASSUME_ROLE",
                target_arn,
                {"reason": "IAM Policy privilege escalation path"}
            )

    for instance in data["instances"]:
        builder.create_node("EC2Instance", {
            "id": instance["id"],
            "name": instance["name"],
            "public_ip": instance["public_ip"],
            "exposed_to_internet": instance.get("exposed_to_internet", True)
        })
        
        if instance.get("iam_role"):
            builder.create_relationship(
                instance["id"],
                "HAS_IAM_ROLE",
                instance["iam_role"]
            )

    for bucket in data.get("s3_buckets", []):
        builder.create_node("S3Bucket", {
            "id": bucket["name"],
            "name": bucket["name"],
            "public_access": bucket["public_access"],
            "contains_sensitive_data": bucket["contains_sensitive_data"]
        })

    print("[+] Graf veritabanı başarıyla güncellendi.\n")

    # 5. Saldırı Yollarını Tara
    print("[*] Saldırı Yolları (Attack Paths) Analiz Ediliyor...")
    scanner = AttackPathScanner(db)
    
    admin_paths = scanner.find_internet_to_admin_paths()
    s3_leaks = scanner.find_public_s3_data_leaks()

    total_findings = len(admin_paths) + len(s3_leaks)

    if total_findings > 0:
        print(f"\n[!] KRİTİK UYARI: Toplam {total_findings} Adet Güvenlik Zafiyeti Tespit Edildi!\n")
        
        # 6. Rapor Üretme
        reporter = Reporter()
        print("[+] Raporlar oluşturuluyor...")

        if report_format in ["json", "both"]:
            json_file = reporter.generate_json_report(admin_paths, s3_leaks)
            print(f"    - JSON Raporu: {json_file}")

        if report_format in ["html", "both"]:
            html_file = reporter.generate_html_report(admin_paths, s3_leaks)
            print(f"    - HTML Raporu: {html_file}")

        print()

    else:
        print("[+] Güvenli: Herhangi bir kritik zafiyet bulunamadı.")

    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Erebus - Cloud Attack Path Engine")
    parser.add_argument(
        "--format",
        choices=["json", "html", "both"],
        default="both",
        help="Çıktı rapor formatını belirler (json, html, both)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Sadece Neo4j veritabanını temizler ve çıkar"
    )

    args = parser.parse_args()
    run_pipeline(report_format=args.format, clear_db_only=args.clean)