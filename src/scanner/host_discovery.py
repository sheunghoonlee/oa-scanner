"""Host discovery (temporary stub)."""

__all__ = ["HostDiscovery"]


class HostDiscovery:
    """
    Discover alive hosts in a network.

    ⚠️  실제 구현 전까지는 테스트 통과용 더미(dirty stub)입니다.
        ARP → ICMP → `-Pn` 조건부 스캔 로직으로 교체해야 합니다
        (체크리스트 1.1 반영).
    """

    @staticmethod
    def host_discovery(cidr: str) -> list[str]:
        """
        Args:
            cidr: '192.168.1.0/24' 형식의 네트워크 대역

        Returns:
            살아있는 IP 주소 목록 — 현재는 더미 구현으로 빈 리스트 반환
        """
        # TODO: 실제 ARP/ICMP/Nmap 기반 구현으로 교체
        return []
