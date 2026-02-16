# SHL's API

The apis have been found from scraping or reverse engineering. Not offical documentation.

Base path: `https://www.shl.se/api`

## /sports-v2/upcoming-live-games

Request to fetch the IDs for all ongoing or upcoming live games.

**Request**
```
GET /api/sports-v2/upcoming-live-games HTTP/2
```

**Response**
A json array containg objects. Each object containing two IDs for one game.

`gameUuid`: Unique identifier for an ongoing or upcoming live game.
`gameExtId`: Unknown ID.

**Example Response**
```
[
  {
    "gameUuid": "bqsih1fsv5",
    "gameExtId": "22260"
  },
  {
    "gameUuid": "c8aie4zrqw",
    "gameExtId": "22259"
  }
]
```

## GET /sports-v2/game-info/<gameUuid>

**Request**
```
GET /api/sports-v2/game-info/<gameUuid> HTTP/2
```

**Response**
Game metadata, including game info plus home/away team details.

**Example Response**
```
{
  "instanceContext": {
    "siteTeamIsInGame": true,
    "siteTeamIsHomeTeam": true,
    "siteTeamIsAwayTeam": true
  },
  "gameInfo": {
    "gameUuid": "hx5yads5ov",
    "extId": "22285",
    "startDateTime": "2026-01-31T17:00:00.000Z",
    "arenaName": "Vida Arena",
    "state": "pre_game",
    "overtime": false,
    "shootout": false,
    "seriesCode": "SHL",
    "seriesName": "SHL",
    "seriesDisplayName": "SHL"
  },
  "homeTeam": {
    "names": {
      "code": "VLH",
      "short": "Växjö",
      "long": "Växjö Lakers",
      "full": "Växjö Lakers",
      "codeSite": "VLH",
      "shortSite": "Växjö Lakers",
      "fullSite": "Växjö Lakers",
      "longSite": "Växjö Lakers"
    },
    "uuid": "fe02-fe02mf1FN",
    "instanceId": "vlh1_vlh",
    "foundedOn": "1997",
    "address": "Storgatan 86\r\n352 46 Växjö",
    "email": "kansli@vaxjolakers.se",
    "icon": "https://sportality.cdn.s8y.se/team-logos/vlh1_vlh.svg",
    "score": ""
  },
  "awayTeam": {
    "names": {
      "code": "LIF",
      "short": "Leksand",
      "long": "Leksands IF",
      "full": "Leksands Idrottsförening",
      "codeSite": "LIF",
      "shortSite": "Leksand",
      "longSite": "Leksands IF Herr",
      "fullSite": "Leksands Idrottsförening"
    },
    "uuid": "9541-95418PpkP",
    "instanceId": "lif1_lif",
    "foundedOn": "1919",
    "address": "Postadress: Box 118, 793 23 Leksand\r\nBesöksadress: Arenavägen 9, 793 35 Leksand",
    "email": "Se personalsida",
    "icon": "https://sportality.cdn.s8y.se/team-logos/lif1_lif.svg",
    "score": ""
  },
  "ssgtUuid": "iuzqg7dqk9",
  "seriesUuid": "qQ9-bb0bzEWUk"
}
```

## GET /gameday/team-stats/<gameUuid>

**Request**
```
GET /api/gameday/team-stats/<gameUuid> HTTP/2
```

If the object time is empty `time: {}`. The match has not yet begun.

| Key              | Full Name            | Definition / Logic                                               |
| ---------------- | -------------------- | ---------------------------------------------------------------- |
| **G**            | Goals                | Total goals scored by the team in the specified period/total.    |
| **PIM**          | Penalties In Minutes | Total cumulative minutes for all penalties served.               |
| **FOW**          | Face-offs Won        | Total number of successful face-off wins.                        |
| **SOG**          | Shots On Goal        | Shots that hit the net (resulting in either a save or a goal).   |
| **SPG**          | Shots Past Goal      | Shots that missed the net entirely (wide or over).               |
| **PPSOG**        | Power Play SOG       | Shots on goal taken specifically during a Power Play.            |
| **Saves**        | Saves                | Number of shots stopped by the goaltender.                       |
| **GA**           | Goals Against        | Total goals conceded to the opponent.                            |
| **SavesPerShot** | Save Percentage      | The ratio of saves to total shots on goal (e.g., 1 = 100%).      |
| **PP_perc**      | Power Play %         | Efficiency rating for Power Play opportunities.                  |
| **SH_perc**      | Short-handed %       | Efficiency rating for Penalty Killing (Short-handed) situations. |
| **PPG**          | Power Play Goals     | Goals scored while the team had a man advantage.                 |
| **SHG**          | Short-handed Goals   | Goals scored while the team was playing with fewer players.      |
| **PPGA**         | Power Play GA        | Power Play goals conceded (while being short-handed).            |
| **SHGA**         | Short-handed GA      | Short-handed goals conceded (while being on a Power Play).       |
| **NumPP**        | Number of PP         | Total count of Power Play opportunities awarded to the team.     |
| **NumSH**        | Number of SH         | Total count of Short-handed (Penalty Kill) situations faced.     |
| **Hits**         | Hits                 | Number of recorded physical body checks.                         |
| **BkS**          | Blocked Shots        | Shots by the opponent that were blocked by a skater.             |
| **SiBk**         | Shots into Block     | Shots by this team that were blocked by an opposing skater.      |

