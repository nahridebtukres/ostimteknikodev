# SWOT Analizi — Ağ İzleme Ödev 1

**Öğrenci:** Bedirhan Serkut Yöntem  
**Numara:** 250401041  
**Sistem:** `ag_izleme.py` — localhost SSH failed-login izleme

## 1. Konu

`ag_izleme.py`, `127.0.0.1:2222` üzerindeki lab SSH sunucusuna yanlış parola ile bağlanmayı dener ve her turda 20 ağ/sistem değişkenini kaydeder. `--run` modu atak + ölçüm yapar; `--monitor` modu aynı değişkenleri terminalde canlı basar. Yan yana çalıştırıldığında `--run` başarısız giriş sayısını `lab_auth/attack_status.txt` dosyasına yazar; `--monitor` bu dosyayı okuyarak panelde `failed_login_count` değerini günceller. Kalıcı sonuç `ssh_monitor_log.csv` dosyasına yazılır. SWOT tablosu bu tasarımın artılarını, eksiğini, açılabilecek yönlerini ve çalışma sırasındaki risklerini listeler.

## S — Güçlü yönler

1. Tek `.py` dosyası; arayüz terminal. GUI yok.
2. `--run` (atak) ve `--monitor` (izleme) ayrı; karışmıyor.
3. 20 değişken failed-login ve tekrarlı denemeye göre seçildi (`connection_state`, `failed_login_count`, trafik hızı vb.).
4. Lab SSH 2222’de proje içinde ayağa kalkıyor; sistem OpenSSH’ına dokunulmuyor.
5. Eksik `psutil`/`paramiko` kod içinde kuruluyor; CSV yoksa oluşturuluyor.
6. `AUTH_FAILED` ve artan `failed_login_count` reddi sayısal olarak gösteriyor.
7. İki terminalde yan yana demoda paylaşılan `attack_status.txt` ile monitor da fail sayacını gösterebiliyor.

## W — Zayıf yönler

1. Kod ~250 satır; grafik/filtre yok.
2. Ölçüm localhost ile sınırlı; dış ağ yok.
3. `net_connections` bazı makinelerde yetki ister; aktif/LISTEN sayacı 0 kalabilir.
4. Tek CSV; ayrı özet sayfası yok.
5. Paylaşılan durum dosyası basit metin; eşzamanlı yazma kilidi yok (ödev ölçeğinde yeterli).

## O — Fırsatlar

1. Aynı iskelet port tarama veya anomali senaryosuna çekilebilir.
2. CSV Excel/LibreOffice’te açılıp derste satır satır bakılabilir.
3. BPMN, DFD, ERD ile birlikte anlatımda kullanılabilir.
4. İki terminalde `--run` + `--monitor` aynı anda koşturulup atak izi canlı gösterilebilir.

## T — Tehditler

1. İnternet yoksa ilk pip kurulumu düşer.
2. 2222 doluysa lab SSH açılamaz.
3. Hedef uzak IP’ye çevrilirse istenmeyen deneme olur; hedef `127.0.0.1` kalmalı.
4. Python/pip farkı paket davranışını değiştirebilir.
5. Yalnız `--monitor` çalışırsa fail 0 kalır (atak yoktur); karışıklık olmaması için yanına `--run` gerekir.

## Kısa yorum

S tarafı ödevdeki üç izi (failed-login, tekrarlı bağlantı, yetkisiz erişim reddi) labda ölçülebilir kılıyor; yan yana demoda status dosyası monitor’a da taşıyor. W tarafı satır limiti ve localhost ile bilinçli daraltma. O tarafı sonraki senaryo veya sunum için açık kapı. T tarafı demo öncesi bakılacak yerler: port 2222, ağ, hedef IP, iki terminalin birlikte açılması. Hedef sabit: `127.0.0.1:2222`.
