# Background Tracking
App that tracks animation background painting progress.

## Prerequisites

### Utilities

- **pip** installed with `sudo easy_install pip` or follow [these instructions](https://gist.github.com/haircut/14705555d58432a5f01f9188006a04ed) for installing `pip` without admin priviledges.
- **virtualenv** installed with `pip install virtualenv`.

### Virtual environment

Start the virtual environment with:

```commandline
$ source ./venv/bin/activate
```

### Libraries

After invoking the virtual env, install 3rd-party packages with:

```commandline
pip install -r requirements-to-freeze.txt --upgrade
```

If any libraries are updated, the changes can be saved to `requirements.txt`:

```commandline
pip freeze > requirements.txt
```

## Configuration

### Database

The database for the project is currently a local sqlite3 file: `./bgs.db`

It needs to be copied into the local working directory.

## Starting the server

```commandline
python run.py
```

A message to the effect that the server is `Running on http://127.0.0.1:5000/` should display.

Now connect to the server in a browser using that address.
