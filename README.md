# rsmtpd
A regex based reverse proxy for mail with docker support.

```
THIS PROJECT IS IN DEVELOPMENT STATE AND MAY THEREFORE BE UNSTABLE
```

## Installation
*rsmtpd* needs Python 3 and the following libraries:
* click
* docker

To install all dependencies run

```
pip install -r requirements.txt
```

## Running
You can run *rsmtpd* with the following command:

```
python main.py --config ./path/to/config.json
```

### Parameters
You can pass the following parameters to *rsmtpd*:

#### --config
Path to config.json, defaults to `./config.json`.

#### --ip
IP to which server will bind, defaults to `127.0.0.1`.

#### --port
Port to which server will bind, defaults to `25`.

#### --loglevel
Loglevel for commandline output, defaults to `INFO`.
Possible choices are: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Environment variables
You can also pass these parameters as environment variables in the form `RSMTPD_<PARAMETER>`.  To pass the config file as environment variable you would type:

```
RSMTPD_CONFIG=./path/to/config.json python main.py
```

## Configuration
To run *rsmtpd* you need a config file. The default location for this config file is `./config.json`.

The `config.json` contains some arguments

### General config
The general configuration consists of the three settings `ip`, `port` and `loglevel`.

```
{
    "ip": "127.0.0.1",
    "port": 1025,
    "loglevel": "DEBUG",
    "targets": {
        ...
        }
}
```

#### ip
IP to which server will bind, defaults to `127.0.0.1`.

#### port
Port to which server will bind, defaults to `25`.

#### loglevel
Loglevel for commandline output, defaults to `INFO`.
Possible choices are: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

These configurations can be overridden by parameters or environment variables.

### IP based forwarding
The IP based forwardings are configured in `targets` > `hosts`.  Each entry has the form

```
{
    "regex": "^.*@example.com$",
    "host": "mail.example.com",
    "port": "25"
}
```

If the `RCPT TO` of an incoming SMTP connection matches `regex`, *rsmtpd* will open a SMTP connection to `host`:`port` and forward the mail.

### Docker container based forwarding
Forwardings to docker containers are configured in `targets` > `docker`.  Each entry has the form

```
{
    "regex": "^.*@example.net$",
    "container": "dockermail",
    "internal_port": 25
}
```

If the `RCPT TO` of an incoming SMTP connection matches `regex`, *rsmtpd* will open a SMTP connection to the internal port `port` of the container `container` and forward the mail.

### Example config
```
{
    "ip": "127.0.0.1",
    "port": 1025,
    "loglevel": "DEBUG",
    "targets": {
        "hosts": [
            {
                "regex": "^.*@example.com$",
                "host": "mail.example.com",
                "port": "25"
            }
        ],
        "docker": [
            {
                "regex": "^.*@example.net$",
                "container": "dockermail",
                "internal_port": 25
            }
        ]
    }
}
```
