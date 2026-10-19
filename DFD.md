# DFD — Veri Akış Diyagramı

## Seviye 0 (Bağlam)

```mermaid
flowchart LR
    userActor[Kullanici_Terminal] --> processMain[Ag_Izleme_Programi]
    osNet[Isletim_Sistemi_Ag_API] --> processMain
    sshSvc[Localhost_SSH_Servisi] --> processMain
    processMain --> xlsxStore[(ssh_monitor_log.xlsx)]
    processMain --> userActor
```

- Kullanıcı programı başlatır ve terminal özetini görür.
- Program işletim sisteminden ağ/sistem metriklerini alır.
- Program localhost SSH’a giriş denemesi gönderir / yanıt alır.
- Sonuçlar XLSX veri deposuna yazılır (2 sayfa).

## Seviye 1 (Süreçler)

```mermaid
flowchart TD
    userActor[Kullanici] -->|baslat| p1[1_0_Dongu_Yonetimi]
    p1 --> p2[2_0_Metrik_Toplama]
    osNet[OS_psutil_ping] --> p2
    p2 --> p3[3_0_SSH_Denemesi]
    sshSvc[SSH_22] --> p3
    p3 --> p4[4_0_XLSX_Kayit]
    p2 --> p4
    p4 --> xlsxStore[(XLSX)]
    p4 --> userActor
```

### Süreç açıklamaları

| No | Süreç | Girdi | Çıktı |
|----|-------|-------|-------|
| 1.0 | Döngü yönetimi | Tur sayısı, aralık | Ölçüm tetikleri |
| 2.0 | Metrik toplama | OS sayaçları | 19 değişken (+ssh sonrası 20.) |
| 3.0 | SSH denemesi | host/user/yanlış şifre | setup_time, failed_login, state |
| 4.0 | XLSX kayıt | Birleşik satırlar | Ölçüm + Özet sayfaları |

## Veri akışları (kısa)

1. OS → Metrik toplama: bytes, packets, connections, CPU, memory, ping
2. SSH servisi → SSH denemesi: auth/connect sonucu
3. Metrik + SSH sonucu → XLSX: timestamp + 20 değişken + özet
4. Program → Kullanıcı: tur özeti (state, fail, cpu, rate)
