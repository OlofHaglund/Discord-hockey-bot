# Discord Hockey Bot

Minimal Python scaffold for a Discord bot, intended to run in a container.

## Setup (Local)

1) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Copy the env file and add your bot token:

```bash
cp .env.example .env
```

Optional: disable play-by-play logging:

```bash
PLAY_BY_PLAY_LOGGING=false
```

3) Run the bot:

```bash
python src/bot.py
```

## Setup (Podman)

1) Build the image:

```bash
podman build -t discord-hockey-bot .
```

2) Copy the env file and add your bot token:

```bash
cp .env.example .env
```

3) Run the container:

```bash
podman run --rm --env-file .env discord-hockey-bot
```

## Podman Helper Script

```bash
./podman.sh build
./podman.sh run
```

## Bot Commands

- `/ping` - basic health check

## Multi-team Mode

`TEAM_CODES` in `src/bot.py` can include multiple team codes to run multiple polling services at once.
All services share the same Discord token, so each will post announcements into the same configured channel.
