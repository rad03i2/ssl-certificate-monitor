from __future__ import annotations

import socket
import ssl
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class CertificateResult:
    host: str
    port: int
    ok: bool
    expires_at: str | None = None
    days_remaining: int | None = None
    issuer: str | None = None
    subject: str | None = None
    serial_number: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _name(parts: tuple) -> str:
    values = []
    for group in parts:
        for key, value in group:
            if key in {"commonName", "organizationName"}:
                values.append(str(value))
    return ", ".join(values)


def inspect_certificate(host: str, port: int = 443, timeout: float = 5.0) -> CertificateResult:
    host = host.strip()
    if not host:
        raise ValueError("host cannot be empty")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=host) as tls:
                cert = tls.getpeercert()
        not_after = cert.get("notAfter")
        if not not_after:
            raise ssl.SSLError("certificate has no expiry date")
        expiry = datetime.fromtimestamp(ssl.cert_time_to_seconds(not_after), tz=timezone.utc)
        remaining = expiry - datetime.now(timezone.utc)
        days = max(-1, int(remaining.total_seconds() // 86400))
        return CertificateResult(
            host=host, port=port, ok=True,
            expires_at=expiry.isoformat(), days_remaining=days,
            issuer=_name(cert.get("issuer", ())), subject=_name(cert.get("subject", ())),
            serial_number=cert.get("serialNumber"),
        )
    except (OSError, ssl.SSLError, socket.timeout) as exc:
        return CertificateResult(host=host, port=port, ok=False, error=f"{type(exc).__name__}: {exc}")


def status_for(result: CertificateResult, warn_days: int = 30, critical_days: int = 7) -> str:
    if critical_days < 0 or warn_days < critical_days:
        raise ValueError("thresholds must satisfy 0 <= critical_days <= warn_days")
    if not result.ok or result.days_remaining is None:
        return "ERROR"
    if result.days_remaining <= critical_days:
        return "CRITICAL"
    if result.days_remaining <= warn_days:
        return "WARNING"
    return "OK"
