# 🔍 Network Device Scanner + Visual Map

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![Scapy](https://img.shields.io/badge/Scapy-2.5-orange)](https://scapy.net)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Cybersecurity Project #3** from "10 Creative Hacking Projects" - Live ARP network scanner with IEEE OUI vendor lookup (30k+ vendors), port scanning, hostname resolution, interactive search/filter dashboard, and **network topology map**.

## 🎯 Features
- **🔍 ARP Network Discovery** - Finds all devices on your LAN (5-20 typical)
- **🏢 IEEE OUI Database** - Auto-downloads 30,000+ vendor lookups
- **🔌 Port Scanning** - Scans common ports (22,80,443,445,3389,8080)
- **🌐 Hostname Resolution** - Reverse DNS for each device
- **📊 Interactive Dashboard** - Live search/filter by IP/MAC/vendor/hostname
- **🗺️ Network Topology Map** - Interactive vis.js graph visualization
- **📈 Professional UI** - Responsive table with hover effects + suspicious device highlighting

## 🖥️ Live Demo
```
http://localhost:5000          # 📊 Dashboard + Search/Filter
http://localhost:5000/map      # 🗺️  Interactive Network Map
```

## 📸 Screenshots
![Dashboard](screenshot-dashboard.png)
![Network Map](screenshot-map.png)

## 🚀 Quick Start

### Prerequisites
- **Windows**: Run VS Code/PowerShell **as Administrator** for ARP scanning
- Python 3.8+

### Installation
```
git clone https://github.com/YOURUSERNAME/network-device-scanner.git
cd network-device-scanner
pip install -r requirements.txt
```

### Run
```
# CHANGE SUBNET in main.py to your network (ex: 192.168.1.0/24)
python main.py
```

**Open: http://localhost:5000**

## 🛠️ Tech Stack
```
Frontend:    Flask + HTML/CSS + vis.js (network graphs)
Backend:     Scapy (ARP scanning) + socket (ports/DNS)
Data:        IEEE OUI JSON (30k+ vendors, auto-cached 24h)
Standards:   Cybersecurity reconnaissance + network mapping
```

## 💡 Use Cases
- **Network Inventory** - Document all devices on corporate/home LAN
- **Security Auditing** - Detect unauthorized/rogue devices
- **Penetration Testing** - Reconnaissance phase tool
- **Portfolio Project** - Demonstrates networking + web dev + cybersecurity skills

## 🔍 Sample Output
```
IP: 192.168.1.10    Hostname: router.local    MAC: AA:BB:CC:DD:EE:FF    Vendor: Cisco    Ports: 80,443
IP: 192.168.1.15    Hostname: laptop.local    MAC: 00:1B:63:XX:XX:XX    Vendor: Apple    Ports: 3389
IP: 192.168.1.100   Hostname: Unknown         MAC: XX:XX:XX:XX:XX:XX    Vendor: Unknown  Ports: None
```

## ⚠️ Requirements & Notes
- **Windows**: Run as Administrator for Scapy ARP scanning
- **Linux/macOS**: `sudo python main.py`
- **Fallback**: Ping scanning works without admin rights (no MAC addresses)
- **Network**: Change `SUBNET = "192.168.1.0/24"` to match your LAN

## 📁 Project Structure
```
network-device-scanner/
├── main.py              # Complete scanner + Flask app
├── requirements.txt     # Dependencies
├── README.md           # This file
├── screenshot-*.png    # Demo images
└── oui_cache.json      # Auto-downloaded (gitignored)
```

## 🎓 Skills Demonstrated
- **Networking**: ARP protocol, subnet scanning, port scanning
- **Cybersecurity**: Reconnaissance, vendor fingerprinting, device inventory
- **Web Development**: Flask REST API, responsive UI, data visualization
- **Data Processing**: IEEE OUI parsing, parallel processing (ThreadPoolExecutor)
- **DevOps**: GitHub repo, requirements management, documentation

## 🤝 Contributing
1. Fork the repo
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- **IEEE OUI Database** - Official vendor registry
- **vis.js** - Interactive network visualization
- **Scapy** - Packet crafting and network scanning
- **Project inspiration**: "10 Actually Creative Projects To Fall In Love With Hacking" [YouTube](https://youtu.be/10CLi-OUy4E)

---

**Built by Peter Vu | Cybersecurity Portfolio Project #3** 🚀
