"""Service layer for polling SHL games and posting announcements."""

import asyncio
import json
import logging
import os
import signal
from datetime import datetime, timezone

import aiohttp
import discord
from discord.ext import commands
from discord.ext import tasks

from shl_sdk import ShlApiError, ShlSdk

logger = logging.getLogger("discord_hockey_bot")
START_ANNOUNCE_CHANNEL_ID = 1462165235677790434
PLAY_BY_PLAY_DIR = os.path.join(os.getcwd(), "data", "play_by_play")


class BotService:
    """Coordinates SHL polling, Discord announcements, and shutdown handling."""

    def __init__(self, team_code: str) -> None:
        """Initialize service state for a team code."""
        self._team_code = team_code
        self._play_by_play_logging_enabled = self._get_env_bool(
            "PLAY_BY_PLAY_LOGGING", default=True
        )
        self._team_game_uuids: set[str] = set()
        self._team_game_start_times: dict[str, str] = {}
        self._play_by_play_tasks: dict[str, asyncio.Task] = {}
        self._last_event_ids: dict[str, int] = {}
        self._start_announced_uuids: set[str] = set()
        self._game_over_announced_uuids: set[str] = set()
        self._period_event_keys: dict[str, set[str]] = {}
        self._bot: commands.Bot | None = None

    def create_bot(self) -> commands.Bot:
        """Create and configure the Discord bot instance."""
        intents = discord.Intents.default()
        intents.message_content = True

        bot = commands.Bot(command_prefix="/", intents=intents)
        self._bot = bot
        bot._startup_checked = False  # avoid duplicate startup requests on reconnect

        @bot.event
        async def on_ready() -> None:
            """Handle the Discord ready event."""
            logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)
            if bot._startup_checked:
                return
            bot._startup_checked = True
            if not self._hourly_upcoming_games_check.is_running():
                self._hourly_upcoming_games_check.start()

        @bot.command(name="ping")
        async def ping(ctx: commands.Context) -> None:
            """Respond with a basic health check."""
            await ctx.send("Pong!")

        return bot

    async def run(self) -> None:
        """Run the bot service until shutdown is requested."""
        token = self._get_required_env("DISCORD_TOKEN")
        bot = self.create_bot()
        stop_event = asyncio.Event()

        def _request_shutdown() -> None:
            """Signal the bot to shut down."""
            if not stop_event.is_set():
                stop_event.set()

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _request_shutdown)
            except NotImplementedError:
                pass

        async with bot:
            bot_task = asyncio.create_task(bot.start(token))
            stop_task = asyncio.create_task(stop_event.wait())
            done, pending = await asyncio.wait(
                {bot_task, stop_task}, return_when=asyncio.FIRST_COMPLETED
            )
            if stop_task in done:
                await self._shutdown_bot(bot)
                await bot_task
            else:
                stop_task.cancel()
                await asyncio.gather(stop_task, return_exceptions=True)

    def _get_required_env(self, name: str) -> str:
        """Fetch a required environment variable."""
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return value

    def _get_env_bool(self, name: str, default: bool = False) -> bool:
        """Parse a boolean environment variable with a default."""
        value = os.getenv(name)
        if value is None:
            return default
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
        logger.warning("Invalid %s value %r; using default %s", name, value, default)
        return default

    async def _check_upcoming_live_games(self) -> None:
        """Fetch upcoming/live games and schedule polling tasks."""
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                sdk = ShlSdk(session)
                games = await sdk.get_upcoming_live_games()
                team_game_uuids = await self._find_team_game_uuids(sdk, games)
                team_game_start_times = await self._fetch_game_start_times(sdk, team_game_uuids)
            self._store_team_game_uuids(team_game_uuids)
            self._store_team_game_start_times(team_game_start_times)
            self._schedule_play_by_play_tasks(team_game_start_times)
            logger.info("Startup upcoming-live-games response: %s", games)
            logger.info(
                "Found %d games for %s: %s",
                len(team_game_uuids),
                self._team_code,
                sorted(team_game_uuids),
            )
            logger.info("Team game start times: %s", team_game_start_times)
        except Exception:
            logger.exception("Failed to fetch upcoming live games on startup.")

    async def _find_team_game_uuids(self, sdk: ShlSdk, games: list[dict]) -> set[str]:
        """Filter upcoming games to those involving the configured team."""
        team_game_uuids: set[str] = set()
        for game in games:
            game_uuid = game.get("gameUuid")
            if not game_uuid:
                continue
            try:
                team_stats = await self._fetch_team_stats(sdk, game_uuid)
            except Exception:
                logger.warning(
                    "Failed to fetch team stats for gameUuid %s", game_uuid, exc_info=True
                )
                continue
            if team_stats and self._team_stats_has_code(team_stats, self._team_code):
                team_game_uuids.add(game_uuid)
        return team_game_uuids

    async def _fetch_team_stats(self, sdk: ShlSdk, game_uuid: str) -> dict:
        """Fetch team stats, tolerating non-JSON responses."""
        try:
            return await sdk.get_team_stats(game_uuid)
        except ShlApiError:
            return {}

    def _team_stats_has_code(self, team_stats: dict, team_code: str) -> bool:
        """Return whether team stats include the given team code."""
        for side in ("home", "away"):
            team = team_stats.get(side)
            if isinstance(team, dict) and team.get("teamCode") == team_code:
                return True
        return False

    def _store_team_game_uuids(self, team_game_uuids: set[str]) -> None:
        """Persist team game UUIDs in memory."""
        self._team_game_uuids = set(team_game_uuids)

    async def _fetch_game_start_times(
        self, sdk: ShlSdk, game_uuids: set[str]
    ) -> dict[str, str]:
        """Fetch start times for the provided game UUIDs."""
        start_times: dict[str, str] = {}
        for game_uuid in game_uuids:
            try:
                game_info = await self._fetch_game_info(sdk, game_uuid)
            except Exception:
                logger.warning("Failed to fetch game info for gameUuid %s", game_uuid, exc_info=True)
                continue
            start_date_time = self._extract_start_date_time(game_info)
            if start_date_time:
                start_times[game_uuid] = start_date_time
        return start_times

    async def _fetch_game_info(self, sdk: ShlSdk, game_uuid: str) -> dict:
        """Fetch game info metadata."""
        return await sdk.get_game_info(game_uuid)

    def _extract_start_date_time(self, game_info: dict) -> str | None:
        """Extract the startDateTime from game info, if present."""
        info = game_info.get("gameInfo")
        if isinstance(info, dict):
            start_date_time = info.get("startDateTime")
            if isinstance(start_date_time, str):
                return start_date_time
        return None

    def _store_team_game_start_times(self, start_times: dict[str, str]) -> None:
        """Persist team game start times in memory."""
        self._team_game_start_times = dict(start_times)

    def _schedule_play_by_play_tasks(self, start_times: dict[str, str]) -> None:
        """Schedule polling tasks for each game start time."""
        for game_uuid, start_time in start_times.items():
            if game_uuid in self._play_by_play_tasks:
                continue
            start_dt = self._parse_start_time(start_time)
            if not start_dt:
                logger.warning("Invalid startDateTime for gameUuid %s: %s", game_uuid, start_time)
                continue
            task = asyncio.create_task(self._run_play_by_play_polling(game_uuid, start_dt))
            self._play_by_play_tasks[game_uuid] = task

    def _parse_start_time(self, start_time: str) -> datetime | None:
        """Parse an ISO start time into a UTC datetime."""
        try:
            if start_time.endswith("Z"):
                start_time = start_time[:-1] + "+00:00"
            return datetime.fromisoformat(start_time).astimezone(timezone.utc)
        except ValueError:
            return None

    async def _run_play_by_play_polling(self, game_uuid: str, start_dt: datetime) -> None:
        """Poll play-by-play for a game until it ends or the task is cancelled."""
        try:
            now = datetime.now(timezone.utc)
            if start_dt > now:
                await asyncio.sleep((start_dt - now).total_seconds())

            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                sdk = ShlSdk(session)
                while True:
                    try:
                        events = await self._fetch_play_by_play(sdk, game_uuid)
                    except Exception:
                        logger.warning(
                            "Failed to fetch play-by-play for gameUuid %s",
                            game_uuid,
                            exc_info=True,
                        )
                    else:
                        if self._play_by_play_logging_enabled:
                            self._persist_play_by_play(game_uuid, events)
                        await self._maybe_announce_game_start(game_uuid, events)
                        await self._handle_new_events(game_uuid, events)
                        if self._is_game_over(events):
                            await self._announce_game_over(game_uuid, events)
                            logger.info(
                                "Game ended for gameUuid %s, stopping play-by-play polling.",
                                game_uuid,
                            )
                            break
                    await asyncio.sleep(60)
        except asyncio.CancelledError:
            logger.info("Play-by-play polling cancelled for gameUuid %s.", game_uuid)
            raise
        finally:
            self._play_by_play_tasks.pop(game_uuid, None)
            self._last_event_ids.pop(game_uuid, None)
            self._period_event_keys.pop(game_uuid, None)

    async def _fetch_play_by_play(self, sdk: ShlSdk, game_uuid: str) -> list[dict]:
        """Fetch play-by-play data for a game."""
        return await sdk.get_play_by_play(game_uuid)

    def _is_game_over(self, events: list[dict]) -> bool:
        """Return whether the game has ended based on latest events."""
        if not events:
            return False
        latest_event = events[0]
        game_state = latest_event.get("gameState")
        return game_state in {"GameEnded", "GameOver", "Final"}

    async def _handle_new_events(self, game_uuid: str, events: list[dict]) -> None:
        """Process newly arrived play-by-play events."""
        new_events = self._extract_new_events(game_uuid, events)
        new_period_events = self._extract_new_period_events(game_uuid, events)
        if not new_events and not new_period_events:
            return
        logger.info(
            "Processing %d new play-by-play events for %s",
            len(new_events) + len(new_period_events),
            game_uuid,
        )
        for event in new_events:
            await self._maybe_announce_event(game_uuid, event)
        for event in new_period_events:
            await self._announce_period_break(game_uuid, event)

    def _extract_new_events(self, game_uuid: str, events: list[dict]) -> list[dict]:
        """Return non-period events that are newer than the last seen event ID."""
        last_event_id = self._last_event_ids.get(game_uuid)
        events_with_id = [event for event in events if isinstance(event.get("eventId"), int)]
        if not events_with_id:
            return []
        max_event_id = max(event["eventId"] for event in events_with_id)
        if last_event_id is None:
            self._last_event_ids[game_uuid] = max_event_id
            return []
        new_events = [event for event in events_with_id if event["eventId"] > last_event_id]
        self._last_event_ids[game_uuid] = max_event_id
        new_events.sort(key=lambda event: event["eventId"])
        return new_events

    def _extract_new_period_events(self, game_uuid: str, events: list[dict]) -> list[dict]:
        """Return newly finished period events not previously announced."""
        period_events = [
            event
            for event in events
            if event.get("type") == "period" and event.get("finished") is True
        ]
        if game_uuid not in self._period_event_keys:
            self._period_event_keys[game_uuid] = {
                key for event in period_events if (key := self._period_event_key(event))
            }
            return []
        seen_keys = self._period_event_keys[game_uuid]
        new_events: list[dict] = []
        for event in period_events:
            key = self._period_event_key(event)
            if not key or key in seen_keys:
                continue
            seen_keys.add(key)
            new_events.append(event)
        new_events.sort(key=lambda event: event.get("period") or 0)
        return new_events

    def _period_event_key(self, event: dict) -> str | None:
        """Build a stable key for a period end event."""
        period = event.get("period")
        if not isinstance(period, int):
            return None
        finished_at = event.get("finishedAt") or event.get("realWorldTime") or event.get("startedAt")
        if isinstance(finished_at, str):
            return f"{period}:{finished_at}"
        return str(period)

    async def _maybe_announce_game_start(self, game_uuid: str, events: list[dict]) -> None:
        """Announce game start once when the first events appear."""
        if game_uuid in self._start_announced_uuids:
            return
        if not any(isinstance(event.get("eventId"), int) for event in events):
            return
        if self._bot is None:
            logger.warning("Bot not ready; cannot announce game start for %s", game_uuid)
            return
        channel = await self._get_announce_channel()
        if channel is None:
            logger.warning(
                "Channel %s not found; cannot announce game start for %s",
                START_ANNOUNCE_CHANNEL_ID,
                game_uuid,
            )
            return
        matchup = self._find_latest_matchup(events)
        self._start_announced_uuids.add(game_uuid)
        if matchup:
            await channel.send(f"Game started: {matchup}")
        else:
            await channel.send("Game started!")

    async def _maybe_announce_event(self, game_uuid: str, event: dict) -> None:
        """Route an event to the proper announcement handler."""
        event_type = event.get("type")
        if event_type == "goal":
            await self._announce_goal(game_uuid, event)
        elif event_type == "penalty":
            await self._announce_penalty(game_uuid, event)
        elif event_type == "period" and event.get("finished") is True:
            await self._announce_period_break(game_uuid, event)

    async def _announce_goal(self, game_uuid: str, event: dict) -> None:
        """Announce a goal event."""
        channel = await self._get_announce_channel()
        if channel is None:
            return
        team_code = self._event_team_code(event)
        time = event.get("time")
        period = event.get("period")
        home_goals = event.get("homeGoals")
        away_goals = event.get("awayGoals")
        score = self._format_score(home_goals, away_goals)
        matchup = self._find_matchup_from_event(event)
        message = "Goal"
        message = self._append_event_details(message, team_code, period, time, score, matchup)
        await channel.send(message)

    async def _announce_penalty(self, game_uuid: str, event: dict) -> None:
        """Announce a penalty event."""
        channel = await self._get_announce_channel()
        if channel is None:
            return
        team_code = self._event_team_code(event)
        time = event.get("time")
        period = event.get("period")
        offence = self._expand_offence(event.get("offence"))
        matchup = self._find_matchup_from_event(event)
        message = "Penalty"
        message = self._append_event_details(message, team_code, period, time, None, matchup)
        if offence:
            message += f" - {offence}"
        await channel.send(message)

    async def _announce_period_break(self, game_uuid: str, event: dict) -> None:
        """Announce the end of a period."""
        channel = await self._get_announce_channel()
        if channel is None:
            return
        period = event.get("period")
        matchup = self._find_matchup_from_event(event)
        message = "Period break"
        if matchup:
            message += f" - {matchup}"
        if period is not None:
            message += f" - End of period {period}"
        await channel.send(message)

    async def _announce_game_over(self, game_uuid: str, events: list[dict]) -> None:
        """Announce final score when the game ends."""
        if game_uuid in self._game_over_announced_uuids:
            return
        channel = await self._get_announce_channel()
        if channel is None:
            return
        final_score = self._find_latest_score(events)
        teams = self._find_latest_team_codes(events)
        message = "Match over"
        if teams and final_score:
            message += f" - {teams[0]} {final_score} {teams[1]}"
        elif final_score:
            message += f" - Final score {final_score}"
        self._game_over_announced_uuids.add(game_uuid)
        await channel.send(message)

    async def _get_announce_channel(self):
        """Return the configured Discord channel if available."""
        if self._bot is None:
            logger.warning("Bot not ready; cannot announce events.")
            return None
        await self._bot.wait_until_ready()
        return self._bot.get_channel(START_ANNOUNCE_CHANNEL_ID)

    def _event_team_code(self, event: dict) -> str | None:
        """Extract the team code from an event."""
        event_team = event.get("eventTeam")
        if isinstance(event_team, dict):
            team_code = event_team.get("teamCode")
            if isinstance(team_code, str):
                return team_code
        return None

    def _format_score(self, home_goals: int | None, away_goals: int | None) -> str | None:
        """Format a score string if both sides are present."""
        if isinstance(home_goals, int) and isinstance(away_goals, int):
            return f"{home_goals}-{away_goals}"
        return None

    def _append_event_details(
        self,
        message: str,
        team_code: str | None,
        period: int | None,
        time: str | None,
        score: str | None,
        matchup: str | None,
    ) -> str:
        """Append details to a message, using a consistent format."""
        parts: list[str] = []
        if matchup:
            parts.append(matchup)
        if team_code:
            parts.append(team_code)
        if period is not None:
            parts.append(f"P{period}")
        if time:
            parts.append(time)
        if score:
            parts.append(score)
        if parts:
            message += f" - {' | '.join(parts)}"
        return message

    def _find_latest_score(self, events: list[dict]) -> str | None:
        """Return the most recent score found in events."""
        for event in events:
            score = self._format_score(event.get("homeGoals"), event.get("awayGoals"))
            if score:
                return score
        return None

    def _find_latest_team_codes(self, events: list[dict]) -> tuple[str, str] | None:
        """Return the most recent home/away team codes from events."""
        for event in events:
            home_team = event.get("homeTeam")
            away_team = event.get("awayTeam")
            if isinstance(home_team, dict) and isinstance(away_team, dict):
                home_code = home_team.get("teamCode")
                away_code = away_team.get("teamCode")
                if isinstance(home_code, str) and isinstance(away_code, str):
                    return home_code, away_code
        return None

    def _find_matchup_from_event(self, event: dict) -> str | None:
        """Return a matchup string from a single event."""
        home_team = event.get("homeTeam")
        away_team = event.get("awayTeam")
        if isinstance(home_team, dict) and isinstance(away_team, dict):
            home_code = home_team.get("teamCode")
            away_code = away_team.get("teamCode")
            if isinstance(home_code, str) and isinstance(away_code, str):
                return f"{home_code} vs {away_code}"
        return None

    def _find_latest_matchup(self, events: list[dict]) -> str | None:
        """Return the latest matchup string from events."""
        for event in events:
            matchup = self._find_matchup_from_event(event)
            if matchup:
                return matchup
        return None

    def _expand_offence(self, offence: str | None) -> str | None:
        """Expand an offence code to a readable label."""
        if not offence:
            return None
        offence_map = {
            "HI-ST": "High Sticking",
            "HOLD": "Holding",
            "HOOK": "Hooking",
            "TRIP": "Tripping",
            "ROUGH": "Roughing",
            "SLASH": "Slashing",
            "CROSS": "Cross Checking",
            "INTERF": "Interference",
            "ELBOW": "Elbowing",
            "CHARGE": "Charging",
            "BOARD": "Boarding",
            "KNEE": "Kneeing",
            "UNSPORT": "Unsportsmanlike Conduct",
            "DELAY": "Delay of Game",
        }
        return offence_map.get(offence, offence)

    def _persist_play_by_play(self, game_uuid: str, events: list[dict]) -> None:
        """Persist play-by-play events to disk."""
        try:
            game_dir = os.path.join(PLAY_BY_PLAY_DIR, game_uuid)
            os.makedirs(game_dir, exist_ok=True)
            path = os.path.join(game_dir, "play_by_play.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(events, handle, ensure_ascii=True)
        except Exception:
            logger.warning("Failed to persist play-by-play for gameUuid %s", game_uuid, exc_info=True)

    @tasks.loop(hours=1)
    async def _hourly_upcoming_games_check(self) -> None:
        """Periodic task to refresh upcoming/live games."""
        await self._check_upcoming_live_games()

    async def _shutdown_bot(self, bot: commands.Bot) -> None:
        """Cancel tasks and close the Discord client."""
        logger.info("Shutting down bot tasks.")
        if self._hourly_upcoming_games_check.is_running():
            self._hourly_upcoming_games_check.cancel()
        tasks_to_cancel = list(self._play_by_play_tasks.values())
        for task in tasks_to_cancel:
            task.cancel()
        if tasks_to_cancel:
            await asyncio.gather(*tasks_to_cancel, return_exceptions=True)
        self._play_by_play_tasks.clear()
        await bot.close()
