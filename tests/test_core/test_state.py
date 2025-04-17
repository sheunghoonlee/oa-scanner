"""StateManager 테스트 모듈."""

import json
import os
import tempfile
from pathlib import Path
import pytest
from src.core.state import StateManager, INTERNAL_PATH_DEFAULT
from src.utils.exceptions import StateError, StateCorruptedError

class TestStateManager:
    """StateManager 테스트 클래스."""
    
    def setup_method(self):
        """테스트 메서드 실행 전 초기화."""
        self.manager = StateManager()
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = Path(self.temp_dir) / "test_state.json"
    
    def teardown_method(self):
        """테스트 메서드 실행 후 정리."""
        if self.test_path.exists():
            self.test_path.unlink()
        os.rmdir(self.temp_dir)
    
    def test_save_state_default_path(self, tmp_path):
        """기본 경로에 상태 저장 테스트."""
        data = {"test": "data"}
        self.manager.save_state(data)
        assert Path(INTERNAL_PATH_DEFAULT).exists()
        with open(INTERNAL_PATH_DEFAULT, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded == data
        Path(INTERNAL_PATH_DEFAULT).unlink()
    
    def test_save_state_custom_path(self):
        """사용자 정의 경로에 상태 저장 테스트."""
        data = {"test": "data"}
        self.manager.save_state(data, self.test_path)
        assert self.test_path.exists()
        with open(self.test_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded == data
    
    def test_save_state_atomic_write(self):
        """원자적 쓰기 테스트."""
        data = {"test": "data"}
        self.manager.save_state(data, self.test_path)
        assert not self.test_path.with_suffix('.tmp').exists()
    
    def test_save_state_error(self):
        """저장 실패 시 예외 발생 테스트."""
        with pytest.raises(StateError):
            self.manager.save_state({}, "/invalid/path/state.json")
    
    def test_load_state_default_path(self, tmp_path):
        """기본 경로에서 상태 로드 테스트."""
        data = {"test": "data"}
        with open(INTERNAL_PATH_DEFAULT, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        loaded = self.manager.load_state()
        assert loaded == data
        Path(INTERNAL_PATH_DEFAULT).unlink()
    
    def test_load_state_custom_path(self):
        """사용자 정의 경로에서 상태 로드 테스트."""
        data = {"test": "data"}
        with open(self.test_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        loaded = self.manager.load_state(self.test_path)
        assert loaded == data
    
    def test_load_state_not_found(self):
        """파일이 없는 경우 None 반환 테스트."""
        assert self.manager.load_state(self.test_path) is None
    
    def test_load_state_corrupted(self):
        """손상된 파일 로드 시 예외 발생 테스트."""
        with open(self.test_path, 'w', encoding='utf-8') as f:
            f.write("invalid json")
        
        with pytest.raises(StateCorruptedError):
            self.manager.load_state(self.test_path) 