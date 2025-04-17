"""스캔 워크플로우를 관리하는 모듈."""

import logging
from pathlib import Path
from typing import List, Dict, Any

from .host_discovery import HostDiscovery
from .port_scanner import PortScanner
from .service_detector import ServiceDetector
from .os_fingerprint import OSFingerprint
from .detailed_checks import DetailedChecks
from ..core.resume import ResumeManager
from ..core.state import StateManager
from ..output.excel_writer import ExcelWriter  # Excel 리포트 모듈

__all__ = ["ScanWorkflow"]


class ScanWorkflow:
    """호스트 → 포트 → 서비스 → OS → 상세 점검을 순차로 수행하는 워크플로우."""

    def __init__(self, network_cidr: str, top_ports: int = 100) -> None:
        """
        Args:
            network_cidr: 스캔할 네트워크(CIDR 표기)
            top_ports: 스캔할 상위 포트 수 (기본 100)
        """
        self.logger = logging.getLogger(__name__)
        self.network_cidr = network_cidr
        self.top_ports = top_ports

    # ------------------------------------------------------------------ #
    # public
    # ------------------------------------------------------------------ #
    def run(self) -> List[Dict[str, Any]]:
        """전체 스캔 워크플로우를 실행한다.

        Returns:
            각 호스트별 스캔 결과(dict) 리스트
        """
        results: List[Dict[str, Any]] = []

        # ── 재개 여부 확인 ------------------------------------------------ #
        if ResumeManager.should_resume():
            self.logger.info("Resuming previous scan…")
            targets = ResumeManager.get_pending_ips()
        else:
            self.logger.info("Starting new scan for %s", self.network_cidr)
            targets = HostDiscovery.host_discovery(self.network_cidr)

        # ── 대상 IP별 스캔 ------------------------------------------------ #
        for ip in targets:
            self.logger.info("Scanning %s …", ip)

            open_ports = PortScanner.scan(ip, self.top_ports)
            if not open_ports:
                self.logger.info("No open ports on %s", ip)
                continue

            services = ServiceDetector.detect(ip, open_ports)
            os_info = OSFingerprint.fingerprint(ip)
            checks = DetailedChecks.run(ip)

            results.append(
                {
                    "ip": ip,
                    "open_ports": open_ports,
                    "services": services,
                    "os": os_info,
                    "checks": checks,
                }
            )
            self.logger.info("Completed %s  (%d open ports)", ip, len(open_ports))

        # ── 상태 초기화 --------------------------------------------------- #
        StateManager.save_state({"pending_ips": []})
        self.logger.info("Scan finished: %d host(s) processed", len(results))

        # ── Excel 리포트 저장 -------------------------------------------- #
        if results:  # 결과가 있을 때만 저장
            report_path = Path("scan_results.xlsx")
            ExcelWriter().write(results, str(report_path))   # ← 인스턴스화
            self.logger.info("Excel report saved to %s", report_path.resolve())

        return results
