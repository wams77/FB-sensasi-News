from __future__ import annotations

import logging
import sys
from pathlib import Path

from config import LOG_DIR


LOG_FILE = Path(LOG_DIR) / "bot.log"


logger = logging.getLogger("SensasiNews")

logger.setLevel(logging.INFO)

logger.handlers.clear()


formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)


console = logging.StreamHandler(

    sys.stdout

)

console.setFormatter(

    formatter

)


file_handler = logging.FileHandler(

    LOG_FILE,

    encoding="utf-8",

)

file_handler.setFormatter(

    formatter

)


logger.addHandler(

    console

)

logger.addHandler(

    file_handler

)


logger.propagate = False
