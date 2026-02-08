import random
import time
import pandas as pd
from datetime import datetime, timedelta

class TrafficGenerator:
    def __init__(self):
        self.protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS']
        self.common_ports = [80, 443, 53, 22, 21, 8080]
        self.internal_ips = [f"192.168.1.{i}" for i in range(2, 255)]
        self.external_ips = [
            "104.21.55.2", "172.67.188.12", "142.250.180.14", "8.8.8.8",
            "1.1.1.1", "45.33.32.156", "185.199.108.153"
        ]

    def generate_packet(self):
        """Generates a single random packet (dictionary)."""
        src = random.choice(self.internal_ips + self.external_ips)
        dst = random.choice(self.internal_ips) if src in self.external_ips else random.choice(self.external_ips)

        protocol = random.choice(self.protocols)
        length = random.randint(64, 1500)
        flags = ""

        if protocol == 'TCP':
            flags = random.choice(['SYN', 'ACK', 'FIN', 'PSH,ACK'])

        return {
            "Timestamp": datetime.now(),
            "Source": src,
            "Destination": dst,
            "Protocol": protocol,
            "Length": length,
            "Flags": flags,
            "Info": f"{protocol} packet from {src} to {dst}"
        }

    def generate_batch(self, count=10):
        """Generates a batch of random packets."""
        return [self.generate_packet() for _ in range(count)]

    def generate_dos_attack(self, target_ip, duration_seconds=5):
        """Simulates a DOS attack (high volume of traffic from one IP)."""
        attacker_ip = random.choice(self.external_ips)
        packets = []
        packet_count = 50 * duration_seconds
        start_time = datetime.now() - timedelta(seconds=duration_seconds)

        # Generate a burst of packets spread over the duration
        for i in range(packet_count):
            packets.append({
                "Timestamp": start_time + timedelta(seconds=i/50),
                "Source": attacker_ip,
                "Destination": target_ip,
                "Protocol": "TCP",
                "Length": 64,
                "Flags": "SYN", # SYN Flood characteristic
                "Info": f"[ALERT] Potential SYN Flood from {attacker_ip}"
            })
        return packets

    def generate_port_scan(self, target_ip):
        """Simulates a Port Scan (sequential ports accessed rapidly)."""
        attacker_ip = random.choice(self.external_ips)
        packets = []
        scanned_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080]
        start_time = datetime.now() - timedelta(seconds=1)

        for i, port in enumerate(scanned_ports):
            packets.append({
                "Timestamp": start_time + timedelta(milliseconds=i*50),
                "Source": attacker_ip,
                "Destination": target_ip,
                "Protocol": "TCP",
                "Length": 64,
                "Flags": "SYN",
                "Info": f"[ALERT] Port Scan detected on port {port} from {attacker_ip}"
            })
        return packets
