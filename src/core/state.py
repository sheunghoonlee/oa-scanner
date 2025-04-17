"""상태 관리를 담당하는 모듈."""
# 상단 import 유지
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from ..utils.exceptions import StateError, StateCorruptedError

__all__ = ['StateManager']

INTERNAL_PATH_DEFAULT = "scan_state.json"


class StateManager:
    """상태 관리 클래스."""

    logger = logging.getLogger(__name__)  # 클래스‑레벨 로거

    @staticmethod
    def save_state(data: Dict[str, Any],
                   path: Optional[str | Path] = None) -> None:
        """상태 데이터를 원자적으로 저장."""
        if path is None:
            path = INTERNAL_PATH_DEFAULT
        path = Path(path)
        temp_path = path.with_suffix(".tmp")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_path.replace(path)  # 원자적 교체
            StateManager.logger.debug("State saved to %s", path)
        except (OSError, IOError) as exc:
            StateManager.logger.error("Save failed: %s", exc)
            raise StateError(f"Failed to save state: {exc}") from exc

    @staticmethod
    def load_state(path: Optional[str | Path] = None) -> Optional[Dict[str, Any]]:
        """상태 데이터를 로드. 없으면 None, 손상 시 StateCorruptedError."""
        if path is None:
            path = INTERNAL_PATH_DEFAULT
        path = Path(path)
        if not path.exists():
            StateManager.logger.debug("State file not found: %s", path)
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            StateManager.logger.debug("State loaded from %s", path)
            return data
        except json.JSONDecodeError as exc:
            StateManager.logger.error("Corrupted state file: %s", exc)
            raise StateCorruptedError(f"State file corrupted: {exc}") from exc
        except IOError as exc:
            StateManager.logger.error("Read failed: %s", exc)
            raise StateError(f"Failed to read state: {exc}") from exc

