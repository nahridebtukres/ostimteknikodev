# -*- coding: utf-8 -*-
# Ag Izleme Odev 1 — tek dosya, GUI yok | Win11/Ubuntu/Pardus Python 3.15
# Kullanim: python3 ag_izleme.py --run | --monitor
# Ataklar: Failed-login | Repeated connection | Unauthorized-access
import argparse, csv, os, platform, socket, subprocess, sys, threading, time
from datetime import datetime
# requirements.txt yok; eksik paket kod icinde kurulur
DEPS = (("psutil", "psutil"), ("paramiko", "paramiko"))
def ensure_deps():
    # Eksik psutil/paramiko -> pip install
    need = []
    for mod, pip_name in DEPS:
        try: __import__(mod)
        except ImportError: need.append(pip_name)
    if need:
        print("Eksik paketler kuruluyor:", ", ".join(need))
        subprocess.check_call([sys.executable, "-m", "pip", "install", *need])
ensure_deps()
import paramiko, psutil
# Lab SSH — sistem OpenSSH'a dokunulmaz
SSH_HOST, SSH_PORT, SSH_USER = "127.0.0.1", 2222, "labuser"
SSH_LAB_PASSWORD, SSH_WRONG_PASSWORD = "LabPass2222", "wrong_password_lab"
LAB_DIR, CSV_FILE = "lab_auth", "ssh_monitor_log.csv"
STATUS_FILE = os.path.join(LAB_DIR, "attack_status.txt")
INTERVAL, MAX_ROUNDS, SSH_TIMEOUT = 2, 10, 3
prev_bytes_recv = prev_bytes_sent = 0
prev_sample_time, failed_login_total = 0.0, 0
# timestamp + 20 izleme degiskeni
HEADERS = [
    "timestamp", "interface_name", "local_ip", "remote_ip", "remote_port", "local_port",
    "transport_protocol", "connection_state", "active_connection_count", "listening_port_count",
    "bytes_received", "bytes_sent", "packets_received", "packets_sent",
    "incoming_traffic_rate", "outgoing_traffic_rate", "ping_latency", "connection_setup_time",
    "cpu_utilization", "memory_usage", "failed_login_count"]
def write_attack_status(fail, state, setup):
    # --run yazar; --monitor okur (yan yana demo)
    os.makedirs(LAB_DIR, exist_ok=True)
    open(STATUS_FILE, "w", encoding="utf-8").write("{0}|{1}|{2}\n".format(fail, state, setup))
def read_attack_status():
    # Paylasilan atak durumu; yoksa 0/NONE
    try:
        p = open(STATUS_FILE, encoding="utf-8").read().strip().split("|")
        return int(p[0]), p[1], float(p[2])
    except (OSError, ValueError, IndexError):
        return 0, "NONE", 0.0
def ensure_csv(path=CSV_FILE):
    # CSV yoksa baslik satiriyla olustur
    if os.path.isfile(path): return
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS).writeheader()
    print("CSV olusturuldu:", path)
def export_csv(rows, path=CSV_FILE):
    # Olcum satirlarini CSV'ye yaz
    ensure_csv(path)
    if not rows: return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS); w.writeheader()
        for row in rows: w.writerow({k: row.get(k, "") for k in HEADERS})
def collect_interface_metrics():
    # Arayuz, local IP, bayt/paket, B/s hiz
    global prev_bytes_recv, prev_bytes_sent, prev_sample_time
    interface_name, local_ip = "unknown", "127.0.0.1"
    stats, addrs = psutil.net_if_stats(), psutil.net_if_addrs()
    ordered = [n for n, st in stats.items() if st.isup and not n.lower().startswith("lo")] + list(addrs)
    for name in ordered:
        for addr in addrs.get(name, []):
            if addr.family == socket.AF_INET:
                interface_name, local_ip = name, addr.address; break
        if interface_name != "unknown": break
    io_all = psutil.net_io_counters()
    br, bs = int(io_all.bytes_recv), int(io_all.bytes_sent)
    pr, ps = int(io_all.packets_recv), int(io_all.packets_sent)
    now = time.time()
    dt = now - prev_sample_time if prev_sample_time > 0 else 0
    if dt > 0:
        in_r = max(0.0, (br - prev_bytes_recv) / dt)
        out_r = max(0.0, (bs - prev_bytes_sent) / dt)
    else: in_r, out_r = 0.0, 0.0
    prev_bytes_recv, prev_bytes_sent, prev_sample_time = br, bs, now
    return {"interface_name": interface_name, "local_ip": local_ip,
            "bytes_received": br, "bytes_sent": bs, "packets_received": pr, "packets_sent": ps,
            "incoming_traffic_rate": round(in_r, 2), "outgoing_traffic_rate": round(out_r, 2)}
