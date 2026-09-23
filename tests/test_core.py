from ssl_certificate_monitor.core import CertificateResult, status_for


def result(days=None, ok=True):
    return CertificateResult("example.com", 443, ok, days_remaining=days, error=None if ok else "failed")


def test_status_ok():
    assert status_for(result(90)) == "OK"


def test_status_warning():
    assert status_for(result(20)) == "WARNING"


def test_status_critical():
    assert status_for(result(7)) == "CRITICAL"


def test_status_error():
    assert status_for(result(ok=False)) == "ERROR"


def test_threshold_validation():
    try:
        status_for(result(10), warn_days=2, critical_days=3)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_serialization_does_not_hide_fields():
    data = result(42).to_dict()
    assert data["host"] == "example.com"
    assert data["days_remaining"] == 42
