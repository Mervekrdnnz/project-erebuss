import json
import os
from datetime import datetime

class Reporter:
    """
    Project Erebus - Tarama Bulgularını JSON ve HTML Raporlarına Dönüştüren Modül
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_json_report(self, admin_paths: list, s3_leaks: list, filename: str = None) -> str:
        """Bulguları JSON formatında kaydeder."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"erebus_report_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        report_data = {
            "scan_time": datetime.now().isoformat(),
            "summary": {
                "total_vulnerabilities": len(admin_paths) + len(s3_leaks),
                "privilege_escalation_paths": len(admin_paths),
                "s3_data_leaks": len(s3_leaks)
            },
            "findings": {
                "privilege_escalations": admin_paths,
                "s3_leaks": s3_leaks
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

        return filepath

    def generate_html_report(self, admin_paths: list, s3_leaks: list, filename: str = None) -> str:
        """Bulguları görsel bir HTML raporu olarak kaydeder."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"erebus_report_{timestamp}.html"

        filepath = os.path.join(self.output_dir, filename)
        
        paths_html = ""
        for idx, p in enumerate(admin_paths, 1):
            paths_html += f"""
            <div class="card card-path">
                <h3>Patika #{idx}: {p['start']} &rarr; {p['target']}</h3>
                <p><strong>Adım Sayısı:</strong> {p['steps_count']}</p>
                <p><strong>Saldırı Akışı:</strong> <code>{p['path_description']}</code></p>
            </div>
            """

        leaks_html = ""
        for idx, s in enumerate(s3_leaks, 1):
            leaks_html += f"""
            <div class="card card-leak">
                <h3>Risk #{idx}: S3 Veri Sızıntısı</h3>
                <p>{s['description']}</p>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Project Erebus - Güvenlik Tarama Raporu</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }}
                h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
                .summary {{ display: flex; gap: 20px; margin-bottom: 30px; }}
                .stat-box {{ background-color: #1e293b; padding: 20px; border-radius: 8px; flex: 1; text-align: center; border: 1px solid #334155; }}
                .stat-box h2 {{ margin: 0; font-size: 32px; color: #f43f5e; }}
                .stat-box p {{ margin: 5px 0 0 0; color: #94a3b8; }}
                .section-title {{ color: #e2e8f0; margin-top: 30px; border-left: 4px solid #38bdf8; padding-left: 10px; }}
                .card {{ background-color: #1e293b; border-radius: 8px; padding: 15px 20px; margin-bottom: 15px; border: 1px solid #334155; }}
                .card-path {{ border-left: 4px solid #f43f5e; }}
                .card-leak {{ border-left: 4px solid #fbbf24; }}
                code {{ background-color: #0f172a; padding: 4px 8px; border-radius: 4px; color: #38bdf8; font-family: monospace; }}
            </style>
        </head>
        <body>
            <h1>Project Erebus - Bulut Saldırı Yolu Analiz Raporu</h1>
            <p><strong>Tarih:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="summary">
                <div class="stat-box">
                    <h2>{len(admin_paths) + len(s3_leaks)}</h2>
                    <p>Toplam Zafiyet</p>
                </div>
                <div class="stat-box">
                    <h2>{len(admin_paths)}</h2>
                    <p>Yetki Yükseltme Patikası</p>
                </div>
                <div class="stat-box">
                    <h2>{len(s3_leaks)}</h2>
                    <p>S3 Veri Sızıntısı</p>
                </div>
            </div>

            <h2 class="section-title">Yetki Yükseltme Patikaları</h2>
            {paths_html if paths_html else "<p>Kritik patika bulunamadı.</p>"}

            <h2 class="section-title">S3 Veri Sızıntıları</h2>
            {leaks_html if leaks_html else "<p>Veri sızıntısı bulunamadı.</p>"}
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return filepath