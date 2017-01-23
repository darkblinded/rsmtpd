import socket
import targets.api
import logging
import docker
import requests
import sys


__name__ = "docker"


class Target(targets.api.Target):

    def __init__(self, regex, container, internal_port=25):
        """
        Creates a new docker target.
        Args:
            regex: Regular expression matching all rcpt addresses for which the
                mail should be forwarded
            container: Name or ID of the container
            internal_port: The port inside the container to which the SMTP
                connection should be established

        Returns:
            A new instance of Target
        """
        super(Target, self).__init__(regex)
        self._container = container
        self._internal_port = internal_port

        self.target_type = __name__

        self._logger = logging.getLogger(name="docker-target")

        self._client = docker.from_env()

    def get_ip(self):
        """Returns a string containing the target's IP address"""
        # raise NotImplementedError  # TODO
        return (self._client.inspect_container(self._container)
                ["NetworkSettings"]["Gateway"])

    def get_port(self):
        """Returns the target's port"""
        # raise NotImplementedError  # TODO
        return (int(self._client.inspect_container(self._container)
                ["NetworkSettings"]["Ports"]
                [str(self._internal_port) + "/tcp"][0]["HostPort"]))

    def get_instances(config):
        """
        Static method for generating instances from config.json
        Args:
            config: Dictionary representing config.json["targets"]["docker"]

        Returns:
            A list of DockerTargets containing a target for every entry
            in config.json["targets"]["docker"]
        """
        try:
            # Testing docker connectivity
            docker.from_env().containers()
        except Exception as e:
            cause = ""
            e.__cause__ = e
            try:
                raise e.__cause__ from e.__cause__.__context__
            except requests.exceptions.ConnectionError as e:
                try:
                    raise e.__cause__ from e.__cause__.__context__
                except requests.packages.urllib3.exceptions.ProtocolError as e:
                    try:
                        raise e.__cause__ from e.__cause__.__context__
                    except PermissionError as e:
                        cause = ("Permissions denied. Please run with docker "
                                 "privileges")
                    except Exception as e:
                        cause = ("Unknown protocol error " + str(e) +
                                 ". Please create an issue at "
                                 "https://github.com/darkblinded/rsmtpd/issues"
                                 "/new")
                except Exception as e:
                    cause = ("Unknown connection error " + str(e) +
                             ". Please create an issue at "
                             "https://github.com/darkblinded/rsmtpd/issues"
                             "/new")
            logging.getLogger(
                name=__name__ + "-target").critical(
                "Cannot connect to docker socket: " + cause)
            sys.exit(1)

        instances = []
        for item in config:
            # TODO Test if regex exists in config.json
            # --> Just forward to both and maybe add detection+warning later

            try:
                """Try parsing and validate range"""
                if (int(item["internal_port"]) < 0 or
                        int(item["internal_port"]) > 65535):
                    raise ValueError
            except ValueError:
                (self._logger
                 .error("Parsing error: \"{}\" is not a valid port!"
                        .format(item["internal_port"])))
                continue

            instances.append(Target(regex=item["regex"],
                                    container=item["container"],
                                    internal_port=item["internal_port"]))

        return instances

    def __str__(self):
        """Returns a string representing the target"""
        return "{}:{}".format(self._container, self._internal_port)