**Response**
An object for each ongoing or done period with statistics.
Note: Before puck drop (or when the game start is not close), the endpoint may return a 200 with a non-JSON body.
**Example Response**
```
{
  "home": {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "place": "home",
    "score": 0,
    "teamId": "OHK",
    "teamName": "Örebro Hockey",
    "teamCode": "ÖRE",
    "statistics": [
      {
        "period": 0,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 2
          },
          {
            "key": "FOW",
            "value": 17
          },
          {
            "key": "SOG",
            "value": 19
          },
          {
            "key": "SPG",
            "value": 9
          },
          {
            "key": "PPSOG",
            "value": 6
          },
          {
            "key": "Saves",
            "value": 14
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 0
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 3
          },
          {
            "key": "NumSH",
            "value": 0
          },
          {
            "key": "Hits",
            "value": 10
          },
          {
            "key": "BkS",
            "value": 7
          },
          {
            "key": "SiBk",
            "value": 19
          }
        ]
      },
      {
        "period": 1,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 0
          },
          {
            "key": "FOW",
            "value": 13
          },
          {
            "key": "SOG",
            "value": 9
          },
          {
            "key": "SPG",
            "value": 7
          },
          {
            "key": "PPSOG",
            "value": 3
          },
          {
            "key": "Saves",
            "value": 5
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 0
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 2
          },
          {
            "key": "NumSH",
            "value": 0
          },
          {
            "key": "Hits",
            "value": 5
          },
          {
            "key": "BkS",
            "value": 4
          },
          {
            "key": "SiBk",
            "value": 12
          }
        ]
      },
      {
        "period": 2,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 2
          },
          {
            "key": "FOW",
            "value": 4
          },
          {
            "key": "SOG",
            "value": 10
          },
          {
            "key": "SPG",
            "value": 2
          },
          {
            "key": "PPSOG",
            "value": 3
          },
          {
            "key": "Saves",
            "value": 9
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 0
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 1
          },
          {
            "key": "NumSH",
            "value": 0
          },
          {
            "key": "Hits",
            "value": 5
          },
          {
            "key": "BkS",
            "value": 3
          },
          {
            "key": "SiBk",
            "value": 7
          }
        ]
      }
    ],
    "gameUuid": "e6uyyogl05"
  },
  "away": {
    "gameSourceId": "20260122-OHK-VLH",
    "gameId": 22264,
    "place": "away",
    "score": 0,
    "teamId": "VLH",
    "teamName": "Växjö Lakers",
    "teamCode": "VLH",
    "statistics": [
      {
        "period": 0,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 8
          },
          {
            "key": "FOW",
            "value": 11
          },
          {
            "key": "SOG",
            "value": 14
          },
          {
            "key": "SPG",
            "value": 6
          },
          {
            "key": "PPSOG",
            "value": 0
          },
          {
            "key": "Saves",
            "value": 19
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 1
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 0
          },
          {
            "key": "NumSH",
            "value": 3
          },
          {
            "key": "Hits",
            "value": 9
          },
          {
            "key": "BkS",
            "value": 19
          },
          {
            "key": "SiBk",
            "value": 7
          }
        ]
      },
      {
        "period": 1,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 6
          },
          {
            "key": "FOW",
            "value": 5
          },
          {
            "key": "SOG",
            "value": 5
          },
          {
            "key": "SPG",
            "value": 1
          },
          {
            "key": "PPSOG",
            "value": 0
          },
          {
            "key": "Saves",
            "value": 9
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 1
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 0
          },
          {
            "key": "NumSH",
            "value": 2
          },
          {
            "key": "Hits",
            "value": 4
          },
          {
            "key": "BkS",
            "value": 12
          },
          {
            "key": "SiBk",
            "value": 4
          }
        ]
      },
      {
        "period": 2,
        "parsedTotalStatistics": [
          {
            "key": "G",
            "value": 0
          },
          {
            "key": "PIM",
            "value": 2
          },
          {
            "key": "FOW",
            "value": 6
          },
          {
            "key": "SOG",
            "value": 9
          },
          {
            "key": "SPG",
            "value": 5
          },
          {
            "key": "PPSOG",
            "value": 0
          },
          {
            "key": "Saves",
            "value": 10
          },
          {
            "key": "GA",
            "value": 0
          },
          {
            "key": "SavesPerShot",
            "value": 1
          },
          {
            "key": "PP_perc",
            "value": 0
          },
          {
            "key": "SH_perc",
            "value": 1
          },
          {
            "key": "PPG",
            "value": 0
          },
          {
            "key": "SHGA",
            "value": 0
          },
          {
            "key": "SHG",
            "value": 0
          },
          {
            "key": "PPGA",
            "value": 0
          },
          {
            "key": "NumPP",
            "value": 0
          },
          {
            "key": "NumSH",
            "value": 1
          },
          {
            "key": "Hits",
            "value": 5
          },
          {
            "key": "BkS",
            "value": 7
          },
          {
            "key": "SiBk",
            "value": 3
          }
        ]
      }
    ],
    "gameUuid": "e6uyyogl05"
  }
}
```

## GET /gameday/play-by-play/<gameUuid>

**Request**
```
GET /api/gameday/play-by-play/<gameUuid> HTTP/2
```

**Response**
JSON array of play-by-play events for the game (shots, goals, penalties, period start/end, goalkeeper swaps).

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


## /gameday/game-overview/bqsih1fsv5

Game Overview om ett game är fortfarande igång samt vilket period.
