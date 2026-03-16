# utils.py
import datetime
from scapy.all import ARP, sniff

# =========================
# Configuration
# =========================

SCAN_INTERVAL = 5

# =========================
# Logging System
# =========================

def log_event(message):
    with open("ids_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} : {message}\n")


# =========================
# Alert System
# =========================

def alert_attack(ip):
    print(f"[ALERT] Possible ARP spoofing detected from {ip}")
    log_event(f"ARP spoofing detected from {ip}")


# =========================
# Packet Analysis
# =========================

def analyze_packet(packet):
    if packet.haslayer(ARP):
        print("ARP packet detected")
        log_event("ARP packet captured")


# =========================
# Detection Logic
# =========================

def detect_spoof(packet):
    if packet.haslayer(ARP):
        ip = packet.psrc
        mac = packet.hwsrc
        print(f"Checking packet from {ip} ({mac})")


# =========================
# Packet Sniffer
# =========================

def start_sniffing():
    print("Starting IDS monitoring...")
    sniff(filter="arp", prn=analyze_packet)