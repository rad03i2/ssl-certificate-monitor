import json
from unittest.mock import patch
from ssl_certificate_monitor.cli import _target, main
from ssl_certificate_monitor.core import CertificateResult


def test_target_default_port():
    assert _target("example.com") == ("example.com", 443)


def test_target_custom_port():
    assert _target("localhost:8443") == ("localhost", 8443)


def test_json_output(capsys):
    fake = CertificateResult("example.com", 443, True, "2030-01-01T00:00:00+00:00", 100)
    with patch("ssl_certificate_monitor.cli.inspect_certificate", return_value=fake):
        assert main(["example.com", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["status"] == "OK"
    assert payload[0]["host"] == "example.com"


def test_warning_exit_code():
    fake = CertificateResult("example.com", 443, True, "2030-01-01T00:00:00+00:00", 10)
    with patch("ssl_certificate_monitor.cli.inspect_certificate", return_value=fake):
        assert main(["example.com"]) == 1


def test_error_exit_code():
    fake = CertificateResult("bad.invalid", 443, False, error="DNS failed")
    with patch("ssl_certificate_monitor.cli.inspect_certificate", return_value=fake):
        assert main(["bad.invalid"]) == 2
