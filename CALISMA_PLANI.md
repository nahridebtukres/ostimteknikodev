# Çalışma Planı — SSH Localhost Ağ İzleme

## Ödev özeti

Tek Python dosyasında (`ag_izleme.py`), proje içi lab SSH (`127.0.0.1:2222`) üzerinde bilinçli başarısız giriş denemeleri yapılırken 20 ağ/sistem değişkeni toplanır, her ölçüme timestamp eklenir ve sonuçlar tek dosya olarak `ssh_monitor_log.xlsx` içine yazılır (Sayfa1: ölçümler, Sayfa2: Özet). Sistem SSH ayarına dokunulmaz; yetki `lab_auth/` dizinindedir. GUI yoktur. Kod yaklaşık 200–250 satırdır (yorumlar hariç). AI promptları hem `.py` dosyasının sonunda hem `AI_PROMPTS.md` içindedir.

## Kilitlelen kararlar

- Hedef: `127.0.0.1:2222` (proje içi lab SSH)
- Yetki dizini: `lab_auth/users.txt` ve `lab_auth/host_key` (ilk çalıştırmada oluşur)
- Atak odağı: Failed-login + Repeated connection attempts (+ Unauthorized-access izi)
- Depolama: tek dosya `ssh_monitor_log.xlsx` (2 sayfa)
- Bağımlılıklar: `psutil`, `paramiko`, `openpyxl`
- İstemci doğru şifreyi kullanmaz; beklenen durum `AUTH_FAILED`

## 20 değişken ve seçilme gerekçeleri

| # | Değişken | Gerekçe (atak izi) |
|---|----------|--------------------|
| 1 | interface_name | Trafiğin geçtiği arayüzü tanımlar |
| 2 | local_ip | Kaynak adresi; tekrarlı denemelerin yereli |
| 3 | remote_ip | SSH hedefi (127.0.0.1) |
| 4 | remote_port | Hedef port (22) |
| 5 | local_port | İstemci tarafı ephemeral port |
| 6 | transport_protocol | SSH taşıma katmanı (TCP) |
| 7 | connection_state | Bağlantı/auth sonucu durumu |
| 8 | active_connection_count | Tekrarlı bağlantı yoğunluğu |
| 9 | listening_port_count | Dinleyen servis sayısı (SSH dahil) |
| 10 | bytes_received | Deneme sırasında gelen bayt |
| 11 | bytes_sent | Deneme sırasında giden bayt |
| 12 | packets_received | Gelen paket artışı |
| 13 | packets_sent | Giden paket artışı |
| 14 | incoming_traffic_rate | Trafik oranı anomalisi (B/s) |
| 15 | outgoing_traffic_rate | Trafik oranı anomalisi (B/s) |
| 16 | ping_latency | Hedefe gecikme (ms) |
| 17 | connection_setup_time | SSH deneme süresi (ms) |
| 18 | cpu_utilization | İzleme/deneme sırasında CPU |
| 19 | memory_usage | İzleme sürecinin bellek kullanımı (MB) |
| 20 | failed_login_count | Başarısız giriş sayacı (failed-login) |

Timestamp bu 20’ye dahil değildir; her satırda ayrıca yazılır.

## Ölçüm ve kayıt sırası

1. `get_timestamp()`
2. `collect_interface_metrics()`
3. `collect_connection_metrics()`
4. `collect_system_metrics()`
5. `attempt_ssh_login()`
6. `sleep(INTERVAL)` — döngü tekrarı
7. `export_xlsx()` — turlar bitince

## Fonksiyonlar

1. `get_timestamp` — zaman damgası
2. `collect_interface_metrics` — arayüz + bayt/paket + hız
3. `collect_connection_metrics` — IP/port/protokol/durum/sayaçlar
4. `collect_system_metrics` — CPU, bellek, ping
5. `attempt_ssh_login` — localhost yanlış auth
6. `export_xlsx` — 2 sayfalı Excel
7. `main` — döngü ve hata yönetimi

## Teslim dosyaları

- `ag_izleme.py`
- `requirements.txt`
- `CALISMA_PLANI.md`
- `SWOT.md`
- `BPMN.md`
- `DFD.md`
- `ERD.md`
- `AI_PROMPTS.md`
- Çalışınca üretilir: `ssh_monitor_log.xlsx`
- Excel sayfaları: `ssh_monitor_log` (ölçümler) + `Ozet` (ARTIS/AZALIS)

## Platform notları

- Windows 11: `pip install -r requirements.txt` sonra `python ag_izleme.py`
- Ubuntu / Pardus: `pip3 install -r requirements.txt` sonra `python3 ag_izleme.py`
- OpenSSH kurulumu gerekmez; program `lab_auth/` oluşturur ve 2222 portunu dinler
- Ping: Windows’ta `-n`, Linux’ta `-c` kullanılır

## Teslim öncesi checklist (ödev maddeleri)

1. [x] Zaman damgası hariç 20 değişken kodda ve XLSX’te var mı? (21 kolon)
2. [x] Program ağ izleme hedeflerini (SSH failed-login / tekrarlı bağlantı) karşılıyor mu?
3. [x] Kod mantıksal düzen içinde mi ve ~200–250 satır sınırında mı (yorum hariç)?
4. [x] Yorumlar kısa, Türkçe ve bilgilendirici mi?
5. [x] Sözdizimi doğru mu; Windows’ta çalıştırıldı (Linux notları yukarıda)?

## Sınav cevap omurgası

**Promptlar:** `AI_PROMPTS.md` ve `ag_izleme.py` sonundaki blok.

**Neden bu değişkenler?** Failed-login ve tekrarlı SSH denemelerinde bağlantı sayısı, trafik hızı, kurulum süresi, CPU/bellek ve `failed_login_count` yükselir veya durum değişir.

**Toplama sırası:** timestamp → arayüz/trafik → bağlantı → sistem → SSH denemesi → XLSX.

**Kayıt yöntemi:** `openpyxl` ile `ssh_monitor_log.xlsx` (Sayfa1 ölçüm, Sayfa2 özet).

**Bileşenlerin birlikte çalışması:** `main` döngüsü metrikleri toplar, SSH denemesini tetikler, birleşik satırı kaydeder.

**SWOT / BPMN / DFD / ERD:** ilgili `.md` dosyalarında.
