"""서비스 탐지를 담당하는 모듈."""

import logging
import re
import subprocess
from typing import Dict, List
import ipaddress

__all__ = ['ServiceDetector']

class ServiceDetector:
    """서비스 탐지 클래스."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def detect(self, ip: str, ports: List[int]) -> Dict[int, str]:
        """IP 주소의 특정 포트에서 실행 중인 서비스를 탐지합니다.
        
        Args:
            ip: 탐지할 IP 주소
            ports: 탐지할 포트 번호 리스트
            
        Returns:
            포트 번호를 키로, 서비스 정보를 값으로 하는 딕셔너리
            
        Raises:
            ValueError: 유효하지 않은 IP 주소
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError as e:
            self.logger.error(f"Invalid IP address: {ip}")
            raise ValueError(f"Invalid IP address: {ip}") from e
        
        if not ports:
            self.logger.debug("No ports to scan")
            return {}
        
        port_args = [f"{ip}:{p}" for p in ports]
        cmd = ["nmap", "-sV", "--version-intensity", "2"] + port_args
        self.logger.debug(f"Running service detection command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                timeout=300,
                capture_output=True,
                text=True,
                shell=False
            )
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Service detection timeout for {ip}")
            return {}
        
        if result.returncode != 0:
            self.logger.warning(f"Service detection failed for {ip}: {result.stderr}")
            return {}
        
        services = self._parse_nmap_output(result.stdout)
        self.logger.debug(f"Found {len(services)} services for {ip}")
        return services
    
    def _parse_nmap_output(self, output: str) -> Dict[int, str]:
        """Nmap 출력에서 서비스 정보를 추출합니다."""
        pattern = r"(\d+)/tcp\s+open\s+\S+\s+(.*?)(?:\n|$)"
        services = {}
        
        for match in re.finditer(pattern, output):
            port = int(match.group(1))
            service = match.group(2).strip()
            services[port] = service
        
        return services
