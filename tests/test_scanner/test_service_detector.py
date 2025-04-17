"""서비스 탐지 테스트 모듈."""

import unittest
from unittest.mock import patch, MagicMock
import pytest
from src.scanner.service_detector import ServiceDetector

__all__ = ['TestServiceDetector']

class TestServiceDetector(unittest.TestCase):
    """서비스 탐지 테스트 클래스."""
    
    def setUp(self):
        self.detector = ServiceDetector()
    
    def test_detect_empty_ports(self):
        """빈 포트 리스트로 탐지 시 빈 딕셔너리 반환 테스트."""
        result = self.detector.detect("192.168.1.1", [])
        self.assertEqual(result, {})
    
    def test_invalid_ip(self):
        """잘못된 IP 주소로 탐지 시 ValueError 발생 테스트."""
        with pytest.raises(ValueError):
            self.detector.detect("invalid_ip", [22])
    
    @patch('subprocess.run')
    def test_detect_single_service(self, mock_run):
        """단일 서비스 탐지 테스트."""
        # Mock subprocess.run
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "22/tcp open  ssh  OpenSSH 8.2\n"
        mock_run.return_value = mock_result
        
        # Run test
        result = self.detector.detect("192.168.1.1", [22])
        
        # Verify result
        self.assertEqual(result, {22: "OpenSSH 8.2"})
        
        # Verify command
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertIn("nmap", cmd)
        self.assertIn("-sV", cmd)
        self.assertIn("--version-intensity", cmd)
        self.assertIn("192.168.1.1:22", cmd) 