"""상세 보안 점검을 담당하는 모듈."""

import logging
import subprocess
from typing import Dict
import ipaddress

__all__ = ['DetailedChecks']

class DetailedChecks:
    """상세 보안 점검 클래스."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def run(self, ip: str) -> Dict[str, bool]:
        """IP 주소에 대한 상세 보안 점검을 수행합니다.
        
        Args:
            ip: 점검할 IP 주소
            
        Returns:
            각 보안 항목의 점검 결과를 담은 딕셔너리
            
        Raises:
            ValueError: 유효하지 않은 IP 주소
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError as e:
            self.logger.error(f"Invalid IP address: {ip}")
            raise ValueError(f"Invalid IP address: {ip}") from e
        
        results = {
            'smbv1': False,
            'anonymous_share': False,
            'weak_tls': False
        }
        
        # SMBv1 프로토콜 점검
        cmd = ["nmap", "--script", "smb-protocols", "-p", "445", ip]
        self.logger.debug(f"Running SMBv1 check: {' '.join(cmd)}")
        result = self._run_nmap_script(cmd)
        if result and "SMBv1 enabled" in result:
            results['smbv1'] = True
        
        # 익명 공유 점검
        cmd = ["nmap", "--script", "smb-enum-shares", "-p", "445", ip]
        self.logger.debug(f"Running anonymous share check: {' '.join(cmd)}")
        result = self._run_nmap_script(cmd)
        if result and "Anonymous login" in result:
            results['anonymous_share'] = True
        
        # 취약한 TLS 점검
        cmd = ["nmap", "--script", "ssl-enum-ciphers", "-p", "443", ip]
        self.logger.debug(f"Running weak TLS check: {' '.join(cmd)}")
        result = self._run_nmap_script(cmd)
        if result and ("TLSv1.0" in result or "SSLv3" in result):
            results['weak_tls'] = True
        
        self.logger.debug(f"Detailed checks results for {ip}: {results}")
        return results
    
    def _run_nmap_script(self, cmd: list) -> str:
        """Nmap 스크립트를 실행하고 결과를 반환합니다."""
        try:
            result = subprocess.run(
                cmd,
                timeout=300,
                capture_output=True,
                text=True,
                shell=False
            )
            if result.returncode == 0:
                return result.stdout
            self.logger.warning(f"Script execution failed: {result.stderr}")
            return ""
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Script execution timeout: {e}")
            return ""