def collect_connection_metrics():
    # SSH hedefi, local_port, protokol, state, aktif/LISTEN
    local_port, proto, state = 0, "TCP", "NONE"
    active_n, listen_n = 0, 0
    try: conns = psutil.net_connections(kind="inet")
    except (psutil.AccessDenied, PermissionError): conns = []
    for c in conns:
        if c.status == "LISTEN": listen_n += 1
        if c.status in ("ESTABLISHED", "SYN_SENT", "SYN_RECV", "TIME_WAIT"): active_n += 1
        if not c.raddr or c.raddr.port != SSH_PORT: continue
        if c.raddr.ip not in (SSH_HOST, "127.0.0.1", "::1"): continue
        local_port = c.laddr.port if c.laddr else 0
        state = c.status
        proto = "UDP" if c.type == socket.SOCK_DGRAM else "TCP"
    return {"remote_ip": SSH_HOST, "remote_port": SSH_PORT, "local_port": local_port,
            "transport_protocol": proto, "connection_state": state,
            "active_connection_count": active_n, "listening_port_count": listen_n}
def collect_system_metrics():
    # CPU %, bellek MB, ping ms (Win/Linux bayrak ayri)
    cpu = float(psutil.cpu_percent(interval=0.2))
    mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)
    win = platform.system().lower() == "windows"
    cmd = (["ping", "-n", "1", "-w", "1000", SSH_HOST] if win else ["ping", "-c", "1", "-W", "1", SSH_HOST])
    ping = -1.0
    try:
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if proc.returncode == 0:
            out = ((proc.stdout or "") + (proc.stderr or "")).lower()
            ping = round((time.time() - t0) * 1000.0, 2)
            if "time=" in out:
                tok = "".join(ch if ch.isdigit() or ch == "." else " " for ch in out.split("time=")[-1])
                ping = float(tok.split()[0])
    except Exception: ping = -1.0
    return {"cpu_utilization": cpu, "memory_usage": mem, "ping_latency": ping}
class LabSSH(paramiko.ServerInterface):
    # Lab parola; yanlis sifre -> AUTH_FAILED
    def get_allowed_auths(self, username): return "password"
    def check_auth_password(self, username, password):
        try:
            for line in open(os.path.join(LAB_DIR, "users.txt"), encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line: continue
                user, pwd = line.split(":", 1)
                if username == user and password == pwd: return paramiko.AUTH_SUCCESSFUL
        except OSError: pass
        return paramiko.AUTH_FAILED
    def check_channel_request(self, kind, chanid): return paramiko.OPEN_SUCCEEDED
def start_lab_ssh():
    # 127.0.0.1:2222 lab SSH dinleyici
    os.makedirs(LAB_DIR, exist_ok=True)
    key_p, user_p = os.path.join(LAB_DIR, "host_key"), os.path.join(LAB_DIR, "users.txt")
    if not os.path.isfile(user_p):
        open(user_p, "w", encoding="utf-8").write("labuser:{0}\n".format(SSH_LAB_PASSWORD))
    if os.path.isfile(key_p): key = paramiko.RSAKey(filename=key_p)
    else: key = paramiko.RSAKey.generate(2048); key.write_private_key_file(key_p)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SSH_HOST, SSH_PORT)); sock.listen(8)
    def serve(client):
        tr = None
        try:
            tr = paramiko.Transport(client)
            tr.add_server_key(key); tr.start_server(server=LabSSH())
            end = time.time() + SSH_TIMEOUT
            while time.time() < end and tr.is_active(): time.sleep(0.05)
        except Exception: pass
        finally:
            if tr is not None: tr.close()
            client.close()
    def loop():
        while True:
            client, _ = sock.accept()
            threading.Thread(target=serve, args=(client,), daemon=True).start()
    threading.Thread(target=loop, daemon=True).start(); time.sleep(0.2)
