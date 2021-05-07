# Gandi Dynamic Live DNS

Dynamically update an A record on Gandi's LiveDNS system to reflect the current public IP address where this script is running.

## Usage

1. `pip install poetry`
2. `python -m poetry install`
3. Add the correct values into `.env.example` and rename it to `.env`
4. Add to your [crontab](https://crontab-generator.org/) to run periodically

For Example:

`*/15 * * * * python -m poetry run /path/to/script/livedns.py >/dev/null 2>&1`

_if you hate poetry then the only deps you need are:_

- _requests_
- _python-dotenv_
