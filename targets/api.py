
config_indentifier = NotImplemented


class Target(object):

    def __init__(self, regex):
        """
        Creates a new target.
        This method should be overloaded in the child class to add additional
        parameters.  The method should only be used by the child's
        get_instances() method.
        Args:
            regex: Regular expression matching all rcpt addresses for which the
                mail should be forwarded

        Returns:
            A new instance of Target
        """
        self._regex = regex
        self.target_type = NotImplemented

    def get_regex(self):
        """Returns the target's regex"""
        return self._regex

    def get_ip(self):
        """Returns a string containing the target's IP address"""
        raise NotImplementedError

    def get_port(self):
        """Returns the target's port"""
        raise NotImplementedError

    def get_instances(config):
        """
        Static method for generating instances from config.json
        Args:
            config: Dictionary representing config.json["targets"][<MODULE>]

        Returns:
            A list of Targets containing a target for every entry
            in config.json["targets"][<MODULE>]
        """
        raise NotImplementedError

    # def __str__(self):
    #     """Returns a string representing the target"""
    #     raise NotImplementedError
