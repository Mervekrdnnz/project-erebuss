# Project Erebus - Cloud Attack Path Analysis Engine

**Project Erebus**, AWS altyapılarındaki karmaşık güvenlik ilişkilerini, yetki yükseltme zincirlerini (Privilege Escalation) ve veri sızıntısı risklerini grafik veritabanı (Graph Database) yaklaşımıyla analiz eden açık kaynaklı bir güvenlik tarama aracıdır.

---

## 🚀 Özellikler

- **Graf Tabanlı Saldırı Analizi:** Neo4j kullanarak varlıklar (EC2, IAM Role, S3) ve yetkiler arasındaki ilişkileri modeller.
- **Yetki Yükseltme Tespiti (Privilege Escalation):** İnternete açık sunuculardan başlayıp Admin yetkisine ulaşan rol zincirlerini (`CAN_ASSUME_ROLE`) otomatik tespit eder.
- **Hassas Veri Sızıntısı Analizi:** İnternete açık ve hassas veri barındıran S3 depolama alanlarını saptar.
- **Esnek Raporlama:** Bulguları otomatik olarak zaman damgalı **JSON** veya görsel **HTML** raporlarına dönüştürür.
- **Birim Testleri:** `pytest` ile desteklenen test altyapısı sayesinde yüksek kod kalitesi.

---

## 🛠️ Mimari ve Teknolojiler

- **Dil:** Python 3.13+
- **Veritabanı:** Neo4j (Docker ortamında)
- **Test Çerçevesi:** Pytest
- **Raporlama:** Custom HTML/JSON Engine

---

## 📋 Kurulum ve Çalıştırma

### 1. Gereksinimler & Neo4j Başlatma
Docker Container üzerinde Neo4j veritabanını ayağa kaldırın:

```bash
docker-compose up -d