"""Explicit network check of Python TLS trust after the eMudhra CA incident."""

from __future__ import annotations

import concurrent.futures
import json
import socket
import ssl
import sys

import certifi

HOSTS = (
    "example.com",
    "dv-g3b-emudhra.we-have-a-problem.com",
    "dv-g3b-aaa-emudhra.we-have-a-problem.com",
    "dv-g3b-noct-emudhra.we-have-a-problem.com",
    "dv-g3b-aaa-noct-emudhra.we-have-a-problem.com",
)


def check_endpoint(task: tuple[str, str | None, str]) -> dict[str, str]:
    """Count only certificate verification errors as evidence of rejection."""
    source, cafile, host = task
    detail = ""
    try:
        context = ssl.create_default_context(cafile=cafile)
        with socket.create_connection((host, 443), timeout=10) as connection:
            with context.wrap_socket(connection, server_hostname=host):
                result = "ACCEPTED"
    except ssl.SSLCertVerificationError as exc:
        result, detail = "REJECTED", str(exc)
    except (OSError, ssl.SSLError) as exc:
        result, detail = "INCONCLUSIVE", str(exc)
    return {"source": source, "host": host, "result": result, "detail": detail}


def main() -> int:
    """Exit successfully only when both positive and negative checks pass."""
    sources = (("stdlib", None), ("certifi", certifi.where()))
    tasks = [(source, cafile, host) for source, cafile in sources for host in HOSTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_endpoint, tasks))
    ok = all(
        item["result"] == ("ACCEPTED" if item["host"] == HOSTS[0] else "REJECTED")
        for item in results
    )
    print(
        json.dumps(
            {
                "python": sys.version.split()[0],
                "ssl_context": ssl.SSLContext.__module__,
                "certifi": certifi.__version__,
                "results": results,
                "ok": ok,
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
