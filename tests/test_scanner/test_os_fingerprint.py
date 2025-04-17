"""OS 핑거프린팅 테스트 모듈."""

import unittest
from unittest.mock import patch, MagicMock
import pytest
from src.scanner.os_fingerprint import OSFingerprint

__all__ = ['TestOSFingerprint']

class TestOSFingerprint(unittest.TestCase):
    """OS 핑거프린팅 테스트 클래스."""
    
    def setUp(self):
        self.fingerprinter = OSFingerprint()
    
    @patch('subprocess.run')
    def test_valid_os_string(self, mock_run):
        """유효한 OS 정보가 있는 경우 테스트."""
        # Mock subprocess.run
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "# OS details: Linux 5.4 - 5.10\n"
        mock_run.return_value = mock_result
        
        # Run test
        result = self.fingerprinter.fingerprint("192.168.1.1")
        
        # Verify result
        self.assertEqual(result, "Linux 5.4 - 5.10")
        
        # Verify command
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertIn("nmap", cmd)
        self.assertIn("-O", cmd)
        self.assertIn("-T1", cmd)
        self.assertIn("192.168.1.1", cmd)
    
    @patch('subprocess.run')
    def test_no_match_returns_none(self, mock_run):
        """OS 정보가 없는 경우 None 반환 테스트."""
        # Mock subprocess.run
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "No OS information available\n"
        mock_run.return_value = mock_result
        
        # Run test
        result = self.fingerprinter.fingerprint("192.168.1.1")
        
        # Verify result
        self.assertIsNone(result)
    
    def test_invalid_ip_raises(self):
        """잘못된 IP 주소로 핑거프린팅 시 ValueError 발생 테스트."""
        with pytest.raises(ValueError):
            self.fingerprinter.fingerprint("invalid_ip") 