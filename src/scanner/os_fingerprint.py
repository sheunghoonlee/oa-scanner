"""OS 핑거프린팅을 담당하는 모듈."""

import logging
import re
import subprocess
from typing import Optional
import ipaddress

__all__ = ['OSFingerprint']

class OSFingerprint:
    """OS 핑거프린팅 클래스."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def fingerprint(self, ip: str) -> Optional[str]:
        """IP 주소의 운영체제 정보를 탐지합니다.
        
        Args:
            ip: 탐지할 IP 주소
            
        Returns:
            운영체제 정보 문자열 또는 None
            
        Raises:
            ValueError: 유효하지 않은 IP 주소
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError as e:
            self.logger.error(f"Invalid IP address: {ip}")
            raise ValueError(f"Invalid IP address: {ip}") from e
        
        cmd = ["nmap", "-O", "-T1", ip, "-oG", "-"]
        self.logger.debug(f"Running OS fingerprint command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                timeout=300,
                capture_output=True,
                text=True,
                shell=False
            )
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"OS fingerprint timeout for {ip}")
            return None
        
        if result.returncode != 0:
            self.logger.warning(f"OS fingerprint failed for {ip}: {result.stderr}")
            return None
        
        os_info = self._parse_nmap_output(result.stdout)
        if os_info:
            self.logger.debug(f"Found OS info for {ip}: {os_info}")
        else:
            self.logger.debug(f"No OS info found for {ip}")
        return os_info
    
    def _parse_nmap_output(self, output: str) -> Optional[str]:
        """Nmap 출력에서 OS 정보를 추출합니다."""
        # OS details 패턴
        pattern = r"OS details: (.*?)(?:\n|$)"
        match = re.search(pattern, output)
        if match:
            return match.group(1).strip()
        
        # Running 패턴 (OS details가 없을 때)
        pattern = r"Running: (.*?)(?:\n|$)"
        match = re.search(pattern, output)
        if match:
            return match.group(1).strip()
        
        return None
