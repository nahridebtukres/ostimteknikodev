# SWOT — Ağ İzleme Ödev 1

Konu: Python ile localhost SSH failed-login / tekrarlı bağlantı izleme.

## Strengths (Güçlü yanlar)

- Tek Python dosyası, terminal arayüzü; GUI yok (ödev tercihi)
- Timestamp + 20 değişken anlamlı kullanılıyor
- Atak izi doğrudan görünür: `AUTH_FAILED`, `failed_login_count`, trafik ve bağlantı sayısı
- Proje içi lab SSH (2222) sistem ayarı istemez; Windows / Ubuntu / Pardus ortak kütüphanelerle çalışır
- Sonuç Excel’de iki sayfada durur: ham ölçüm ve ARTIS/AZALIS özeti

## Weaknesses (Zayıf yanlar)

- 200–250 satır sınırı gelişmiş grafik/filtrelemeyi engeller
- Ölçüm localhost lab ortamındadır; gerçek WAN gürültüsünü taşımaz
- `psutil.net_connections` bazı hesaplarda yetki ister; kısmi veri gelebilir
- XLSX Excel’de açıkken üzerine yazılamaz

## Opportunities (Fırsatlar)

- Aynı iskelet port tarama veya trafik anomalisi senaryosuna taşınabilir
- XLSX çıktısı derste gösterilen tablo analizine uygundur
- SWOT / BPMN / DFD / ERD ile süreç sınavda anlatılabilir
- Tur sayısı ve aralık sabitlerden kolayca değiştirilebilir

## Threats (Tehditler)

- `psutil` / `paramiko` / `openpyxl` kurulmazsa program başlamaz
- 2222 portu başka süreç tarafından tutulursa lab SSH açılamaz
- Yanlışlıkla gerçek/uzak SSH hedefine çevrilirse politika ihlali oluşur
- Python sürüm farkı (lab 3.15, geliştirme 3.12) paket kurulumunu etkileyebilir
