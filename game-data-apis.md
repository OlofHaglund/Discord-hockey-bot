# game-data.s8y.se API

Base path: `https://game-data.s8y.se`

## GET /play-by-play/by-game-uuid/<gameUuid>

Request to fetch the play-by-play event feed for a single game.

**Request**
```
GET /play-by-play/by-game-uuid/<gameUuid> HTTP/2
Host: game-data.s8y.se
```

**Response**
A JSON array of event objects (shots, goals, penalties, period start/end, goalkeeper swaps) in reverse chronological order.

**Object Structure**

Top-level keys (present depending on `type` and event):

| Key | Type | Notes |
| --- | --- | --- |
| `arena` | string | Arena name. |
| `assists` | object | Goal assists; see `assists.*`. |
| `attendance` | int | Attendance count. |
| `awayGoals` | int | Away score after goal event. |
| `awayTeam` | object | Team info; see `team`. |
| `didRenderInPenaltyShot` | bool | Penalty flag. |
| `eventId` | int | Numeric event id. |
| `eventTeam` | object | Team credited with event; see `eventTeam`. |
| `eventUuid` | string | Event UUID. |
| `finished` | bool | For `period` events. |
| `finishedAt` | string | ISO timestamp; for `period` events. |
| `gameId` | int | Numeric game id. |
| `gameSourceId` | string | External game id. |
| `gameState` | string | Game state at event. |
| `gameType` | string | League type. |
| `gameUuid` | string | Game UUID. |
| `goalSection` | int | Shot/goal section. |
| `goalStatus` | string | Goal status, e.g. `EQ`. |
| `homeGoals` | int | Home score after goal event. |
| `homeTeam` | object | Team info; see `team`. |
| `isEmptyNetGoal` | bool | Goal flag. |
| `isEntering` | bool | Goalkeeper event flag. |
| `isPenaltyShot` | bool | Shot/goal flag. |
| `locationX` | int | Shot/goal location. |
| `locationY` | int | Shot/goal location. |
| `nep` | array | Players on ice for non-event team; see `playerRef`. |
| `offence` | string | Penalty code, e.g. `SLASH`. |
| `period` | int | Period number. |
| `player` | object | Primary player; see `player`. |
| `pop` | array | Players on ice for event team; see `playerRef`. |
| `realWorldTime` | string | ISO timestamp. |
| `revision` | int | Revision number. |
| `round` | int | Round number. |
| `startDateAndTime` | string | Game start time. |
| `started` | bool | For `period` events. |
| `startedAt` | string | ISO timestamp; for `period` events. |
| `time` | string | Game clock time, `MM:SS`. |
| `type` | string | One of: `goal`, `goalkeeper`, `penalty`, `period`, `shot`. |
| `updatedTime` | string | ISO timestamp. |
| `variant` | object | Penalty variant; see `variant`. |

`team` object (used by `homeTeam` and `awayTeam`):

| Key | Type | Notes |
| --- | --- | --- |
| `teamId` | string | Team id. |
| `teamName` | string | Team name. |
| `teamCode` | string | Short code. |
| `score` | int | Score at event time. |

`eventTeam` object:

| Key | Type | Notes |
| --- | --- | --- |
| `teamId` | string | Team id. |
| `teamName` | string | Team name. |
| `teamCode` | string | Short code. |
| `place` | string | `home` or `away`. |

`player` object:

| Key | Type | Notes |
| --- | --- | --- |
| `playerId` | string | Player id. |
| `firstName` | string | First name. |
| `familyName` | string | Last name. |
| `jerseyToday` | string | Jersey number. |
| `statistics` | array | Optional; see `player.statistics`. |

`player.statistics` items:

| Key | Type | Notes |
| --- | --- | --- |
| `key` | string | Stat key, e.g. `G`, `A`. |
| `value` | string | Stat value. |

`assists` object:

| Key | Type | Notes |
| --- | --- | --- |
| `first` | object | Assist player; same shape as `player`. |
| `second` | object | Assist player; same shape as `player`. |

`playerRef` items (used by `pop` and `nep`):

