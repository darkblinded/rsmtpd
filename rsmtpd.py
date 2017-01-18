import smtpd
import smtplib
import re
import logging
from targets import *


class RSMTPDServer(smtpd.SMTPServer):

    def __init__(self, config):
        super(RSMTPDServer, self).__init__(
            localaddr=(config["ip"], config["port"]),
            remoteaddr=None)

        self._logger = logging.getLogger(name="rsmtpd")

        self.config = config
        self.target_list = []

        # self.target_list.append(targets.target.Target.get_instances(
        #     config=self.config[targets.target.config_indentifier]))
        # self.target_list.append(targets.docker.DockerTarget.get_instances(
        #     config=self.config[targets.docker.config_indentifier]))

        # self.target_list.append(targets.target.Target.get_instances(
        #     config=self.config[targets.target.config_indentifier]))
        # self.target_list.append(targets.docker.Target.get_instances(
        #     config=self.cyonfig[targets.docker.config_indentifier]))

        # TODO Handle missing parts in config
        # TODO Auto-import
        self.target_list = (self.target_list + targets.hosts.Target
                            .get_instances(config=self.config["targets"][
                                    targets.hosts.config_indentifier]))

        self.target_list = (self.target_list + targets.docker.Target
                            .get_instances(config=self.config["targets"][
                                    targets.docker.config_indentifier]))

        self._logger.debug("Parsed the following hosts:")
        for item in self.target_list:
            self._logger.debug("{} - {} ({})".format(
                str(self.target_list.index(item)),
                str(item), item.target_type))

    def process_message(self, peer, mailfrom, rcpttos, data):
        """
        Implementation of smtpd's interface
        Args:

        Returns:

        """
        self._logger.info("Processing mail from {} to {}"
                          .format(mailfrom, rcpttos))
        accepted = False
        for target in self.target_list:
            for rcpt in rcpttos:
                if re.match(target.get_regex(), rcpt):
                    self._logger.debug("Got match for host {}"
                                       .format(str(target)))
                    server = smtplib.SMTP(host=target.get_ip(),
                                          port=target.get_port())
                    server.set_debuglevel(True)
                    try:
                        server.sendmail(mailfrom, [rcpt], data)
                    # TODO Handle connection problems
                    finally:
                        server.quit()

                    accepted = True

        if accepted:
            return None
        else:
            return "550 Requested action not taken: mailbox unavailable"
