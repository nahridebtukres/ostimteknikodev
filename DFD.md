# DFD — Ağ İzleme Ödev 1

## Seviye 0 (bağlam)

```mermaid
flowchart LR
    userActor[Kullanici_Terminal] --> processMain[ag_izleme.py]
    osNet[Isletim_Sistemi_psutil_ping] --> processMain
    sshSvc[LabSSH_127_0_0_1_2222] --> processMain
    pipNet[Pip_psutil_paramiko] --> processMain
    processMain --> csvStore[(ssh_monitor_log.csv)]
    processMain --> statusStore[(lab_auth_attack_status.txt)]
    statusStore --> processMain
    processMain --> userActor
```

- Kullanıcı `python3 ag_izleme.py --run` veya `--monitor` ile başlatır.
- İlk çalıştırmada eksik paketler pip ile kurulur (`requirements.txt` yok).
- CSV yoksa program başlık satırıyla oluşturur.
- Program OS’tan arayüz, bağlantı, CPU, bellek, ping alır.
- `--run` lab SSH’a yanlış kimlik gönderir; `AUTH_FAILED` döner ve `lab_auth/attack_status.txt` güncellenir.
- `--monitor` atak yapmaz; yan yana `--run` varsa status dosyasından `failed_login_count` / state okur.
- Sonuç `ssh_monitor_log.csv` dosyasına yazılır; monitor’da canlı terminal + `//` açıklama vardır (21 alan: timestamp + 20 değişken).

## Seviye 1 (süreçler)

```mermaid
flowchart TD
    userActor[Kullanici] -->|run_veya_monitor| p0[0_0_CLI]
    p0 --> p6[6_0_Deps_ve_CSV]
    pipNet[Pip] --> p6
    p6 --> p1[1_0_Dongu]
    p1 --> p2[2_0_Metrik_Toplama]
    osNet[OS] --> p2
    p2 -->|run| p3[3_0_SSH_Failed_Login]
    sshSvc[LabSSH_2222] --> p3
    p3 --> p7[7_0_Status_Yaz]
    p7 --> statusStore[(attack_status.txt)]
    p7 --> p1
    p2 -->|monitor| p8[8_0_Status_Oku]
    statusStore --> p8
    p8 --> p5[5_0_Canli_Ekran]
    p5 --> p1
    p1 -->|bitti_veya_CtrlC| p4[4_0_CSV_Kayit]
    p2 --> p4
    p3 --> p4
    p4 --> csvStore[(ssh_monitor_log.csv)]
    p4 --> userActor
    p5 --> userActor
```

| No | Süreç | Girdi | Çıktı |
|----|--------|--------|--------|
| 0.0 | CLI | `--run` / `--monitor` | mod seçimi |
| 6.0 | Deps + CSV | eksik paket / dosya yok | kurulu paket, başlıklı CSV |
| 1.0 | Döngü | tur / Ctrl+C | ölçüm tetikleri |
| 2.0 | Metrik toplama | OS sayaçları | 20 değişken |
| 3.0 | SSH denemesi | yanlış şifre | state, setup_time, fail |
| 7.0 | Status yaz | fail, state, setup | `attack_status.txt` |
| 8.0 | Status oku | `attack_status.txt` | fail/state (monitor) |
| 4.0 | CSV kayıt | satırlar | `ssh_monitor_log.csv` |
| 5.0 | Canlı ekran | satır | terminal paneli + `//` not |
