# Contributing Guide

For now, this is a personal project and I don't have any plans to support it,
but of course, pull requests are always welcome. I might also start to support
the project if anybody else finds it useful. ;)

## Getting started with local development

These instructions assume that [Python 3](https://docs.python.org/3/) is
installed in your system and is available in your shell's command search path
as `python3`.

Once you have cloned this repository, create and activate a temporary virtual
environment, and then install the required dependencies as follows:

```
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.test.txt
```

You should now be able to start a Home Assistant instance for development via
`mkdir -p .homeassistant && python -m homeassistant -c .homeassistant --open-ui`.

During the onboarding process, you will be asked whether you want install
additional integrations. Click on the "... More" button and search for "jpdb.io"
to set this integration up.

## Running unit and integration tests locally

Ensure that the temporary virtual environment created for local development is
active, and then execute the command `pytest`.