| Key | Type | Notes |
| --- | --- | --- |
| `playerId` | string | Player id. |
| `firstName` | string | First name. |
| `familyName` | string | Last name. |
| `jerseyToday` | string | Jersey number. |

`variant` object (penalties):

| Key | Type | Notes |
| --- | --- | --- |
| `shortName` | string | Short description, e.g. `Minor`. |
| `description` | string | Full description, e.g. `2 min`. |
| `minorTime` | string | Minutes as string. |
| `doubleMinorTime` | string | Minutes as string. |
| `benchTime` | string | Minutes as string. |
| `majorTime` | string | Minutes as string. |
| `misconductTime` | string | Minutes as string. |
| `gMTime` | string | Minutes as string. |
| `mPTime` | string | Minutes as string. |

**Example Response**
```
[
  {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "eventId": 123,
    "eventUuid": "6a5642f5-b6d7-526c-a4f2-9190180fbce6",
    "round": 38,
    "gameType": "Elitserien",
    "arena": "Behrn Arena",
    "attendance": 5078,
    "startDateAndTime": "2026-01-22T19:00:00",
    "period": 4,
    "time": "01:46",
    "gameState": "GameEnded",
    "revision": 2,
    "type": "goalkeeper",
    "realWorldTime": "2026-01-22T21:10:53.30284",
    "updatedTime": "2026-01-22T20:10:53.722639",
    "homeTeam": {
      "teamId": "OHK",
      "teamName": "Örebro Hockey",
      "teamCode": "ÖRE",
      "score": 0
    },
    "awayTeam": {
      "teamId": "VLH",
      "teamName": "Växjö Lakers",
      "teamCode": "VLH",
      "score": 1
    },
    "eventTeam": {
      "teamId": "VLH",
      "place": "away",
      "teamCode": "VLH",
      "teamName": "Växjö Lakers"
    },
    "player": {
      "playerId": "3550",
      "firstName": "Adam",
      "familyName": "Åhman",
      "jerseyToday": "70"
    },
    "isEntering": false,
    "gameUuid": "e6uyyogl05"
  },
  {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "eventId": 121,
    "eventUuid": "0faf8cf9-a99c-5e1a-b46d-f764d3ff6189",
    "round": 38,
    "gameType": "Elitserien",
    "arena": "Behrn Arena",
    "attendance": 5078,
    "startDateAndTime": "2026-01-22T19:00:00",
    "period": 4,
    "time": "01:46",
    "gameState": "GameEnded",
    "revision": 2,
    "type": "goal",
    "realWorldTime": "2026-01-22T21:09:49.553916",
    "updatedTime": "2026-01-22T20:10:47.916826",
    "homeTeam": {
      "teamId": "OHK",
      "teamName": "Örebro Hockey",
      "teamCode": "ÖRE",
      "score": 0
    },
    "awayTeam": {
      "teamId": "VLH",
      "teamName": "Växjö Lakers",
      "teamCode": "VLH",
      "score": 1
    },
    "eventTeam": {
      "teamId": "VLH",
      "place": "away",
      "teamCode": "VLH",
      "teamName": "Växjö Lakers"
    },
    "player": {
      "playerId": "6160",
      "firstName": "Dylan",
      "familyName": "McLaughlin",
      "jerseyToday": "13",
      "statistics": [
        { "key": "G", "value": "9" },
        { "key": "A", "value": "11" }
      ]
    },
    "locationX": 32,
    "locationY": 51,
    "homeGoals": 0,
    "awayGoals": 1,
    "goalSection": 7,
    "isPenaltyShot": false,
    "isEmptyNetGoal": false,
    "pop": [
      { "playerId": "6850", "firstName": "Brogan", "familyName": "Rafferty", "jerseyToday": "11" },
      { "playerId": "6160", "firstName": "Dylan", "familyName": "McLaughlin", "jerseyToday": "13" }
    ],
    "nep": [
      { "playerId": "920", "firstName": "Jhonas", "familyName": "Enroth", "jerseyToday": "1" },
      { "playerId": "6750", "firstName": "Luke", "familyName": "Martin", "jerseyToday": "7" }
    ],
    "assists": {
      "first": {
        "playerId": "4058",
        "firstName": "Karl",
        "familyName": "Henriksson",
        "jerseyToday": "24",
        "statistics": [
          { "key": "G", "value": "9" },
          { "key": "A", "value": "5" }
        ]
      },
      "second": {
        "playerId": "3550",
        "firstName": "Adam",
        "familyName": "Åhman",
        "jerseyToday": "70",
        "statistics": [
          { "key": "G", "value": "0" },
          { "key": "A", "value": "2" }
        ]
      }
    },
    "goalStatus": "EQ",
    "gameUuid": "e6uyyogl05"
  },
  {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "eventId": 120,
    "eventUuid": "a5f31bb4-a02a-58c6-abc3-fdbbe00f1752",
    "round": 38,
    "gameType": "Elitserien",
    "arena": "Behrn Arena",
    "attendance": 5078,
    "startDateAndTime": "2026-01-22T19:00:00",
    "period": 4,
    "time": "01:38",
    "gameState": "OverTime",
    "revision": 1,
    "type": "shot",
    "realWorldTime": "2026-01-22T21:09:39.530774",
    "updatedTime": "2026-01-22T20:09:42.095253",
    "homeTeam": {
      "teamId": "OHK",
      "teamName": "Örebro Hockey",
      "teamCode": "ÖRE",
      "score": 0
    },
    "awayTeam": {
      "teamId": "VLH",
      "teamName": "Växjö Lakers",
      "teamCode": "VLH",
      "score": 0
    },
    "eventTeam": {
      "teamId": "OHK",
      "place": "home",
      "teamCode": "ÖRE",
      "teamName": "Örebro Hockey"
    },
    "player": {
      "playerId": "3246",
      "firstName": "William",
      "familyName": "Wikman",
      "jerseyToday": "17"
    },
    "locationX": 121,
    "locationY": 61,
    "goalSection": 3,
    "isPenaltyShot": false,
    "gameUuid": "e6uyyogl05"
  },
  {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "eventId": 19,
    "eventUuid": "724b5754-3ca5-5ce0-a67c-6d313c390b01",
    "round": 38,
    "gameType": "Elitserien",
    "arena": "Behrn Arena",
    "attendance": 0,
    "startDateAndTime": "2026-01-22T19:00:00",
    "period": 1,
    "time": "10:31",
    "gameState": "Ongoing",
    "revision": 2,
    "type": "penalty",
    "realWorldTime": "2026-01-22T19:14:48.836242",
    "updatedTime": "2026-01-22T18:18:46.534456",
    "homeTeam": {
      "teamId": "OHK",
      "teamName": "Örebro Hockey",
      "teamCode": "ÖRE",
      "score": 0
    },
    "awayTeam": {
      "teamId": "VLH",
      "teamName": "Växjö Lakers",
      "teamCode": "VLH",
      "score": 0
    },
    "eventTeam": {
      "teamId": "VLH",
      "place": "away",
      "teamCode": "VLH",
      "teamName": "Växjö Lakers"
    },
    "player": {
      "playerId": "1964",
      "firstName": "Dennis",
      "familyName": "Rasmussen",
      "jerseyToday": "40"
    },
    "variant": {
      "shortName": "Minor",
      "minorTime": "2",
      "doubleMinorTime": "0",
      "benchTime": "0",
      "majorTime": "0",
      "misconductTime": "0",
      "gMTime": "0",
      "mPTime": "0",
      "description": "2 min"
    },
    "offence": "SLASH",
    "didRenderInPenaltyShot": false,
    "gameUuid": "e6uyyogl05"
  },
  {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "period": 4,
    "started": true,
    "startedAt": "2026-01-22T21:06:58.040Z",
    "finished": true,
    "finishedAt": "2026-01-22T21:10:44.008Z",
    "realWorldTime": "2026-01-22T21:10:44.80227",
    "gameUuid": "e6uyyogl05",
    "type": "period"
  }
]
```
