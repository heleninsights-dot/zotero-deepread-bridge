#!/usr/bin/env python3
"""Thin wrapper — delegates to the installed zotero-deepread-bridge package.

If you're working from a git clone and haven't pip-installed the package yet,
this script adds src/ to sys.path so you can still run it directly:

    python3 tools/zotero_collection_pdfs.py list
"""

import sys
from pathlib import Path

try:
    from zotero_deepread_bridge.cli import main
except ImportError:
    src = Path(__file__).resolve().parent.parent / "src"
    if src.is_dir():
        sys.path.insert(0, str(src))
        try:
            from zotero_deepread_bridge.cli import main
        except ImportError:
            print(
                "Could not import zotero_deepread_bridge.\n\n"
                "Install the package:\n"
                "  pip install git+https://github.com/heleninsights-dot/zotero-deepread-bridge.git\n\n"
                "Or from a local clone:\n"
                "  pip install -e .\n"
                "  python3 -m zotero_deepread_bridge list\n",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        print(
            "Could not import zotero_deepread_bridge and src/ directory not found.\n\n"
            "Install the package:\n"
            "  pip install git+https://github.com/heleninsights-dot/zotero-deepread-bridge.git\n",
            file=sys.stderr,
        )
        sys.exit(1)

sys.exit(main())
