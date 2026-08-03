from __future__ import annotations

from logger import logger

from bot import NewsBot


def banner():

    logger.info("")

    logger.info("=" * 70)

    logger.info("")

    logger.info("        GOSIP.ID AI NEWS BOT")

    logger.info("")

    logger.info("        Football • KPOP • Entertainment")

    logger.info("")

    logger.info("=" * 70)

    logger.info("")


def main():

    banner()

    bot = NewsBot()

    bot.run()

    logger.info("")

    logger.info("=" * 70)

    logger.info("BOT FINISHED")

    logger.info("=" * 70)


if __name__ == "__main__":

    main()

