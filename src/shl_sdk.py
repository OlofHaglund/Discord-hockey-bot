"""Small SDK wrapper for SHL API calls."""

import aiohttp


class ShlApiError(RuntimeError):
    """Raised when the SHL API response is not as expected."""

    pass


class ShlSdk:
    """Convenience wrapper around the SHL API endpoints."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the SDK with a shared aiohttp session."""
        self._session = session

    async def get_upcoming_live_games(self) -> list[dict]:
        """Return upcoming or live games from the SHL API."""
        url = "https://www.shl.se/api/sports-v2/upcoming-live-games"
        return await self._get_json(url)

    async def get_team_stats(self, game_uuid: str) -> dict:
        """Return team stats for the given game UUID."""
        url = f"https://www.shl.se/api/gameday/team-stats/{game_uuid}"
        return await self._get_json(url, require_json=True)

    async def get_game_info(self, game_uuid: str) -> dict:
        """Return game info metadata for the given game UUID."""
        url = f"https://www.shl.se/api/sports-v2/game-info/{game_uuid}"
        return await self._get_json(url)

    async def get_play_by_play(self, game_uuid: str) -> list[dict]:
        """Return play-by-play events for the given game UUID."""
        url = f"https://www.shl.se/api/gameday/play-by-play/{game_uuid}"
        return await self._get_json(url)

    async def _get_json(self, url: str, require_json: bool = False):
        """Fetch JSON from the given URL, optionally enforcing content type."""
        async with self._session.get(url) as response:
            response.raise_for_status()
            if require_json:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    raise ShlApiError(f"Unexpected content type for {url}: {content_type}")
            return await response.json()
