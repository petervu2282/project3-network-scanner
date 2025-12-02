"""
Network Device Scanner + Visual Map (Project 3 - COMPLETE)
Cybersecurity tool: ARP scan → IEEE OUI vendor lookup → Interactive web dashboard + network map
Run as Administrator for Scapy to work on Windows!
"""

import scapy.all as scapy
from flask import Flask, render_template_string, request
import os
import json
import time
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# === CONFIG ===
SUBNET = "192.168.2.0/24"  # CHANGE TO YOUR NETWORK
OUI_CACHE = "oui_cache.json"

# === 1. IEEE OUI DATABASE (Auto-download) ===
def download_oui_db():
    """Download fresh IEEE OUI database (cached 24h)"""
    if os.path.exists(OUI_CACHE) and (time.time() - os.path.getmtime(OUI_CACHE)) < 86400:
        return load_oui_cache()
    
    print("📥 Downloading IEEE OUI database...")
    try:
        import requests
        resp = requests.get("https://standards-oui.ieee.org/oui/oui.json", timeout=10)
        oui_data = resp.json()
        
        vendors = {}
        for entry in oui_data:
            oui = entry['oui'].replace('-', ':').upper()
            vendors[oui] = entry['org_name']
        
        with open(OUI_CACHE, 'w') as f:
            json.dump(vendors, f)
        print(f"✅ Saved {len(vendors)} vendors")
        return vendors
    except:
        print("⚠️ Using fallback vendors")
        return load_fallback_vendors()

def load_oui_cache():
    with open(OUI_CACHE, 'r') as f:
        return json.load(f)

def load_fallback_vendors():
    return {
        "00:1A:2B": "Cisco", "00:1B:63": "Apple", "F4:5C:89": "Samsung",
        "00:50:56": "VMware", "08:00:27": "VirtualBox", "52:54:00": "QEMU"
    }

def get_mac_vendor(mac):
    """Lookup vendor from OUI database"""
    mac = mac.upper()
    vendors = download_oui_db()
    return vendors.get(mac[0:8], "Unknown")

# === 2. ENHANCED NETWORK SCANNING ===
def scan_network(ip_range):
    """ARP scan + hostname + ports"""
    print(f"🔍 Scanning {ip_range}...")
    
    # ARP scan (needs admin rights)
    try:
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        answered = scapy.srp(arp_request_broadcast := broadcast/arp_request, 
                           timeout=3, verbose=False)[0]
        
        devices = []
        for sent, received in answered:
            device = {
                "ip": received.psrc,
                "mac": received.hwsrc,
                "vendor": get_mac_vendor(received.hwsrc)
            }
            devices.append(device)
    except Exception as e:
        print(f"⚠️ Scapy failed ({e}), using ping scan...")
        devices = ping_scan(ip_range)
    
    # Add hostname + ports
    devices = enrich_devices(devices)
    print(f"✅ Found {len(devices)} devices")
    return devices

def ping_scan(ip_range):
    """Fallback ping scanner (no admin needed)"""
    devices = []
    base = '.'.join(ip_range.split('.')[:-1])
    for i in range(1, 255):
        ip = f"{base}.{i}"
        if subprocess.run(['ping', '-n', '1', '-w', '500', ip], 
                         capture_output=True).returncode == 0:
            devices.append({"ip": ip, "mac": "N/A", "vendor": "Ping Active"})
    return devices

def enrich_devices(devices):
    """Add hostname + open ports"""
    def get_hostname(ip):
        try: return socket.gethostbyaddr(ip)[0]
        except: return "Unknown"
    
    def scan_ports(ip):
        ports = [22, 80, 443, 445, 3389, 8080]
        open_ports = []
        for port in ports:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        return open_ports
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        for device in devices:
            device['hostname'] = executor.submit(get_hostname, device['ip']).result()
            device['ports'] = executor.submit(scan_ports, device['ip']).result()
    return devices

