import click
import json
import logging
import os
import asyncore
import sys
from rsmtpd import RSMTPDServer


@click.command()
@click.option("--config", help="Path to config.json", type=click.File('r'),
              default="./config.json")
@click.option("--ip", help="IP to which server will bind")
@click.option("--port", type=click.INT, help="Port to which server will bind")
@click.option("--loglevel", help="Loglevel for commandline output",
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL']))
def main(config, **kwargs):
    config_file = config
    try:
        config = json.load(config_file)
    except json.decoder.JSONDecodeError:
        click.echo(message="Error: Parsing config failed: Invalid JSON syntax", err=True)
        sys.exit(1)
    config_file.close()

    config = validate_config(config, kwargs)

    logging.basicConfig(level=config["loglevel"],
                        datefmt='%H:%M:%S',
                        format='%(asctime)s.%(msecs)03d %(name)s %(levelname' +
                        ')s %(message)s')
    logger = logging.getLogger(name="init")
    logger.info("Starting rsmptd...")

    server = RSMTPDServer(config)

    logger.info("Listening on {}:{}".format(config["ip"], config["port"]))

    asyncore.loop()

    logger.info("rsmtpd closed.")


def validate_config(config, parameters):
    if "targets" not in config or len(config["targets"]) == 0:
        click.echo("No targets configured. Exiting...")
        sys.exit(0)

    if parameters["ip"] is not None:
        config["ip"] = parameters["ip"]
    if "ip" not in config:
        config["ip"] = "127.0.0.1"

    if parameters["port"] is not None:
        config["port"] = parameters["port"]
    if "port" not in config:
        config["port"] = 25
    try:
        config["port"] = int(config["port"])
        if config["port"] < 0 or config["port"] > 65535:
            raise ValueError
    except ValueError:
        config["port"] = 25

    if parameters["loglevel"] is not None:
        config["loglevel"] = parameters["loglevel"]
    if ("loglevel" not in config or config["loglevel"] not in
            ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
        config["loglevel"] = "INFO"

    return config

if __name__ == '__main__':
    main(auto_envvar_prefix='RSMTPD')
