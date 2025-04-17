"""Nmap 실행을 관리하는 모듈."""

import logging
import re
import subprocess
from typing import List, Dict
from .host_discovery import HostDiscovery
from .port_scanner import PortScanner
from .service_detector import ServiceDetector
from .os_fingerprint import OSFingerprint
import ipaddress

__all__ = ['NmapRunner']

class NmapRunner:
    """Nmap 실행을 관리하는 클래스."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def host_discovery(self, cidr: str) -> List[str]:
        """CIDR 범위 내 활성 호스트를 발견합니다.
        
        Args:
            cidr: 검사할 네트워크 범위 (CIDR 표기법)
            
        Returns:
            발견된 활성 호스트 IP 주소 리스트
            
        Raises:
            ValueError: 유효하지 않은 CIDR 형식
        """
        try:
            ipaddress.ip_network(cidr)
        except ValueError as e:
            self.logger.error(f"Invalid CIDR format: {cidr}")
            raise ValueError(f"Invalid CIDR format: {cidr}") from e
        
        ips = set()
        
        # ARP 스캔
        self.logger.debug(f"Starting ARP scan for {cidr}")
        result = subprocess.run(
            ["nmap", "-sn", "-PR", cidr],
            timeout=300,
            capture_output=True,
            text=True,
            shell=False,
            check=False
        )
        if result.returncode == 0:
            ips.update(self._parse_nmap_output(result.stdout))
        
        # ICMP 스캔 (ARP 실패 시)
        if not ips:
            self.logger.debug(f"Starting ICMP scan for {cidr}")
            result = subprocess.run(
                ["nmap", "-sn", "-PE", cidr],
                timeout=300,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
            if result.returncode == 0:
                ips.update(self._parse_nmap_output(result.stdout))
        
        # TCP Ping (ARP, ICMP 실패 시)
        if not ips:
            self.logger.debug(f"Starting TCP ping scan for {cidr}")
            result = subprocess.run(
                ["nmap", "-sn", "-Pn", cidr],
                timeout=300,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
            if result.returncode == 0:
                ips.update(self._parse_nmap_output(result.stdout))
        
        return sorted(list(ips))
    
    def _parse_nmap_output(self, output: str) -> set:
        """Nmap 출력에서 IP 주소를 추출합니다."""
        pattern = r"Nmap scan report for (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        return set(re.findall(pattern, output))
    
    def port_scan(self, ip: str) -> List[int]:
        # IMPLEMENT: 포트 스캔
        pass
    
    def service_scan(self, ip: str) -> Dict[int, str]:
        # IMPLEMENT: 서비스 스캔
        pass
    
    def os_fingerprint(self, ip: str) -> str:
        # IMPLEMENT: OS 핑거프린팅
        pass
    
    def detailed_checks(self, ip: str) -> Dict[str, str]:
        # IMPLEMENT: 상세 점검
        pass 