# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`srpenergy` is an unofficial single-module Python client for scraping hourly energy usage data from SRP (Salt River Project, an Arizona utility) via their unofficial web API (`myaccount.srpnet.com/myaccountapi`). It is not an official SRP integration and there is no public API contract to rely on — the endpoints are the same ones the SRP customer web portal uses.

## Commands

```bash
# Install dev dependencies + editable package
python -m pip install -r requirements_dev.txt
pip install --editable .

# Run tests
python -m pytest tests
python -m pytest tests/test_client.py::test_name  # single test

# Run tests with coverage (mirrors CI)
python -m pytest --cov-report=xml --cov-report term-missing --cov=srpenergy tests/

# Lint / format (Ruff is the source of truth; flake8/pylint/bandit run via pre-commit too)
ruff check .                 # lint
ruff check --fix .           # auto-fix
ruff format --check .        # check formatting
ruff format .                # format (Black-compatible)
codespell .
rstcheck README.rst

# Pre-commit (runs codespell, ruff-check, ruff-format, shellcheck, rstcheck, bandit, pylint)
pre-commit run --all-files
pre-commit run <hook_id>     # run one hook, e.g. `pre-commit run bandit`

# Docs (Sphinx, from repo root)
cd docs && python -m sphinx -T -b html -d _build/doctrees -D language=en . _build/html
```

There is no separate `lint`/`test` script wrapper — use the commands above directly. `tox.ini` exists but targets old interpreters (py36-38) and is not the primary workflow; prefer the commands above.

Manually exercising a real account (not part of the automated test suite) is done via `quickstart_test.py`, which reads `SRP_BILLING_ACCOUNT`, `SRP_USER_NAME`, `SRP_PASSWORD` from a `.env` file (see `example.env`).

## Architecture

Everything lives in `srpenergy/client.py` — there is no package-internal module split. Two things live in that file:

1. **`get_rate(str_usage_time)`** — a pure function implementing SRP's time-of-use (TOU) pricing table (summer/peak-summer/winter windows, weekday peak hours, the six observed holidays). Used only when `usage(..., is_tou=True)`. This encodes a specific SRP price plan (`E-26`, see the sheet linked in `README.rst`) as of the docstring's writing — if SRP changes rates, this table needs a manual update, since nothing fetches it dynamically.

2. **`SrpEnergyClient`** — the client class. `usage()` performs a **3-step scripted session against the SRP customer portal**, not a documented REST API:
   - `POST login/authorize` with username/password to authenticate the `requests.Session`.
   - `GET login/antiforgerytoken` to obtain an `xsrf-token` cookie (required for the next call).
   - `GET usage/hourlydetail` with `billaccount`/`beginDate`/`endDate` params and the XSRF token echoed back as an `x-xsrf-token` header.

   Because this hits a live consumer web app rather than a stable API, the client sends full browser-like headers (`BROWSER_HEADERS`, including `User-Agent`/`Referer`) to reduce the chance of being blocked, and `_check_response()` specifically detects HTTP 403 (Cloudflare/SRP bot-blocking) and raises a distinguishable `SrpEnergyError` rather than a generic HTTP error. When touching request/session logic, preserve this distinction — tests assert on it (see `tests/common.py`'s `MOCK_CLOUDFLARE_RESPONSE_TEXT`).

   `usage()` also normalizes SRP's response quirks:
   - Non-TOU customers get `totalKwh`/`totalCost` directly from the API; **EZ-3 plan customers get 0 for both**, so the client falls back to summing the `onPeak`/`offPeak`/`shoulder`/`superOffPeak` components.
   - TOU customers never get `totalKwh`/`totalCost` from the API at all — the client recomputes usage/cost per row using `get_rate()`.

`validate()` only performs step 1 (auth) and returns a bool, swallowing all exceptions — it's meant as a lightweight credential check, not for diagnosing failures.

## Testing conventions

- Tests mock `requests.Session.get`/`.post` directly (`tests/common.py`'s `PATCH_GET`/`PATCH_POST` = `"srpenergy.client.requests.Session.get"`/`.post`), not the `requests` module-level functions — the client uses `with requests.Session() as session`.
- `tests/common.py::get_mock_requests(routes, ...)` builds a `side_effect` for the GET mock: `routes` is a list of `(pattern, response)` tuples matched against the URL, `beginDate`, or `billaccount`; unmatched calls raise loudly instead of silently returning `None`, which is intentional — keep that behavior when extending it.
- Fixture-style mock data (`MOCK_LOGIN_RESPONSE`, `MOCK_USAGE_RESPONSE`, `MOCK_ANTI_FORGERY_RESPONSE_COOKIES`, `MOCK_CLOUDFLARE_RESPONSE_TEXT`, etc.) lives in `tests/common.py` and is shared across `tests/test_client.py`, `tests/test_rate.py`, and `tests/test_time_of_use.py` — add new shared fixtures there rather than duplicating them per test file.
- `ruff`'s per-file-ignores already relax `S101`/`S105`/`S106`/docstring rules for `*_test.py` and `test_*.py`, so asserts and dummy hardcoded test credentials are fine as-is.

## Style (enforced by Ruff, see `pyproject.toml`)

- f-strings everywhere, **except** logging calls, which use `%`-style formatting so the message isn't formatted when the log level suppresses it (e.g. `_LOGGER.info("... %s at %s", a, b)`).
- numpy-style docstrings; full-sentence comments ending in a period.
- Import order is isort-enforced (`ruff check --fix .` fixes it automatically); `srpenergy`/`tests` are first-party, `tests` imports are force-separated from other first-party imports.
- Constants and dict/list contents should be alphabetically ordered.

## Releasing

Version is duplicated in three places and must be bumped together: `srpenergy/__init__.py`, `pyproject.toml`, `docs/conf.py`. Release flow is: bump version → commit → `git tag -a X.Y.Z -m "X.Y.Z"` → push tags → create a GitHub Release (auto-generated notes) → `python -m build` → `twine check dist/*` → upload to TestPyPI first, verify, then upload to PyPI proper.
