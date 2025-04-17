"""ResumeManager 테스트 모듈."""

import pytest
from src.core.resume import ResumeManager
from src.core.state import StateManager

class TestResumeManager:
    """ResumeManager 테스트 클래스."""
    
    def setup_method(self):
        """테스트 메서드 실행 전 초기화."""
        self.manager = ResumeManager()
    
    def test_no_state_returns_false(self, monkeypatch):
        """상태 파일이 없는 경우 False 반환 테스트."""
        def mock_load_state():
            return None
        
        monkeypatch.setattr(StateManager, 'load_state', mock_load_state)
        assert not self.manager.should_resume()
    
    def test_pending_ips_detected(self, monkeypatch):
        """대기 중인 IP가 있는 경우 True 반환 테스트."""
        def mock_load_state():
            return {"pending_ips": ["192.168.1.5"]}
        
        monkeypatch.setattr(StateManager, 'load_state', mock_load_state)
        assert self.manager.should_resume()
    
    def test_get_pending_ips_returns_list(self, monkeypatch):
        """대기 중인 IP 목록 반환 테스트."""
        def mock_load_state():
            return {"pending_ips": ["192.168.1.5"]}
        
        monkeypatch.setattr(StateManager, 'load_state', mock_load_state)
        assert self.manager.get_pending_ips() == ["192.168.1.5"] 