def attempt_ssh_login():
    # Yanlis sifre denemesi; AUTH_FAILED + kumulatif fail
    global failed_login_total
    setup, state = 0.0, "FAILED"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t0 = time.time()
    try:
        client.connect(
            hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_WRONG_PASSWORD,
            timeout=SSH_TIMEOUT, allow_agent=False, look_for_keys=False,
            banner_timeout=SSH_TIMEOUT, auth_timeout=SSH_TIMEOUT)
        state = "ESTABLISHED"
    except paramiko.AuthenticationException:
        failed_login_total += 1; state = "AUTH_FAILED"
    except (paramiko.SSHException, socket.error, OSError, TimeoutError):
        failed_login_total += 1; state = "CONNECT_FAILED"
    finally:
        setup = round((time.time() - t0) * 1000.0, 2)
        try: client.close()
        except Exception: pass
    write_attack_status(failed_login_total, state, setup)
    return {"connection_setup_time": setup, "failed_login_count": failed_login_total,
            "ssh_connection_state": state}
def build_row(attack=False):
    # Timestamp + 20 degisken; attack ise SSH dene
    row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    row.update(collect_interface_metrics())
    row.update(collect_connection_metrics())
    row.update(collect_system_metrics())
    if attack:
        ssh = attempt_ssh_login()
        row["connection_state"] = ssh["ssh_connection_state"]
        row["connection_setup_time"] = ssh["connection_setup_time"]
        row["failed_login_count"] = ssh["failed_login_count"]
    else:
        fail, state, setup = read_attack_status()  # yan yana --run
        row["failed_login_count"], row["connection_setup_time"] = fail, setup
        if fail > 0: row["connection_state"] = state
    return row
def print_live(row, n):
    # Her ornek yeni olcum; Win cls / Unix clear
    os.system("cls" if os.name == "nt" else "clear")
    print("CANLI IZLEME  Ctrl+C=kaydet  | ornek={0}\n{1}".format(n, "-" * 72))
    tips = [
        "olcum zamani", "trafigin gectigi ag arayuzu", "bu makinenin kaynak IP",
        "hedef SSH IP", "hedef SSH port", "yerel kaynak port", "TCP/UDP protokol",
        "SSH/TCP baglanti durumu", "etkin TCP baglanti sayisi", "dinleyen LISTEN port",
        "toplam alinan bayt", "toplam gonderilen bayt", "toplam alinan paket",
        "toplam gonderilen paket", "gelen trafik hizi B/s", "giden trafik hizi B/s",
        "ping gecikmesi ms", "baglanti kurma suresi ms", "CPU kullanimi yuzde",
        "surec bellek MB", "kumulatif basarisiz giris"]
    for key, tip in zip(HEADERS, tips):
        print("{0:28} {1:<22}  // {2}".format(key, row.get(key, ""), tip))
    sys.stdout.flush()
def mode_run():
    # Atak: lab SSH + turlar + CSV
    ensure_csv(); write_attack_status(0, "NONE", 0.0); start_lab_ssh()
    print("ATAK MODU | {0}:{1} | tur={2} | csv={3}".format(SSH_HOST, SSH_PORT, MAX_ROUNDS, CSV_FILE))
    collected = []
    for n in range(1, MAX_ROUNDS + 1):
        try:
            row = build_row(attack=True); collected.append(row)
            print("[{0}] tur={1} state={2} fail={3}".format(
                row["timestamp"], n, row["connection_state"], row["failed_login_count"]))
        except Exception as exc:
            print("Tur {0} hata: {1}".format(n, exc))
        if n < MAX_ROUNDS: time.sleep(INTERVAL)
    export_csv(collected); print("Tamamlandi | {0}".format(CSV_FILE))
