"""LicenseManager 테스트 모듈."""

import hashlib
import pytest
from src.core.license import LicenseManager

class TestLicenseManager:
    """LicenseManager 테스트 클래스."""
    
    def setup_method(self):
        """테스트 메서드 실행 전 초기화."""
        self.manager = LicenseManager()
    
    def test_invalid_format(self):
        """잘못된 형식의 키 검증 테스트."""
        assert not self.manager.validate_key("BADKEY")
    
    def test_expired_date(self):
        """만료된 날짜의 키 검증 테스트."""
        assert not self.manager.validate_key("COMPANY-20000101")
    
    def test_unknown_hash(self):
        """알 수 없는 해시의 키 검증 테스트."""
        assert not self.manager.validate_key("COMPANY-20991231")
    
    def test_valid_key(self, monkeypatch):
        """유효한 키 검증 테스트."""
        key = "COMPANY-20991231"
        key_hash = hashlib.sha256((key + self.manager.SALT).encode()).hexdigest()
        
        # VALID_HASHES를 모의(mock)하여 테스트
        monkeypatch.setattr('src.core.license.VALID_HASHES', {key_hash})
        assert self.manager.validate_key(key) 