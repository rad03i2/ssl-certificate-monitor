# Security Policy

## Supported version
The latest version on `main` receives security fixes.

## Reporting
Please report suspected vulnerabilities privately through GitHub's available private security-reporting channel when enabled. Do not publish secrets, private keys, internal host inventories, or exploitable details in a public issue.

## Security model
The tool uses Python's default TLS context, validates certificate trust and hostnames, and intentionally offers no `--insecure` switch. Target names are supplied by the operator; therefore do not run untrusted target lists in sensitive network environments without reviewing them first.

Maintainer: Radwan Abdulhadi Ahmed / @rad03i2.
