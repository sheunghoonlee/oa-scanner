"""스캔 재개 기능을 담당하는 모듈."""

import logging
from typing import List
from .state import StateManager


class ResumeManager:
    """스캔 재개 관리 클래스."""

    logger = logging.getLogger(__name__)

    @staticmethod
    def should_resume() -> bool:
        """스캔을 재개해야 하는지 확인한다."""
        state = StateManager.load_state()
        return bool(state and state.get("pending_ips"))

    @staticmethod
    def get_pending_ips() -> List[str]:
        """대기 중인 IP 목록을 반환한다."""
        state = StateManager.load_state()
        return state.get("pending_ips", []) if state else []
