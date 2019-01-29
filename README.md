# Tadoº exporter for Prometheus

This software is a little [Python-based exporter](https://github.com/prometheus/client_python) that will expose data from your Tadoº devices in a [Prometheus](https://prometheus.io) readable format; this way, you can have your neat pretty graphics wherever you want and you won't be constrained to use the Tadoº app for Android/iOS. It relies on the wonderful [libtado](https://github.com/ekeih/libtado).

## How to run it

The app is meant to be run in a Docker container, but you can obviously run however you want. Since it's containters-first, the configuration is entirely done via environment variables.
There is a sample `.env.sample` file with the needed environment variables. Copy it to `.env` and customize it with your values.

To run it with docker:

```bash
$ sudo docker run --env-file .env vide/tado-exporter
```

If you want to run it without Python
```bash
$ source .env
$ python3 init.py
```

but I strongly recommend to put some process manager before it (be it systemd, supervisor etc) to restart it if it fails for any reason.

### Env vars explanation

From `.env.sample`:

```bash
TADO_EXPORTER_REFRESH_RATE=30
TADO_PASSWORD=your-tado-password
TADO_CLIENT_SECRET=a-long-random-string-you-should-get-from-inspecting-tado-website
TADO_EXPORTER_PORT=8000
# this is in seconds
TADO_USERNAME=your.tado@username
```

The only one that need explanation is `TADO_CLIENT_SECRET`: this is a secret token you have to extrapolate manually from the Tadoº website when logging in with your username and password. 

* Open your browser of choiche (Firefox)
* Fire up the developer tools
* Go to the Network tab
* Go to https://my.tado.com and login with your user and password
* Select the `POST token` request
* Go to the Params tab (form data)
* There you will find your `client_secret`

Since it's a form value that the login page is submitting it's probably some JS in the page that derives it somehow from your user/password. I will investigate further.

## Configure Prometheus scraper

This is a bit out of the scope of this README but it's just as simple as adding

```yaml
---
scrape_configs:
  - job_name: tado_exporter
    static_configs:
      - targets: ['tado-exporter:8000']
```

assuming, obviously, that `tado-exporter:8000` is a valid DNS name + port pointing to your tado-exporter instance.