# === 3. WEB DASHBOARD ===
@app.route("/")
def dashboard():
    devices = scan_network(SUBNET)
    query = request.args.get('q', '').lower()
    
    # Filter
    filtered = [d for d in devices 
                if (query in d['ip'].lower() or 
                    query in d['vendor'].lower() or 
                    query in d['hostname'].lower())] if query else devices
    
    return render_template_string(DASHBOARD_HTML, 
                                devices=filtered, 
                                subnet=SUBNET, 
                                query=query, 
                                count=len(filtered))

@app.route("/map")
def network_map():
    devices = scan_network(SUBNET)
    nodes = [{"id": i, "label": f"{d['ip']}\n{d['vendor']}", 
              "title": f"Ports: {d['ports']}", "color": "#007bff"} 
             for i, d in enumerate(devices)]
    return render_template_string(MAP_HTML, nodes_json=nodes)

# === HTML TEMPLATES ===
DASHBOARD_HTML = """
<!DOCTYPE html>
<html><head><title>Network Scanner Pro</title>
<style>
body{font-family:Arial;padding:20px;background:#f5f5f5;}
.container{max-width:1200px;margin:auto;background:white;padding:20px;border-radius:10px;}
input{padding:10px;width:300px;border:2px solid #ddd;border-radius:5px;}
button{padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer;}
table{width:100%;border-collapse:collapse;margin-top:20px;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd;}
th{background:#007bff;color:white;}
tr:hover{background:#f1f1f1;}
.stats{background:#e9ecef;padding:15px;border-radius:5px;margin-bottom:20px;}
.suspicious{background:#fff3cd;}
</style></head><body>
<div class="container">
<h1>🔍 Network Device Scanner Pro</h1>
<div class="stats">
<strong>{{ count }} devices</strong> on {{ subnet }} 
| <a href="/">🔄 Rescan</a> | <a href="/map">🌐 Network Map</a>
</div>
<form method="GET">
<input name="q" placeholder="Search IP/MAC/Vendor/Hostname..." value="{{ query }}">
<button>🔎 Filter</button>{% if query %}<a href="/" style="margin-left:10px;">Clear</a>{% endif %}
</form>
<table>
<tr><th>IP</th><th>Hostname</th><th>MAC</th><th>Vendor</th><th>Open Ports</th></tr>
{% for d in devices %}
<tr class="{% if 'unknown' in d.vendor.lower() or d.mac=='N/A' %}suspicious{% endif %}">
<td><strong>{{ d.ip }}</strong></td>
<td>{{ d.hostname }}</td>
<td>{{ d.mac }}</td>
<td>{{ d.vendor }}</td>
<td>{{ d.ports|join(', ') or 'None' }}</td>
</tr>{% endfor %}</table>
</div></body></html>
"""

MAP_HTML = """
<!DOCTYPE html>
<html><head>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>#network{width:100%;height:600px;border:1px solid #ccc;}body{font-family:Arial;padding:20px;}</style>
</head><body>
<h1>🌐 Network Topology Map</h1>
<a href="/">← Back to Table</a>
<div id="network"></div>
<script>
const nodes = new vis.DataSet({{ nodes_json|tojson }});
const edges = new vis.DataSet([]);
const container = document.getElementById('network');
const data = {nodes: nodes, edges: edges};
const options = {
    nodes: {shape:'dot',size:25,font:{size:12},color:{background:'rgba(7,123,255,0.8)'}},
    physics: {enabled: true, stabilization: {iterations: 100}}
};
new vis.Network(container, data, options);
</script></body></html>
"""

if __name__ == "__main__":
    print("🚀 Starting Network Scanner (Run as Administrator!)")
    print(f"📡 Scanning: {SUBNET}")
    print("🌐 Dashboard: http://localhost:5000")
    print("🗺️  Map: http://localhost:5000/map")
    app.run(debug=True, host='0.0.0.0', port=5000)
