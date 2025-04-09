# REPLAY

replay :- replay.

This replays `urenlopen` from previous editions.
It implements a mockup ronny that sends out realistic data from previous editions.

### Requirements

Ronny dumps from a previous edition are required, these can be downloaded from [https://dataset.12urenloop.be](https://dataset.12urenloop.be).

### Setup

1. Put the ronny01.json, ronny02.json, ... in the dumps directory.
2. Setup with or without docker (see next section)
3. Make sure the environment variables in the compose or the `.env` file are correct.
    - `API_URL`: The url that points to the replay emulator, this is required for telraam to reach the 'fake' ronny's. 
      REPLAY directly connects to the telraam database and changes the station urls to `API_URL` as base path.
    - `START_TIME`: Unix timestamp of when the replay should start. Default is the start of the 12urenloop in 2024.
4. Create the database (according to the env) and initialize it with the telraam dump for the correct edition.
    - [https://dataset.12urenloop.be](https://dataset.12urenloop.be) should also include a telraam.sql backup. For restoring see the [the telraam wiki](https://github.com/12urenloop/Telraam/wiki/Playing-with-the-database#exporting-the-database)


#### Setup With docker

There is a `docker-compose.yml` available that will run the replay application, a postgres database, telraam and loxsi.

#### Setup Without docker

The dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

Install all the dependencies with:

```console
uv sync
```

The environment can be activated with:

Activate the virtual environment with:

```console
source .venv/bin/activate
```

Create an `.env`:

```console
cp .env.sample .env
```

### Usage

There are currently 2 API endpoints available:

- `/{ronney0[1-9]}`: The endpoints where Telraam will connect to for each ronnny and can open a websocket. Path will be `/ronny01` for ronney1, `/ronney02` for ronney2,...
- `/reset`: Accepts a `time` datetime query parameter. REPLAY will change its internal clock to this datetime.
    - This will close al open ronny websockets from Telraam, and Telraam should then automatically retry and open new websockets for each ronny.
    - It also deletes the detection and lap records with a more recent timestamp from the telraam database.

See also `/docs` to get an interactive swagger dashboard.

DISCLAIMER: starting up or resetting into a datetime far into the event can take some time as it needs to catch up and send out all the previous detections.

TODO: the 10urenloop dumps from 2024 somehow do not work.

