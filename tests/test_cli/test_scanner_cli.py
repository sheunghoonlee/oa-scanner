"""CLI 테스트 모듈 (수정판)."""

from __future__ import annotations

from src.scanner_cli import main
from src.core.license import LicenseManager


class TestScannerCLI:
    """Scanner CLI 동작 검증."""

    BASE_ARGS = ["--cidr", "127.0.0.1/32", "--top-ports", "10"]

    # ──────────────────────────────────────────────────────────────
    # 성공 시나리오
    # ──────────────────────────────────────────────────────────────
    def test_valid_license_exit_zero(self, monkeypatch):
        """유효한 라이선스 → 종료 코드 0."""
        monkeypatch.setattr(LicenseManager, "validate_key", lambda *_: True)

        exit_code = main(self.BASE_ARGS + ["--license", "OK"])
        assert exit_code == 0

    # ──────────────────────────────────────────────────────────────
    # 실패 시나리오
    # ──────────────────────────────────────────────────────────────
    def test_invalid_license_exit_one(self, monkeypatch):
        """잘못된 라이선스 → 종료 코드 1."""
        monkeypatch.setattr(LicenseManager, "validate_key", lambda *_: False)

        exit_code = main(self.BASE_ARGS + ["--license", "BAD"])
        assert exit_code == 1
