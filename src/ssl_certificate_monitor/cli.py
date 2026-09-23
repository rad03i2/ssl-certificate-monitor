from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .core import inspect_certificate, status_for

VERSION = "1.0.0"


def _target(value: str) -> tuple[str, int]:
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("target cannot be empty")
    if ":" in value:
        host, raw_port = value.rsplit(":", 1)
        try:
            port = int(raw_port)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("port must be an integer") from exc
    else:
        host, port = value, 443
    if not host or not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("expected HOST or HOST:PORT")
    return host, port


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ssl-monitor", description="Check TLS certificate validity and expiry.")
    p.add_argument("targets", nargs="*", type=_target, metavar="HOST[:PORT]")
    p.add_argument("--file", type=Path, help="read one target per line (# comments allowed)")
    p.add_argument("--warn-days", type=int, default=30)
    p.add_argument("--critical-days", type=int, default=7)
    p.add_argument("--timeout", type=float, default=5.0)
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    p.add_argument("--version", action="version", version=f"ssl-certificate-monitor {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.critical_days < 0 or args.warn_days < args.critical_days:
        build_parser().error("thresholds require 0 <= critical-days <= warn-days")
    targets = list(args.targets)
    if args.file:
        try:
            lines = args.file.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr); return 2
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                try: targets.append(_target(line))
                except argparse.ArgumentTypeError as exc:
                    print(f"error in {args.file}: {line}: {exc}", file=sys.stderr); return 2
    if not targets:
        build_parser().error("provide at least one target or --file")

    rows = []
    exit_code = 0
    for host, port in targets:
        result = inspect_certificate(host, port, args.timeout)
        status = status_for(result, args.warn_days, args.critical_days)
        row = {"status": status, **result.to_dict()}
        rows.append(row)
        if status in {"ERROR", "CRITICAL"}: exit_code = 2
        elif status == "WARNING" and exit_code == 0: exit_code = 1
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            remaining = "-" if row["days_remaining"] is None else f'{row["days_remaining"]}d'
            detail = row["error"] or row["expires_at"] or "-"
            print(f'{row["status"]:<8} {row["host"]}:{row["port"]:<5} {remaining:<6} {detail}')
    return exit_code
