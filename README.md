# Netflix “Trending Titles” API Challenge

Welcome – here’s a self‑contained exercise that lets you demonstrate back‑end design, data‑access skills.

## 1 · Background

StreamScout is a proprietary service used by editorial analysts and media research partners to surface Netflix viewing trends, specifically tailored for journalistic and critical reporting. Two screens drive almost all traffic:

1. **Top‑10 Explorer** – shows the current Top‑10 titles (movies and TV‑show seasons) for any language locale.

2. **Engagement Timeline** – given a title, shows how many hours it was viewed each week and how its rank moved over time.

An analyst dataset (based on Netflix’s public Weekly Top 10 and Engagement Report) has already been loaded into MySQL for you.

| table        | purpose                          | key columns                                                                                                  |
| ------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| movie        | movie metadata                   | id, title, locale, release_date, runtime                                                                     |
| tv_show      | series‑level metadata            | id, title, locale                                                                                            |
| season       | season metadata                  | id, tv_show_id, season_number, release_date, runtime                                                         |
| view_summary | pre‑aggregated viewing snapshots | duration (WEEKLY / SEMI_ANNUALLY), start_date, end_date, view_rank, hours_viewed, views, movie_id, season_id |

This repo contains a docker-compose file which can spin up a local MySQL database containing all the data relevant to this assignment, which can be spun up using the command:

```sh
$ docker compose up
```

## 2 · Your task

Build a small back‑end service that exposes the two HTTP endpoints.

### 2.1 Endpoint A – Top 10 list

```
GET /v1/top10
```

| Query parameter | Required | Example                               | Notes                                                                      |
| --------------- | -------- | ------------------------------------- | -------------------------------------------------------------------------- |
| `locale`        | yes      | `en`                                  | Language/market of interest                                                |
| `window`        | no       | `WEEKLY` (default) / `SEMI_ANNUALLY`  |                                                                            |
| `as_of`         | no       | `2025‑05‑12`                          | ISO date – if omitted, use the latest date available for the chosen window |
| `include`       | no       | `movie` / `season` / `both` (default) |                                                                            |

**Response** (JSON array ordered by view_rank):

```json
[
  {
    "id": 123,
    "type": "movie",              // "movie" or "season"
    "title": "Damsel",
    "view_rank": 1,
    "hours_viewed": 83472000,
    "views": 47000000,
    "runtime": 108
  },
  … up to 10 objects …
]
```

### 2.2 Endpoint B – Engagement timeline

```
GET /v1/title/{id}/engagement
```

| Query parameter | Required | Example      | Notes                                                  |
| --------------- | -------- | ------------ | ------------------------------------------------------ |
| `from`          | no       | `2024‑01‑01` | Earliest week to return (defaults to first week in DB) |
| `to`            | no       | `2025‑06‑02` | Latest week to return (defaults to last week in DB)    |

**Response** (weekly buckets, ascending date):

```json
{
  "id": 567,
  "type": "season",
  "title": "Bridgerton • S2",
  "timeline": [
    {
      "start_date": "2025‑04‑21",
      "hours_viewed": 32800000,
      "views": 18200000,
      "view_rank": 3
    },
    {
      "start_date": "2025‑04‑28",
      "hours_viewed": 21000000,
      "views": 12000000,
      "view_rank": 7
    }
  ]
}
```

## 3 · What to ship

Write a **production-grade** backend service with the **best‑quality code you can** within a reasonable time‑box (we expect 4‑6 hours in total, but feel free to stop whenever you are happy with the result).

## 4 · Submission

Push your work to a public or private Git repository and share the link, or send us a zip/tarball. That’s it – we’ll run it, read the code, and take it from there.

Have fun – we’re looking forward to seeing your craftsmanship!
