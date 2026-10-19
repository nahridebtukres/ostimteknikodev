# Çalışma Planı — Ağ İzleme Ödev 1

Ders: Ağ İzleme  
Ödev: Python Tabanlı Ağ İzleme  
Öğrenci: 250401041 — Bedirhan Serkut Yöntem  
Program: `ag_izleme.py` (tek dosya, terminal)

## Amaç

Program, proje içi lab SSH hedefine (`127.0.0.1:2222`) bilinçli yanlış şifre ile bağlanmayı dener. Bu sırada timestamp hariç 20 ağ/sistem değişkenini toplar ve sonucu `ssh_monitor_log.xlsx` dosyasına kaydeder.

İzlenen saldırı izleri (ödev mailindeki atak listesi):

- Failed-login simulation
- Repeated connection attempts
- Unauthorized-access attempt (auth reddi)

Sistem OpenSSH ayarına dokunulmaz. Lab sunucusu programla birlikte `lab_auth/` dizininde ayağa kalkar.

## Kilitlelen kararlar

| Konu | Karar |
|------|--------|
| Dil / arayüz | Python, GUI yok, terminal |
| Hedef | `127.0.0.1:2222` |
| Kimlik | kullanıcı `labuser`, istemci şifresi kasıtlı yanlış |
| Beklenen durum | `AUTH_FAILED` |
| Kayıt | `ssh_monitor_log.xlsx` (Sayfa1: ölçüm, Sayfa2: özet) |
| Kod uzunluğu | ~200–250 satır (yorum hariç) |
| Prompt arşivi | `AI_PROMPTS.md` |
| Platform | Windows 11, Ubuntu, Pardus |

## 20 değişken (timestamp hariç)

Timestamp her satırda ayrıca tutulur; aşağıdaki 20 değişken atak izini açıklamak için seçilmiştir.

| # | Değişken | Neden seçildi |
|---|----------|----------------|
| 1 | interface_name | Trafiğin geçtiği arayüz |
| 2 | local_ip | Denemelerin kaynak IP’si |
| 3 | remote_ip | SSH hedefi (127.0.0.1) |
| 4 | remote_port | Hedef port (2222) |
| 5 | local_port | İstemci geçici portu |
| 6 | transport_protocol | SSH taşıması (TCP) |
| 7 | connection_state | AUTH_FAILED / CONNECT_FAILED |
| 8 | active_connection_count | Tekrarlı TCP yoğunluğu |
| 9 | listening_port_count | Dinleyen servis sayısı |
| 10 | bytes_received | Gelen bayt |
| 11 | bytes_sent | Giden bayt |
| 12 | packets_received | Gelen paket |
| 13 | packets_sent | Giden paket |
| 14 | incoming_traffic_rate | Gelen hız (B/s) |
| 15 | outgoing_traffic_rate | Giden hız (B/s) |
| 16 | ping_latency | Hedefe gecikme (ms) |
| 17 | connection_setup_time | SSH deneme süresi (ms) |
| 18 | cpu_utilization | CPU (%) |
| 19 | memory_usage | İzleme süreci belleği (MB) |
| 20 | failed_login_count | Kümülatif başarısız giriş |

## Toplama ve kayıt sırası

1. `get_timestamp()`
2. `collect_interface_metrics()`
3. `collect_connection_metrics()`
4. `collect_system_metrics()`
5. `attempt_ssh_login()`
6. Tur kaldıysa `sleep(INTERVAL)`
7. Turlar bitince `export_xlsx()`

## Fonksiyonlar

| Fonksiyon | Görev |
|-----------|--------|
| `get_timestamp` | Zaman damgası |
| `collect_interface_metrics` | Arayüz, bayt/paket, trafik hızı |
| `collect_connection_metrics` | IP/port/protokol/durum/sayaçlar |
| `collect_system_metrics` | CPU, bellek, ping |
| `start_lab_ssh` | Proje içi 2222 lab SSH |
| `attempt_ssh_login` | Yanlış şifre denemesi |
| `export_xlsx` | Ölçüm + özet sayfaları |
| `main` | Döngü ve hata yönetimi |

`LabSSH` sınıfı lab sunucusunun kimlik doğrulamasını yapar; 20 izleme değişkenine dahil değildir.

## Teslim dosyaları

- `ag_izleme.py`
- `requirements.txt` (`psutil`, `paramiko`, `openpyxl`)
- `CALISMA_PLANI.md`, `AI_PROMPTS.md`
- `SWOT.md`, `BPMN.md`, `DFD.md`, `ERD.md`
- Çalışınca üretilir: `ssh_monitor_log.xlsx`
- Çalışınca oluşur (teslimde gizlenebilir): `lab_auth/`

## Çalıştırma

Windows 11:

```text
pip install -r requirements.txt
python ag_izleme.py
```

Ubuntu / Pardus:

```text
pip3 install -r requirements.txt
python3 ag_izleme.py
```

Excel dosyası açıksa program yazamaz; kapatıp yeniden çalıştırın.

## Teslim checklist

1. Timestamp hariç 20 değişken kodda ve XLSX’te var mı?
2. Program failed-login / tekrarlı bağlantı izini topluyor mu?
3. Kod tek dosyada mı ve ~200–250 satır sınırında mı?
4. Promptlar aşamalı belgelenmiş mi (`AI_PROMPTS.md`)?
5. Program Windows’ta çalışıyor mu; Linux ping bayrağı ayrılmış mı?

## Sınav omurgası

- Değişkenler atak izine göre seçildi; doğrulama Prompt-2 ile yapıldı.
- Sıra: timestamp → arayüz → bağlantı → sistem → SSH → XLSX.
- Kayıt: `openpyxl`, iki sayfa.
- Bileşenler `main` içinde sırayla çalışır; lab SSH sistem servisine ihtiyaç duymaz.
