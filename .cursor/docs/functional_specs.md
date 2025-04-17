# Functional Specs (Draft)

| Module | Function | Input | Output | Exceptions | Notes |
|--------|----------|-------|--------|------------|-------|
| scanner/nmap_runner.py | host_discovery(cidr: str) | "192.168.1.0/24" | list[str] (alive IPs) | NetworkError | ARP -> ICMP -> -Pn |
| scanner/nmap_runner.py | port_scan(ip: str) | "192.168.1.10" | list[int] (open ports) | ScanTimeout | --top-ports 100 |
| scanner/nmap_runner.py | service_scan(ip: str) | "192.168.1.10" | dict{port:banner} | ScanTimeout | -sV --version-intensity 2 |
| scanner/nmap_runner.py | os_fingerprint(ip: str) | "192.168.1.10" | str (OS guess) | ScanError | -O -T1 |
| scanner/nmap_runner.py | detailed_checks(ip: str) | "192.168.1.10" | dict{check:result} | ScanError | SMB/HTTP/FTP etc. |
| core/license.py | validate_key(key: str) | "COMPANY-20251231" | bool | InvalidKeyError | SHA‑256 check |
| core/state.py | save_state(path: str, data: dict) | "scan_state.json" | None | IOError | atomic write |
| core/state.py | load_state(path: str) | "scan_state.json" | dict | ValueError | integrity check |
| ui/main_window.py | start_scan() | – | None | – | triggers scanner |
| ui/main_window.py | update_progress() | – | None | – | uses signals/slots |
