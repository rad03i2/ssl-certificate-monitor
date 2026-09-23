"""SSL Certificate Monitor public API."""
from .core import CertificateResult, inspect_certificate, status_for

__all__ = ["CertificateResult", "inspect_certificate", "status_for"]
__version__ = "1.0.0"
