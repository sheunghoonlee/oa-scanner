"""공통 예외 클래스들을 정의하는 모듈."""

__all__ = ['NetworkError', 'ConfigError', 'OutputError', 'StateError', 'StateCorruptedError']

class NetworkError(Exception):
    """네트워크 관련 예외."""
    pass

class ConfigError(Exception):
    """설정 관련 예외."""
    pass

class OutputError(Exception):
    """출력 관련 예외."""
    pass

class StateError(Exception):
    """상태 관리 관련 예외."""
    pass

class StateCorruptedError(StateError):
    """상태 파일 손상 관련 예외."""
    pass 