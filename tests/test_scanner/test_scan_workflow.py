"""ScanWorkflow 테스트 모듈."""

import pytest
from src.scanner.scan_workflow import ScanWorkflow
from src.scanner.host_discovery import HostDiscovery
from src.scanner.port_scanner import PortScanner
from src.scanner.service_detector import ServiceDetector
from src.scanner.os_fingerprint import OSFingerprint
from src.scanner.detailed_checks import DetailedChecks
from src.core.resume import ResumeManager
from src.core.state import StateManager

class TestScanWorkflow:
    """ScanWorkflow 테스트 클래스."""
    
    def setup_method(self):
        """테스트 메서드 실행 전 초기화."""
        self.workflow = ScanWorkflow("192.168.1.0/24")
    
    def test_scan_workflow(self, monkeypatch):
        """스캔 워크플로우 테스트."""
        # 모의(mock) 메서드 설정
        def mock_host_discovery(cidr):
            return ["192.168.1.10"]
        
        def mock_port_scan(ip, top_ports):
            return [22]
        
        def mock_service_detect(ip, ports):
            return {22: "SSH"}
        
        def mock_fingerprint(ip):
            return "Linux"
        
        def mock_checks(ip):
            return {"smbv1": False}
        
        def mock_should_resume():
            return False
        
        def mock_save_state(state):
            pass
        
        # 메서드 패치
        monkeypatch.setattr(HostDiscovery, 'host_discovery', mock_host_discovery)
        monkeypatch.setattr(PortScanner, 'scan', mock_port_scan)
        monkeypatch.setattr(ServiceDetector, 'detect', mock_service_detect)
        monkeypatch.setattr(OSFingerprint, 'fingerprint', mock_fingerprint)
        monkeypatch.setattr(DetailedChecks, 'run', mock_checks)
        monkeypatch.setattr(ResumeManager, 'should_resume', mock_should_resume)
        monkeypatch.setattr(StateManager, 'save_state', mock_save_state)
        
        # 워크플로우 실행
        results = self.workflow.run()
        
        # 결과 검증
        assert len(results) == 1
        result = results[0]
        assert result["ip"] == "192.168.1.10"
        assert result["open_ports"] == [22]
        assert result["services"] == {22: "SSH"}
        assert result["os"] == "Linux"
        assert result["checks"] == {"smbv1": False}
    
    def test_resume_workflow(self, monkeypatch):
        """재개된 스캔 워크플로우 테스트."""
        # 모의(mock) 메서드 설정
        def mock_should_resume():
            return True
        
        def mock_get_pending_ips():
            return ["192.168.1.10"]
        
        def mock_port_scan(ip, top_ports):
            return [22]
        
        def mock_service_detect(ip, ports):
            return {22: "SSH"}
        
        def mock_fingerprint(ip):
            return "Linux"
        
        def mock_checks(ip):
            return {"smbv1": False}
        
        def mock_save_state(state):
            pass
        
        # 메서드 패치
        monkeypatch.setattr(ResumeManager, 'should_resume', mock_should_resume)
        monkeypatch.setattr(ResumeManager, 'get_pending_ips', mock_get_pending_ips)
        monkeypatch.setattr(PortScanner, 'scan', mock_port_scan)
        monkeypatch.setattr(ServiceDetector, 'detect', mock_service_detect)
        monkeypatch.setattr(OSFingerprint, 'fingerprint', mock_fingerprint)
        monkeypatch.setattr(DetailedChecks, 'run', mock_checks)
        monkeypatch.setattr(StateManager, 'save_state', mock_save_state)
        
        # 워크플로우 실행
        results = self.workflow.run()
        
        # 결과 검증
        assert len(results) == 1
        result = results[0]
        assert result["ip"] == "192.168.1.10"
        assert result["open_ports"] == [22]
        assert result["services"] == {22: "SSH"}
        assert result["os"] == "Linux"
        assert result["checks"] == {"smbv1": False} 