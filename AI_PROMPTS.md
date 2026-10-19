# Yapay Zeka Prompt Arşivi — Ağ İzleme Ödev 1

Ödev kuralı: program tek istekte üretilmez. Aşağıdaki promptlar aşamalı kullanılmıştır.  
Vize teslimi gereği yapay zeka kaynaklı kod parçaları ve promptlar saklanır.

## Prompt-1 — Değişken seçimi (AI-1)

```
Failed-login simulation ve Repeated connection attempts ataklarını localhost
SSH üzerinde izlemek için ders listesinden timestamp hariç tam 20 ağ/sistem
değişkeni öner. Her değişkenin atağı nasıl açıkladığını kısa yaz.
```

Sonuç: `interface_name`, `local_ip`, `remote_ip`, `remote_port`, `local_port`,
`transport_protocol`, `connection_state`, `active_connection_count`,
`listening_port_count`, `bytes_received`, `bytes_sent`, `packets_received`,
`packets_sent`, `incoming_traffic_rate`, `outgoing_traffic_rate`, `ping_latency`,
`connection_setup_time`, `cpu_utilization`, `memory_usage`, `failed_login_count`.

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

Sonuç: set yeterli. `failed_login_count` ve `connection_state` auth reddini;
bağlantı sayısı ve trafik hızları tekrarlı denemeyi gösterir.

## Prompt-3 — Fonksiyon sayısı (AI-1)

```
Tek Python dosyasında, 200-250 satır kod sınırıyla localhost SSH failed-login
izleme programını kaç ayrı fonksiyonda yazmalıyım? Görevleri listele.
```

Sonuç: timestamp, arayüz, bağlantı, sistem, lab SSH, giriş denemesi, XLSX, main.

## Prompt-4 — Fonksiyon uygunluğu (AI-2)

```
Şu fonksiyonlar uygun mu: get_timestamp, collect_interface_metrics,
collect_connection_metrics, collect_system_metrics, start_lab_ssh,
attempt_ssh_login, export_xlsx, main? Eksik/fazla varsa söyle.
```

Sonuç: uygun. `LabSSH` sınıfı lab kimlik doğrulaması içindir.

## Prompt-5 — Parça kod (arayüz)

```
Sadece collect_interface_metrics yaz: psutil ile arayüz adı, local IP,
bytes/packets ve önceki örneğe göre trafik hızı döndür.
```

## Prompt-6 — Parça kod (bağlantı)

```
Sadece collect_connection_metrics yaz: remote_ip/port, local_port, TCP,
connection_state, active_connection_count, listening_port_count.
Hedef port 2222 olsun.
```

## Prompt-7 — Parça kod (sistem)

```
Sadece collect_system_metrics yaz: CPU %, süreç bellek MB, localhost ping ms.
Windows ve Linux ping bayraklarını ayır.
```

## Prompt-8 — Parça kod (SSH denemesi)

```
Sadece attempt_ssh_login yaz: paramiko ile 127.0.0.1:2222 yanlış şifre,
connection_setup_time ve failed_login_count döndür; servis yoksa çökmesin.
```

## Prompt-9 — Parça kod (kayıt ve main)

```
export_xlsx ve main yaz: 21 kolonlu XLSX, 2 sayfa (olcum + ozet),
10 tur, 2 saniye aralık, terminal özet. GUI yok.
```
