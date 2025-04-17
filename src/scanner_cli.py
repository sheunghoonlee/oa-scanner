"""네트워크 스캐너 CLI 진입점."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# ── 절대 경로 임포트 ----------------------------------------------------
from src.core.license import LicenseManager
from src.scanner.scan_workflow import ScanWorkflow
# -----------------------------------------------------------------------

LOG_FMT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


# ---------------------------------------------------------------------- #
# helpers
# ---------------------------------------------------------------------- #
def _setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level, format=LOG_FMT)


def _get_license_key(args: argparse.Namespace) -> str:
    """CLI 옵션 → 환경변수 → 사용자 입력 순으로 라이선스 키를 얻는다."""
    if args.license:
        return args.license

    env_key = os.getenv("NETSCAN_LICENSE")
    if env_key:
        return env_key

    # 테스트에서도 stdin을 요구하지 않도록 기본 빈 문자열 반환
    return input("Enter license key: ").strip()


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="netscanner", description="Unauthenticated network scanner")
    parser.add_argument("--cidr", required=True, help="Target network CIDR (e.g. 192.168.1.0/24)")
    parser.add_argument("--top-ports", type=int, default=100, help="Top N ports to scan (default: 100)")
    parser.add_argument("-k", "--license", help="License key (optionally use env NETSCAN_LICENSE)")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO"], default="INFO")
    parser.add_argument("--out", default="scan_results.xlsx", help="Excel output path")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------- #
# main entry
# ---------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    """CLI 메인 함수.

    Args:
        argv: 테스트 시 전달할 인수 리스트. `None`이면 `sys.argv[1:]` 사용.

    Returns:
        0 성공, 1 라이선스 오류, 2 스캔 중 예외
    """
    args = _parse_args(argv)
    _setup_logging(args.log_level)

    # ── 라이선스 검증 ---------------------------------------------------
    key = _get_license_key(args)
    if not LicenseManager.validate_key(key):
        logging.error("Invalid license key")
        return 1

    # ── 워크플로우 실행 -------------------------------------------------
    try:
        ScanWorkflow(network_cidr=args.cidr, top_ports=args.top_ports).run()
        logging.info("Excel report saved to %s", Path(args.out).resolve())
    except Exception as exc:  # pragma: no cover  (표준 예외 통합)
        logging.exception("Scan failed: %s", exc)
        return 2

    return 0


if __name__ == "__main__":           # 파일 직접 실행 시
    raise SystemExit(main())