def mode_monitor():
    # Canli izleme; Ctrl+C -> CSV (--run yanindaysa fail dosyadan okunur)
    ensure_csv()
    print("MONITOR | {0}sn | yan yana --run -> fail artar | Ctrl+C=CSV".format(INTERVAL))
    collected, n = [], 0
    try:
        while True:
            n += 1; row = build_row(attack=False); collected.append(row)
            print_live(row, n); time.sleep(INTERVAL)
    except KeyboardInterrupt:
        export_csv(collected)
        print("\nKaydedildi | {0} | ornek={1}".format(CSV_FILE, len(collected)))
def main():
    # CLI: --run atak, --monitor canli
    ap = argparse.ArgumentParser(description="SSH localhost ag izleme")
    ap.add_argument("--run", "--runn", action="store_true", help="Failed-login atak + olcum + CSV")
    ap.add_argument("--monitor", action="store_true", help="Canli terminal izleme + cikisda CSV")
    args = ap.parse_args()
    if args.run == args.monitor:
        ap.print_help(); print("\nOrnek: python3 ag_izleme.py --run | --monitor"); sys.exit(1)
    mode_run() if args.run else mode_monitor()

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Yapay Zeka Prompt Arsivi (asama asama — tek istekte tum program istenmedi)
# Amac: Hangi prompt ile hangi parcayi urettigimizi belgelemek.
# Yorum satirlari 200-250 kod siniri DISINDADIR.
# Secilen ataklar: Failed-login | Repeated connection attempts |
#                  Unauthorized-access attempt (localhost SSH lab, port 2222)
# ---------------------------------------------------------------------------
#
# === Prompt-1 (AI-1) — Degisken secimi ===
# "Ag Izleme odevi icin Python programi yazacagim. Maildeki atak listesinden
#  Failed-login simulation, Repeated connection attempts ve Unauthorized-access
#  attempt simulation sececegim. Lab ortaminda 127.0.0.1 uzerinde SSH ile
#  yanlis parola denemesi yapilacak. Timestamp HARIC tam 20 ag/sistem degiskeni
#  sec. Her degiskeni ders listesindeki gruplarla (arayuz, baglanti, trafik,
#  zaman) eslestir ve hangi atak izini (AUTH_FAILED, tekrarli TCP, erisim
#  reddi, bayt/paket artisi) gosterebilecegini tek tek yaz. Kod yazma."
# Sonuc (AI-1): interface_name, local_ip, remote_ip, remote_port, local_port,
#   transport_protocol, connection_state, active_connection_count,
#   listening_port_count, bytes_received, bytes_sent, packets_received,
#   packets_sent, incoming_traffic_rate, outgoing_traffic_rate, ping_latency,
#   connection_setup_time, cpu_utilization, memory_usage, failed_login_count.
#
# === Prompt-2 (AI-2, baska oturum) — Degisken dogrulama ===
# "Asagidaki 20 degiskenle Failed-login, Repeated connection ve
#  Unauthorized-access ataklarini izleyebilir miyim? Eksik varsa oner,
#  yeterliyse neden yeterli oldugunu kisa yaz. Kod yazma.
#  Liste: [Prompt-1 sonucu]."
# Sonuc (AI-2): Yeterli. failed_login_count + connection_state AUTH_FAILED
#   failed/unauthorized izini; active_connection_count + traffic rate +
#   connection_setup_time tekrarli denemeyi; remote_ip/port hedefi baglar.
#
# === Prompt-3 (AI-1) — Fonksiyon bolumu ===
# "Tek bir Python dosyasinda, GUI olmadan, yorum haric yaklasik 200-250 satir
#  ag izleme kodu yazacagim. Veri toplama, lab SSH, CSV kayit, --run atak
#  ve --monitor canli izleme olacak. Bunlari kac ayri fonksiyonda yapmaliyim?
#  Fonksiyon adlarini ve her birinin tek gorevini listele. Kod yazma."
# Sonuc (AI-1): ensure_deps, ensure_csv, export_csv, collect_interface_metrics,
#   collect_connection_metrics, collect_system_metrics, LabSSH + start_lab_ssh,
#   attempt_ssh_login, build_row, print_live, mode_run, mode_monitor, main.
#
# === Prompt-4 (AI-2) — Fonksiyon listesi uygun mu? ===
# "Su fonksiyon plani odev icin uygun mu? Eksik/fazla var mi? Tek dosya,
#  20 degisken, CSV, lab SSH failed-login. [Prompt-3 listesi]. Kod yazma."
# Sonuc (AI-2): Uygun; arayuz/baglanti/sistem ayri, atak ayri, CLI ayri.
#
# === Prompt-5 — Arayuz / trafik toplama ===
# "Sadece collect_interface_metrics yaz: psutil ile secili ag arayuzu adi,
#  local IPv4, bytes/packets recv-sent, onceki ornekle B/s incoming/outgoing
#  rate hesapla. Dict dondur. Windows ve Linux'ta calissin."
#
# === Prompt-6 — Baglanti metrikleri ===
# "Sadece collect_connection_metrics yaz: psutil.net_connections ile
#  remote_ip=127.0.0.1 remote_port=2222 eslesen baglantinin local_port,
#  transport_protocol, connection_state; ayrica active_connection_count ve
#  listening_port_count. AccessDenied olursa bos liste kabul et."
#
# === Prompt-7 — Sistem / ping ===
# "Sadece collect_system_metrics yaz: cpu_percent, surec memory MB,
#  ping_latency. Windows'ta ping -n 1 -w 1000, Linux/Pardus'ta ping -c 1 -W 1.
#  Basarisizsa -1.0 don."
#
# === Prompt-8 — Lab SSH + failed-login denemesi ===
# "Paramiko ile sadece lab SSH parcasi yaz: LabSSH (ServerInterface) users.txt
#  dogru parola ise AUTH_SUCCESSFUL degilse AUTH_FAILED; start_lab_ssh
#  127.0.0.1:2222 dinlesin (sistem OpenSSH'a dokunma); attempt_ssh_login
#  bilerek yanlis parola gondersin, connection_setup_time (ms) ve kumulatif
#  failed_login_count + ssh_connection_state dondursun."
#
# === Prompt-9 — Satir birlestirme + CSV + --run ===
# "build_row(timestamp + 20 degisken, attack=True ise SSH denemesi),
#  ensure_csv/export_csv (stdlib csv, ssh_monitor_log.csv), mode_run:
#  10 tur, 2 sn aralik, her turda atak+olcum, bitince CSV yaz. requirements.txt
#  kullanma; eksik psutil/paramiko icin ensure_deps pip ile kursun."
#
# === Prompt-10 — Canli izleme + CLI ===
# "mode_monitor: surekli build_row(attack=False), print_live ile HEADERS'taki
#  tum degiskenleri 'deger // anlam' formatinda bas; Win'de cls, Unix'te clear.
#  Ctrl+C'de CSV kaydet. main: argparse --run/--monitor. Python 3.15 Win/Linux."
#
# === Prompt-11 — Yan yana demo (paylasilan fail) ===
# "Iki ayri surec: --run atak yapsin, --monitor atak yapmasin ama ayni anda
#  acikken failed_login_count artsin. lab_auth/attack_status.txt dosyasina
#  fail|state|setup yazan write_attack_status ve okuyan read_attack_status ekle.
#  attempt_ssh_login yazsin; build_row(attack=False) okusun."
#
# === Prompt-12 (AI-2) — Birlesik kontrol ===
# "20 degisken CSV'de mi? Yorum haric ~250 satir mi? Yan yana --run/--monitor
#  fail paylasimi var mi? Canli panelde 21 alan (timestamp+20) basiliyor mu?"
# Sonuc: Uyumlu; status dosyasi + canli panel tamam.
#
# Not: Her promptta yalnizca bir parca istendi; tam program tek mesajda
# uretilmedi. Yukaridaki sonuclar bu dosyadaki fonksiyonlara isledi.
