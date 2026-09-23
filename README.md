# SSL Certificate Monitor

A small, dependency-free Python CLI and library for checking TLS certificate validity and expiry across one or many endpoints. It is designed for local checks, cron jobs and CI monitoring with stable exit codes and optional JSON output.

## Why it exists
Expired certificates cause avoidable outages. This tool provides a transparent check using Python's standard TLS validation instead of requiring a hosted monitoring account.

## Features
- Validates the normal TLS trust chain and hostname using the system CA store.
- Reports expiry timestamp, remaining days, issuer, subject and serial number.
- Checks multiple `HOST` or `HOST:PORT` targets and target files.
- `OK`, `WARNING`, `CRITICAL` and `ERROR` states with configurable thresholds.
- Human-readable and JSON output.
- Automation-friendly exit codes: `0` OK, `1` warning, `2` critical/error.
- Python API; no runtime dependencies, accounts, telemetry or API keys.

## Preview
```text
OK       example.com:443   81d    2026-12-13T23:59:59+00:00
WARNING  service.test:443  14d    2026-10-07T23:59:59+00:00
```
Dates above are illustrative output, not live certificate data.

## Requirements & installation
Python 3.10+.

```bash
python -m pip install -e .
ssl-monitor --version
```

## Usage
```bash
ssl-monitor example.com
ssl-monitor example.com api.example.com:8443 --warn-days 21 --critical-days 5
ssl-monitor example.com --json
ssl-monitor --file targets.txt --timeout 3
```

`targets.txt` accepts one `HOST` or `HOST:PORT` per line; blank lines and lines beginning with `#` are ignored.

Python API:
```python
from ssl_certificate_monitor import inspect_certificate, status_for

result = inspect_certificate("example.com", timeout=5)
print(status_for(result, warn_days=30, critical_days=7))
print(result.expires_at)
```

## Configuration
There is deliberately no hidden configuration file. CLI flags define timeout and warning thresholds, making automated runs reproducible.

## Project structure
```text
src/ssl_certificate_monitor/  # engine, CLI and public API
tests/                        # deterministic unit/CLI tests
.github/workflows/ci.yml      # cross-platform CI
```

## Testing
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
```
Tests mock network-dependent CLI results so the suite does not depend on public endpoints. CI runs on Linux, Windows and macOS with Python 3.10, 3.12 and 3.13.

## Security & privacy
Certificate checks make outbound TCP/TLS connections only to targets you explicitly provide. No credentials, browsing data or telemetry are collected. Standard certificate and hostname validation stays enabled; the project does not provide an insecure verification bypass.

## Limitations
This is active polling, not a daemon or hosted alerting service. It does not send email/Slack notifications, perform OCSP/CRL auditing, inspect every certificate in a chain, or bypass private/internal CA trust requirements. Remaining days are rounded down to whole days.

## Optional roadmap
Notification adapters and structured Prometheus output may be added if they can remain explicit and testable.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for behavioral changes.

## License
MIT — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

# العربية — مراقب شهادات SSL/TLS

أداة Python محلية خفيفة بلا اعتماديات تشغيل خارجية لفحص صلاحية شهادات TLS وموعد انتهائها لمضيف واحد أو عدة مضيفين. تصلح للفحص اليدوي وCI والمهام المجدولة، وتوفر خرج JSON ورموز خروج ثابتة للأتمتة.

## لماذا المشروع؟
انتهاء الشهادات قد يسبب توقف الخدمات. توفر الأداة فحصًا مباشرًا وشفافًا يعتمد على التحقق القياسي في Python من سلسلة الثقة واسم المضيف دون الحاجة إلى حساب في خدمة مراقبة خارجية.

## المزايا
- التحقق من الثقة واسم المضيف باستخدام مخزن شهادات النظام.
- عرض تاريخ الانتهاء والأيام المتبقية والمُصدر والموضوع والرقم التسلسلي.
- فحص `HOST` و`HOST:PORT` وعدة أهداف أو ملف أهداف.
- حالات `OK` و`WARNING` و`CRITICAL` و`ERROR` مع حدود قابلة للضبط.
- خرج نصي أو JSON.
- رموز خروج للأتمتة: `0` سليم، `1` تحذير، `2` حرج/خطأ.
- API لبايثون، دون مفاتيح API أو تتبع أو حسابات.

## التثبيت والمتطلبات
تحتاج Python 3.10 أو أحدث:
```bash
python -m pip install -e .
ssl-monitor --version
```

## الاستخدام
```bash
ssl-monitor example.com
ssl-monitor example.com api.example.com:8443 --warn-days 21 --critical-days 5
ssl-monitor example.com --json
ssl-monitor --file targets.txt --timeout 3
```
ملف الأهداف يحتوي مضيفًا واحدًا في كل سطر، ويمكن استخدام `#` للتعليقات.

## الإعداد
لا يوجد ملف إعداد مخفي عمدًا؛ تضبط المهلة وحدود التحذير عبر خيارات CLI حتى تكون عمليات التشغيل قابلة لإعادة الإنتاج بوضوح.

## بنية المشروع
المحرك وCLI داخل `src/ssl_certificate_monitor/`، والاختبارات داخل `tests/`، وCI داخل `.github/workflows/ci.yml`.

## الاختبارات
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
```
اختبارات CLI تعزل الشبكة، بينما يشغّل CI الاختبارات على Linux وWindows وmacOS وإصدارات Python المدعومة المختارة.

## الأمان والخصوصية
تتصل الأداة فقط بالأهداف التي تحددها صراحة. لا تجمع بيانات اعتماد أو بيانات تصفح ولا ترسل telemetry. التحقق القياسي من الشهادة واسم المضيف يبقى مفعّلًا ولا يوجد خيار لتعطيله بطريقة غير آمنة.

## القيود
ليست خدمة تنبيه مستضافة ولا daemon دائمًا. لا ترسل بريدًا أو Slack، ولا تنفذ تدقيق OCSP/CRL، ولا تتجاوز متطلبات الثقة للشهادات الداخلية، والأيام المتبقية مقربة للأسفل إلى أيام كاملة.

## التطوير الاختياري
يمكن مستقبلًا إضافة موصلات تنبيه أو خرج Prometheus إذا بقيت صريحة وقابلة للاختبار.

## المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وأضف اختبارات لأي تغيير سلوكي.

## الترخيص
MIT — راجع [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
