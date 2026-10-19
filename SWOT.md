# SWOT Analizi — SSH Localhost Ağ İzleme

## Strengths (Güçlü Yanlar)

- Tek dosyada çalışan, anlaşılır ve teslimi kolay yapı
- Timestamp + 20 değişken ile düzenli XLSX çıktısı (ölçüm + özet sayfası)
- Failed-login ve tekrarlı bağlantı saldırı izlerine doğrudan bağlı metrikler
- Windows 11 ve Linux (Ubuntu/Pardus) için ortak `psutil` / `paramiko` kullanımı
- Proje içi lab SSH (`127.0.0.1:2222`, `lab_auth/`) sistem ayarı gerektirmez
- SSH reddi `AUTH_FAILED` olarak kaydedilir; servis hatasında program çökmez

## Weaknesses (Zayıf Yanlar)

- Kod satırı sınırı (200–250) nedeniyle gelişmiş analiz/filtreleme yok
- GUI ve veritabanı kullanılmıyor; görselleştirme sonradan yapılmalı
- Localhost senaryosu gerçek uzak ağ gürültüsünü tam yansıtmaz
- `net_connections` bazı ortamlarda yetki ister; kısmi veri gelebilir

## Opportunities (Fırsatlar)

- XLSX çıktısı Excel ile doğrudan analiz edilebilir
- Aynı iskelet farklı saldırı senaryolarına (port tarama, trafik anomalisi) uyarlanabilir
- Ders dokümanları (BPMN, DFD, ERD) ile süreç net anlatılabilir
- Laboratuvarda OpenSSH açılarak daha zengin auth log izi elde edilebilir

## Threats (Tehditler)

- OpenSSH kurulu/aktif değilse çoğu deneme `CONNECT_FAILED` olur
- Python veya paket sürüm farkları kurulum hatasına yol açabilir
- Yanlışlıkla gerçek/üretim SSH hedefine yöneltilirse güvenlik riski oluşur
- Yetkisiz ortamda tekrarlı giriş denemeleri politika ihlali sayılabilir (yalnız lab)
