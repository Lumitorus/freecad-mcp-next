#!/usr/bin/env python3
"""Check local prerequisites and the FreeCAD RPC endpoint."""

from __future__ import annotations

import argparse
import shutil
import socket
import sys
import xmlrpc.client


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=9875, type=int)
    args = parser.parse_args()

    failed = False
    print(f"Python: {sys.version.split()[0]}")
    print(f"uv: {shutil.which('uv') or 'NOT FOUND'}")
    try:
        with socket.create_connection((args.host, args.port), timeout=2):
            print(f"TCP {args.host}:{args.port}: reachable")
        proxy = xmlrpc.client.ServerProxy(f"http://{args.host}:{args.port}", allow_none=True)
        print(f"RPC ping: {proxy.ping()}")
    except (OSError, xmlrpc.client.Error) as exc:
        failed = True
        print(f"RPC: FAILED ({exc})")
        print("Open FreeCAD, select 'MCP Addon', and click 'Start RPC Server'.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
