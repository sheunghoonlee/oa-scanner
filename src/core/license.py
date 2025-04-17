"""라이선스 관리를 담당하는 모듈."""

import hashlib
import logging
import re
from datetime import datetime
from typing import Set, Optional

__all__ = ['LicenseManager']

# 내부 DB 시뮬레이션용 유효한 해시 목록
VALID_HASHES: Set[str] = {
    "d41d8cd98f00b204e9800998ecf8427e"  # 예시 해시
}

class LicenseManager:
    """라이선스 관리 클래스."""
    
    SALT = "netscanner"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_key(self, key: str) -> bool:
        """라이선스 키의 유효성을 검사합니다.
        
        Args:
            key: 검사할 라이선스 키
            
        Returns:
            키가 유효하면 True, 아니면 False
        """
        # 키 형식 검사
        if not re.match(r"^[A-Z0-9]+-\d{8}$", key):
            self.logger.debug(f"Invalid key format: {key}")
            return False
        
        # 만료일 검사
        try:
            expiry_date = datetime.strptime(key.split('-')[1], '%Y%m%d')
            if expiry_date.date() < datetime.utcnow().date():
                self.logger.debug(f"Key expired: {key}")
                return False
        except ValueError:
            self.logger.debug(f"Invalid date format in key: {key}")
            return False
        
        # 해시 검사
        key_hash = hashlib.sha256((key + self.SALT).encode()).hexdigest()
        if key_hash not in VALID_HASHES:
            self.logger.debug(f"Unknown key hash: {key_hash}")
            return False
        
        return True
    
    def get_license_info(self) -> Optional[dict]:
        # IMPLEMENT: 라이선스 정보 조회
        pass
    
    def activate_license(self, key: str) -> bool:
        # IMPLEMENT: 라이선스 활성화
        pass 