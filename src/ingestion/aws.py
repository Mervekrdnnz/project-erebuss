import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError

class AWSScanner:
    """
    Project Erebus - AWS Envanter Verisi Çekme Modülü
    """
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name

    def fetch_mock_aws_data(self):
        """
        Çeşitli bulut yetki yükseltme (Privilege Escalation) senaryolarını içeren test envanteri.
        """
        return {
            "instances": [
                {
                    "id": "i-09988776655443322",
                    "name": "Prod-Payment-Gateway",
                    "public_ip": "54.210.12.1",
                    "exposed_to_internet": True,
                    "iam_role": "arn:aws:iam::123456789012:role/PaymentAppRole"
                },
                {
                    "id": "i-01122334455667788",
                    "name": "Dev-Testing-Server",
                    "public_ip": "34.201.55.90",
                    "exposed_to_internet": True,
                    "iam_role": "arn:aws:iam::123456789012:role/DevOpsRole"
                }
            ],
            "roles": [
                {
                    "arn": "arn:aws:iam::123456789012:role/PaymentAppRole",
                    "name": "PaymentAppRole",
                    "admin": False,
                    "can_assume": ["arn:aws:iam::123456789012:role/CloudAdminRole"],
                    "permissions": []
                },
                {
                    "arn": "arn:aws:iam::123456789012:role/DevOpsRole",
                    "name": "DevOpsRole",
                    "admin": False,
                    "can_assume": [],
                    "permissions": ["iam:PassRole", "ec2:RunInstances"]
                },
                {
                    "arn": "arn:aws:iam::123456789012:role/CloudAdminRole",
                    "name": "CloudAdminRole",
                    "admin": True,
                    "can_assume": [],
                    "permissions": ["*"]
                }
            ],
            "s3_buckets": [
                {
                    "name": "erebus-prod-db-backups",
                    "public_access": True,
                    "contains_sensitive_data": True
                }
            ]
        }

if __name__ == "__main__":
    scanner = AWSScanner()
    data = scanner.fetch_mock_aws_data()
    print("[+] AWS Envanteri Başarıyla Çekildi (Mock Data):")
    print(f"    - Bulunan Sunucu Sayısı  : {len(data['instances'])}")
    print(f"    - Bulunan Rol Sayısı      : {len(data['roles'])}")
    print(f"    - Bulunan S3 Bucket Sayısı: {len(data['s3_buckets'])}")