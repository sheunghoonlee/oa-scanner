"""포트 스캐닝을 담당하는 모듈."""

import logging
import re
import subprocess
from typing import List
import ipaddress

__all__ = ['PortScanner', 'ScanTimeout']

class ScanTimeout(Exception):
    """스캔 시간 초과 예외."""
    pass

class PortScanner:
    """포트 스캐너 클래스."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def scan(self, ip: str, top_ports: int = 100) -> List[int]:
        """IP 주소의 열린 포트를 스캔합니다.
        
        Args:
            ip: 스캔할 IP 주소
            top_ports: 스캔할 상위 포트 수 (기본값: 100)
            
        Returns:
            발견된 열린 포트 번호 리스트 (정렬됨)
            
        Raises:
            ValueError: 유효하지 않은 IP 주소
            ScanTimeout: 스캔 시간 초과
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError as e:
            self.logger.error(f"Invalid IP address: {ip}")
            raise ValueError(f"Invalid IP address: {ip}") from e
        
        cmd = ["nmap", "-T1", "--top-ports", str(top_ports), "-oG", "-", ip]
        self.logger.debug(f"Running port scan command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                timeout=300,
                capture_output=True,
                text=True,
                shell=False
            )
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Port scan timeout for {ip}")
            raise ScanTimeout(f"Port scan timeout for {ip}") from e
        
        if result.returncode != 0:
            self.logger.warning(f"Port scan failed for {ip}: {result.stderr}")
            return []
        
        open_ports = self._parse_nmap_output(result.stdout)
        self.logger.debug(f"Found {len(open_ports)} open ports for {ip}")
        return sorted(open_ports)
    
    def _parse_nmap_output(self, output: str) -> List[int]:
        """Nmap 출력에서 열린 포트 번호를 추출합니다."""
        pattern = r"Ports: (.*?)\t"
        match = re.search(pattern, output)
        if not match:
            return []
        
        ports_str = match.group(1)
        open_ports = []
        
        for port_info in ports_str.split(", "):
            if "/open" in port_info:
                port = int(port_info.split("/")[0])
                open_ports.append(port)
        
        return open_ports
