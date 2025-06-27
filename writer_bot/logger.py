"""writer_bot/logger.py – Rich-colour logger that is safe on legacy Windows consoles."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler

# --------------------------------------------------------------------------- #
#  Paths & constants
# --------------------------------------------------------------------------- #
LOG_PATH = Path("writer_bot.log")
LOG_PATH.touch(exist_ok=True)

_FMT = "%(asctime)s | %(levelname)-8s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def _safe_filter(record: logging.LogRecord) -> bool:
    """
    Strip characters that the current console code-page cannot encode.

    Prevents `UnicodeEncodeError: cp1252` when an emoji or other non-ASCII glyph
    sneaks into a log call on Windows cmd / PowerShell running the default
    legacy code-page.

    The message is *pre-formatted* inside the filter so that `record.args`
    can be cleared – otherwise the original (unsafe) string would be formatted
    again downstream and the error would reappear.
    """
    encoding = sys.stdout.encoding or "ascii"
    try:
        # getMessage() applies % formatting with record.args
        safe_msg = record.getMessage().encode(encoding, errors="ignore").decode(
            encoding
        )
    except Exception:  # very last-ditch fallback
        safe_msg = record.getMessage().encode("ascii", "ignore").decode()

    record.msg = safe_msg
    record.args = ()  # already interpolated
    return True


# --------------------------------------------------------------------------- #
#  Handlers
# --------------------------------------------------------------------------- #
# 1‣ colourful console
console_handler = RichHandler(rich_tracebacks=True, markup=True)
console_handler.addFilter(_safe_filter)

# 2‣ rotating UTF-8 logfile (keeps full Unicode)
file_handler = RotatingFileHandler(
    LOG_PATH, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)

# --------------------------------------------------------------------------- #
#  Global logger config
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format=_FMT,
    datefmt=_DATE_FMT,
    handlers=[console_handler, file_handler],
    force=True,  # overwrite any previous basicConfig
)

log = logging.getLogger("writer_bot")
