"""Entrypoint for running one or more bot services."""

import asyncio
import logging

from bot_service import BotService

logger = logging.getLogger("discord_hockey_bot")
TEAM_CODES = ["VLH"]


def main() -> None:
    """Configure logging and run bot services."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    try:
        asyncio.run(_run_bot())
    except KeyboardInterrupt:
        logger.info("Shutdown requested; exiting.")


async def _run_bot() -> None:
    """Run bot services for all configured team codes."""
    services = [BotService(team_code) for team_code in TEAM_CODES]
    await asyncio.gather(*(service.run() for service in services))


if __name__ == "__main__":
    main()
