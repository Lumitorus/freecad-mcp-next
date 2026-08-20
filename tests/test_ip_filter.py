from __future__ import annotations

from rpc_server.ip_filter import _parse_allowed_ips, validate_allowed_ips


def test_validate_allowed_ips_accepts_addresses_and_networks() -> None:
    valid, errors = validate_allowed_ips("127.0.0.1, 192.168.1.0/24, ::1")

    assert valid == ["127.0.0.1", "192.168.1.0/24", "::1"]
    assert errors == []


def test_validate_allowed_ips_rejects_malformed_input() -> None:
    valid, errors = validate_allowed_ips("127.0.0.1,,10.0.0.1")

    assert valid == []
    assert errors


def test_parse_allowed_ips_normalizes_single_addresses() -> None:
    networks = _parse_allowed_ips("127.0.0.1,::1")

    assert str(networks[0]) == "127.0.0.1/32"
    assert str(networks[1]) == "::1/128"
