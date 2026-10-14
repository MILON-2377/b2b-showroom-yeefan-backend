import logging
import logging.config
import sys

from app.core.config import settings


def configure_logging() -> None:
    configured_level = getattr(settings, "LOG_LEVEL", "INFO")
    log_level = str(configured_level).upper()

    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        log_level = "INFO"

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": ("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "standard",
                    "stream": sys.stdout,
                },
            },
            "root": {
                "level": log_level,
                "handlers": ["console"],
            },
        }
    )
