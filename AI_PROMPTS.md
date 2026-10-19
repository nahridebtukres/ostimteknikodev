# Yapay Zeka Prompt Arşivi

Ödev kuralı gereği program tek seferde istenmemiştir. Aşağıdaki promptlar aşamalı kullanılmıştır. Aynı metinler `ag_izleme.py` dosyasının sonunda da yer alır.

## Prompt-1 — Değişken seçimi (AI-1)

```
Failed-login simulation ve Repeated connection attempts ataklarını localhost
SSH üzerinde izlemek için ders listesinden timestamp hariç tam 20 ağ/sistem
değişkeni öner. Her değişkenin atağı nasıl açıkladığını kısa yaz.
```

**Özet sonuç:** interface_name, local_ip, remote_ip, remote_port, local_port,
transport_protocol, connection_state, active_connection_count,
listening_port_count, bytes_received, bytes_sent, packets_received,
packets_sent, incoming_traffic_rate, outgoing_traffic_rate, ping_latency,
connection_setup_time, cpu_utilization, memory_usage, failed_login_count.

## Prompt-2 — Değişken doğrulama (AI-2)

```
Şu 20 değişken failed-login ve tekrarlı SSH bağlantı denemelerini takip etmek
için yeterli mi? Eksik veya gereksiz varsa gerekçeli söyle:
interface_name, local_ip, remote_ip, remote_port, local_port,
transport_protocol, connection_state, active_connection_count,
listening_port_count, bytes_received, bytes_sent, packets_received,
packets_sent, incoming_traffic_rate, outgoing_traffic_rate, ping_latency,
connection_setup_time, cpu_utilization, memory_usage, failed_login_count
```

**Özet sonuç:** Set yeterli; failed_login_count ve connection_setup_time saldırı
izini doğrudan taşır; trafik ve bağlantı sayaçları tekrarlı denemeleri gösterir.

## Prompt-3 — Fonksiyon sayısı (AI-1)

```
Tek Python dosyasında, 200-250 satır kod sınırıyla localhost SSH failed-login
izleme programını kaç ayrı fonksiyonda yazmalıyım? Görevleri listele.
```

**Özet sonuç:** 7 ana fonksiyon önerildi (timestamp, arayüz, bağlantı, sistem,
SSH denemesi, Excel export, main).

## Prompt-4 — Fonksiyon uygunluğu (AI-2)

```
Şu 7 fonksiyon uygun mu: get_timestamp, collect_interface_metrics,
collect_connection_metrics, collect_system_metrics, attempt_ssh_login,
export_xlsx, main? Eksik/fazla varsa söyle.
```

**Özet sonuç:** Uygun; küçük yardımcı fonksiyonlar satır bütçesi içinde kabul edilebilir.

## Prompt-5 — Parça kod (arayüz metrikleri)

```
Sadece collect_interface_metrics yaz: psutil ile arayüz adı, local IP,
bytes/packets ve önceki örneğe göre trafik hızı döndür.
```

## Prompt-6 — Parça kod (bağlantı metrikleri)

```
Sadece collect_connection_metrics yaz: remote_ip/port, local_port, TCP,
connection_state, active_connection_count, listening_port_count.
```

## Prompt-7 — Parça kod (sistem metrikleri)

```
Sadece collect_system_metrics yaz: CPU %, süreç bellek MB, localhost ping ms.
Windows ve Linux ping bayraklarını ayır.
```

## Prompt-8 — Parça kod (SSH denemesi)

```
Sadece attempt_ssh_login yaz: paramiko ile 127.0.0.1:2222 yanlış şifre,
connection_setup_time ve failed_login_count döndür; servis yoksa çökmesin.
```

## Prompt-9 — Parça kod (Excel ve main)

```
export_xlsx ve main yaz: 21 kolonlu XLSX, 2 sayfa (olcum+ozet), 10 tur, terminal ozet.
```
