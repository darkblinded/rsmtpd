import socket
import targets.api
import logging
import docker


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

    def get_ip():
        """Returns a string containing the target's IP address"""
        # raise NotImplementedError  # TODO
        print(client.containers.get(self._container)
              .attrs["NetworkSettings"]["Gateway"])

    def get_port():
        """Returns the target's port"""
        # raise NotImplementedError  # TODO
        print(int(client.containers.get(self._container)
                  .attrs["NetworkSettings"]["Ports"]
                  [str(internal_port) + "/tcp"][0]["HostPort"]))

    def get_instances(config):
        """
        Static method for generating instances from config.json
        Args:
            config: Dictionary representing config.json["targets"]["docker"]

        Returns:
            A list of DockerTargets containing a target for every entry
            in config.json["targets"]["docker"]
        """
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
