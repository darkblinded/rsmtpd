import socket
import targets.api
import logging


__name__ = "hosts"


class Target(targets.api.Target):

    def __init__(self, regex, host, port=25):
        """
        Creates a new host target.
        Args:
            regex: Regular expression matching all rcpt addresses for which the
                mail should be forwarded
            host: IP or hostname of the target host
            internal_port: The port to which the SMTP connection should be
                established

        Returns:
            A new instance of Target
        """
        super(Target, self).__init__(regex)
        self._host = host
        self._port = port

        self.target_type = __name__

        self._logger = logging.getLogger(name="host-target")

    def get_ip(self):
        """Returns the target's IP"""
        # TODO Handle unresolvable hosts
        return socket.gethostbyname(self._host)

    def get_port(self):
        """Returns the target's port"""
        return self._port

    def get_instances(config):
        """
        Static method for generating instances from config.json
        Args:
            config: Dictionary representing config.json["targets"]["hosts"]

        Returns:
            A list of Targets containing a target for every entry
            in config.json["targets"]["hosts"]
        """
        instances = []
        for item in config:
            # TODO Test if regex exists in config.json
            # --> Just forward to both and maybe add detection+warning later
            # TODO Test if host exists in config.json
            # --> Just forward to both and maybe add detection+warning later

            try:
                """Try parsing and validate range"""
                if int(item["port"]) < 0 or int(item["port"]) > 65535:
                    raise ValueError
                    self._logger.error("Invalid port in config: {}"
                                       .format(item["port"]))
            except ValueError:
                (self._logger
                 .error("Parsing error: \"{}\" is not a valid port!"
                        .format(item["port"])))
                continue

            instances.append(Target(regex=item["regex"],
                                    host=item["host"],
                                    port=int(item["port"])))

        return instances

    def __str__(self):
        """Returns a string representing the target"""
        return "{}:{}".format(self._host, self._port)
