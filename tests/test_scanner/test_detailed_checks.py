"""상세 보안 점검 테스트 모듈."""

import unittest
from unittest.mock import patch, MagicMock
import pytest
from src.scanner.detailed_checks import DetailedChecks

__all__ = ['TestDetailedChecks']

class TestDetailedChecks(unittest.TestCase):
    """상세 보안 점검 테스트 클래스."""
    
    def setUp(self):
        self.checker = DetailedChecks()
    
    @patch('subprocess.run')
    def test_all_false(self, mock_run):
        """모든 점검이 실패하는 경우 테스트."""
        # Mock subprocess.run (3개의 빈 결과)
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_run.side_effect = [mock_result, mock_result, mock_result]
        
        # Run test
        result = self.checker.run("192.168.1.1")
        
        # Verify result
        self.assertEqual(result, {
            'smbv1': False,
            'anonymous_share': False,
            'weak_tls': False
        })
        
        # Verify command calls
        self.assertEqual(mock_run.call_count, 3)
    
    @patch('subprocess.run')
    def test_detect_smbv1(self, mock_run):
        """SMBv1만 감지되는 경우 테스트."""
        # Mock subprocess.run
        mock_result1 = MagicMock()
        mock_result1.returncode = 0
        mock_result1.stdout = "SMBv1 enabled"
        
        mock_result2 = MagicMock()
        mock_result2.returncode = 0
        mock_result2.stdout = ""
        
        mock_result3 = MagicMock()
        mock_result3.returncode = 0
        mock_result3.stdout = ""
        
        mock_run.side_effect = [mock_result1, mock_result2, mock_result3]
        
        # Run test
        result = self.checker.run("192.168.1.1")
        
        # Verify result
        self.assertEqual(result, {
            'smbv1': True,
            'anonymous_share': False,
            'weak_tls': False
        })
    
    @patch('subprocess.run')
    def test_detect_all(self, mock_run):
        """모든 취약점이 감지되는 경우 테스트."""
        # Mock subprocess.run
        mock_result1 = MagicMock()
        mock_result1.returncode = 0
        mock_result1.stdout = "SMBv1 enabled"
        
        mock_result2 = MagicMock()
        mock_result2.returncode = 0
        mock_result2.stdout = "Anonymous login"
        
        mock_result3 = MagicMock()
        mock_result3.returncode = 0
        mock_result3.stdout = "TLSv1.0"
        
        mock_run.side_effect = [mock_result1, mock_result2, mock_result3]
        
        # Run test
        result = self.checker.run("192.168.1.1")
        
        # Verify result
        self.assertEqual(result, {
            'smbv1': True,
            'anonymous_share': True,
            'weak_tls': True
        })
    
    def test_invalid_ip_raises(self):
        """잘못된 IP 주소로 점검 시 ValueError 발생 테스트."""
        with pytest.raises(ValueError):
            self.checker.run("invalid_ip") 