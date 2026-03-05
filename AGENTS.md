# Discord Hockey Bot

## Project Summary

Discord bot that posts updates about ice hockey games.

## Default Role

Use the Developer role for coding and maintenance tasks.

## Working Guidelines

- Keep changes small and reversible.
- Match existing coding conventions and file layout.
- Prefer configuration-driven behavior for teams, leagues, and schedules.
- Log external API errors with enough detail to debug.
- Avoid leaking secrets or tokens in logs or docs.
- Keep `README.md` and this file aligned with current setup and workflow.

## Testing

- When asked to test or run the bot, rebuild the container first: `./podman.sh build`.
- Run with Podman (for example `./podman.sh run`) instead of running the Python file directly.

## References

- `SHL-apis.md`
- `game-data-apis.md`
