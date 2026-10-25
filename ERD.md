# ERD — Ağ İzleme Ödev 1

Veritabanı yoktur. Kalıcı depolama `ssh_monitor_log.csv` dosyasıdır (tek tablo / başlıklı satırlar).  
Süreçler arası geçici paylaşım: `lab_auth/attack_status.txt` (`fail|state|setup_ms`).

Dosya yoksa `ensure_csv()` yalnızca başlık satırını yazarak oluşturur; ölçüm bitince `export_csv()` satırları yazar.  
`--run` her SSH denemesinde `write_attack_status()` çağırır; `--monitor` `read_attack_status()` ile aynı değerleri satıra işler.

## Varlık: Measurement

Timestamp + 20 izleme değişkeni. Her program turu / monitor örneği bir satırdır.

| Alan | Tip | Açıklama |
|------|-----|----------|
| timestamp | string | Ölçüm zamanı |
| interface_name | string | Ağ arayüzü |
| local_ip | string | Yerel IP |
| remote_ip | string | 127.0.0.1 |
| remote_port | integer | 2222 |
| local_port | integer | İstemci portu |
| transport_protocol | string | TCP |
| connection_state | string | AUTH_FAILED / TCP durumu / NONE |
| active_connection_count | integer | Etkin bağlantı |
| listening_port_count | integer | Dinleyen port |
| bytes_received | integer | Alınan bayt |
| bytes_sent | integer | Gönderilen bayt |
| packets_received | integer | Alınan paket |
| packets_sent | integer | Gönderilen paket |
| incoming_traffic_rate | float | Gelen B/s |
| outgoing_traffic_rate | float | Giden B/s |
| ping_latency | float | ms |
| connection_setup_time | float | SSH deneme ms (`--run` veya status’tan) |
| cpu_utilization | float | CPU % |
| memory_usage | float | MB |
| failed_login_count | integer | Kümülatif başarısız giriş (`--run` veya status’tan) |

## Varlık: AttackStatus (geçici dosya)

| Alan | Tip | Açıklama |
|------|-----|----------|
| fail | integer | Kümülatif fail |
| state | string | AUTH_FAILED / CONNECT_FAILED / NONE |
| setup_ms | float | Son deneme süresi |

Kalıcı ERD’nin parçası değildir; iki sürecin (`--run` / `--monitor`) aynı anda çalışması için köprüdür.

## İlişki

```text
ProgramCalismasi 1 --- * Measurement
--run 1 --- 1 AttackStatus --- 1 --monitor  (dosya üzerinden)
```

`--run` veya `--monitor` oturumu birden çok Measurement satırı üretir; hepsi aynı CSV şemasına yazılır. XLSX / veritabanı kullanılmaz.
