# Çalışma Planı — Ağ İzleme Ödev 1 / Vize

**Öğrenci:** Bedirhan Serkut Yöntem — 250401041  
**Program:** `ag_izleme.py` (tek dosya, terminal, GUI yok)

## Seçilen ataklar (mail listesinden)

| Atak | Labda ne yapılıyor | Gözlenen iz |
|------|-------------------|-------------|
| Failed-login simulation | `labuser` + yanlış parola → SSH | `AUTH_FAILED`, `failed_login_count` |
| Repeated connection attempts | 10 tur, 2 sn aralık | tur sayısı, trafik hızı, `active_connection_count` |
| Unauthorized-access attempt | yetkisiz kimlik → reddedilme | `connection_state=AUTH_FAILED` |

## 20 değişken (timestamp hariç) ve nedeni

| # | Değişken | Ders listesi grubu | Atak ilişkisi |
|---|----------|-------------------|---------------|
| 1 | interface_name | A arayüz | Trafiğin geçtiği arayüz |
| 2 | local_ip | C yerel IP | Deneme kaynağı |
| 3 | remote_ip | C uzak IP | Lab SSH hedefi |
| 4 | remote_port | C uzak port | 2222 |
| 5 | local_port | C yerel port | İstemci ephemeral port |
| 6 | transport_protocol | C protokol | SSH → TCP |
| 7 | connection_state | C durum | AUTH_FAILED / TCP state |
| 8 | active_connection_count | C etkin sayı | Tekrarlı deneme yoğunluğu |
| 9 | listening_port_count | C dinleyen | Lab servis görünürlüğü |
| 10 | bytes_received | A/C bayt | Gelen hacim |
| 11 | bytes_sent | A/C bayt | Giden hacim (SSH denemeleri) |
| 12 | packets_received | A paket | Gelen paket |
| 13 | packets_sent | A paket | Giden paket |
| 14 | incoming_traffic_rate | C trafik hızı | Gelen B/s |
| 15 | outgoing_traffic_rate | C trafik hızı | Giden B/s (atak anı) |
| 16 | ping_latency | B ping | Hedefe gecikme |
| 17 | connection_setup_time | B kurulum süresi | SSH deneme süresi (ms) |
| 18 | cpu_utilization | D CPU | İzleme yükü |
| 19 | memory_usage | D bellek | Süreç MB |
| 20 | failed_login_count | atak sayacı | Kümülatif başarısız giriş |

## Modlar

| Mod | Ne yapar | `failed_login_count` |
|-----|----------|----------------------|
| `--run` | Lab SSH açar, 10 tur yanlış parola dener, CSV yazar | Her turda artar (1…10) |
| `--monitor` | Atak yapmaz; 20 değişkeni canlı basar, Ctrl+C → CSV | Yan yana `--run` varsa `lab_auth/attack_status.txt` üzerinden okur ve artar; yalnız monitor’da 0 |

Paylaşılan durum dosyası: `lab_auth/attack_status.txt` (`fail|state|setup_ms`). `--run` yazar, `--monitor` okur.

## Toplama ve kayıt sırası

1. `ensure_deps` → paket  
2. `ensure_csv` → dosya yoksa başlık  
3. `--run`: `write_attack_status(0,…)` sıfırla → `start_lab_ssh`  
4. `timestamp`  
5. `collect_interface_metrics`  
6. `collect_connection_metrics`  
7. `collect_system_metrics`  
8. `--run`: `attempt_ssh_login` → `write_attack_status`  
9. `--monitor`: `read_attack_status` (yan yana atak izi)  
10. Bellekte satır biriktir; `INTERVAL` (2 sn) bekle  
11. `export_csv` → `ssh_monitor_log.csv`

## Saklama yöntemi

- Format: CSV (stdlib `csv`), dosya: `ssh_monitor_log.csv`  
- Yan süreç paylaşımı: `lab_auth/attack_status.txt`  
- Veritabanı yok (ERD’de tek varlık: Measurement)  
- GUI yok; terminal: `--run` / `--monitor`

## Dokümantasyon (derste zorunlu)

| Dosya | İçerik |
|-------|--------|
| `SWOT.md` / `SWOT.docx` | Güçlü / zayıf / fırsat / tehdit |
| `BPMN.md` / `BPMN.docx` | İş süreci |
| `DFD.md` / `DFD.docx` | Veri akışı |
| `ERD.md` / `ERD.docx` | Kayıt şeması |
| `ag_izleme.py` sonu | Aşamalı YZ prompt arşivi |

## Çalıştırma (Win / Ubuntu / Pardus — Python 3.15)

```text
python3 ag_izleme.py --run
python3 ag_izleme.py --monitor
```

Yan yana demo: bir terminalde `--monitor`, diğerinde `--run` — monitor panelinde `failed_login_count` atakla birlikte artar.

## Kod sınırı

Yorum hariç ~200–250 satır. Prompt ve `#` yorumları sınır dışı.
