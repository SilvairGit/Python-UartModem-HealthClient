import re
import sys


class HealthClientCli(object):
    """ Health Client CLI """

    def __init__(self, console_out, health_client, prompt="> "):
        """ Initialize CLI.

        :param  console_out:   ConsoleOut, Console output interface
        :param  health_client: HealthClient, Health Client instance
        :return                None
        """
        self._console_out = console_out
        self._cmds = {
            "q": self._quit,
            "quit": self._quit,
            "a": self._attention,
            "attention": self._attention,
            "f": self._fault,
            "fault": self._fault,
            "p": self._period,
            "period": self._period,
            "h": self._help,
            "help": self._help
        }

        self._health_client = health_client
        self._prompt = prompt

    def _quit(self, args):
        """ Exit from application.

        :param  args: str, to be ignored
        :return       None
        """
        sys.exit(0)

    def _help(self, args):
        self._console_out.print_standard_message("Help:")
        self._console_out.print_standard_message("\t[a]ttention - commands for set and get attention")
        self._console_out.print_standard_message("\t[f]ault - commands for get, clear and run tests")
        self._console_out.print_standard_message("\t[p]eriod - commands for set and get Fast Period Divider")
        self._console_out.print_standard_message("\t[q]uit - exit from CLI")
        self._console_out.print_standard_message("")
        self._console_out.print_standard_message("Note: parameters that ends with 'u' e.g. 'setu', 'clearu', ...")
        self._console_out.print_standard_message("      are unacknowledged.")

    def _attention_set_usage(self, cmd):
        self._console_out.print_standard_message("Usage: attention {} <attention_s>".format(cmd))

    def _attention(self, args):
        if not args:
            self._console_out.print_standard_message("Draw attention on the devices in network.\nUsage: attention [get|set|setu] <args>")
            return

        cmd = args[0]
        args = args[1:]

        try:
            if cmd == "get":
                self._health_client.send_attention_get()

            elif cmd == "set":
                if len(args) < 1:
                    self._attention_set_usage(cmd)
                    return
                else:
                    self._health_client.send_attention_set(args[0])

            elif cmd == "setu":
                if len(args) < 1:
                    self._attention_set_usage(cmd)
                    return
                else:
                    self._health_client.send_attention_set(args[0], unack=True)

            else:
                self._console_out.print_standard_message("Command {} not supported!".format(cmd))

        except (OverflowError, ValueError):
            self._console_out.print_error_message("Error: Invalid value!")
            return

    def _fault_get_usage(self, cmd):
        self._console_out.print_standard_message("Usage: fault {} 0x<company_id>".format(cmd))

    def _fault_clear_usage(self, cmd):
        self._console_out.print_standard_message("Usage: fault {} 0x<company_id>".format(cmd))

    def _fault_test_usage(self, cmd):
        self._console_out.print_standard_message("Usage: fault {} 0x<company_id> <test_id>".format(cmd))

    def _fault(self, args):
        if not args:
            self._console_out.print_standard_message("Clear, get registered faults or perform test.\nUsage: fault [get|clear|clearu|test|testu] <args>")
            return

        cmd = args[0]
        args = args[1:]

        try:
            if cmd == "get":
                if len(args) < 1:
                    self._fault_get_usage(cmd)
                    return
                else:
                    self._health_client.send_fault_get(args[0])

            elif cmd == "clear":
                if len(args) < 1:
                    self._fault_clear_usage(cmd)
                    return
                else:
                    self._health_client.send_fault_clear(args[0])

            elif cmd == "clearu":
                if len(args) < 1:
                    self._fault_clear_usage(cmd)
                    return
                else:
                    self._health_client.send_fault_clear(args[0], unack=True)

            elif cmd == "test":
                if len(args) < 2:
                    self._fault_test_usage(cmd)
                    return
                else:
                    self._health_client.send_fault_test(args[0], args[1])

            elif cmd == "testu":
                if len(args) < 2:
                    self._fault_test_usage(cmd)
                    return
                else:
                    self._health_client.send_fault_test(args[0], args[1], unack=True)

            else:
                self._console_out.print_standard_message("Command {} not supported!".format(cmd))

        except (OverflowError, ValueError):
            self._console_out.print_error_message("Error: Invalid value!")
            return

    def _period_set_usage(self, cmd):
        self._console_out.print_standard_message("Usage: period {} <fast_period_divider>".format(cmd))

    def _period(self, args):
        if not args:
            self._console_out.print_standard_message("Set or get Fast Period Divisor.\nUsage: period [get|set|setu] <args>")
            return

        cmd = args[0]
        args = args[1:]

        try:
            if cmd == "get":
                self._health_client.send_period_get()

            elif cmd == "set":
                if len(args) < 1:
                    self._period_set_usage(cmd)
                    return
                else:
                    self._health_client.send_period_set(args[0])

            elif cmd == "setu":
                if len(args) < 1:
                    self._period_set_usage(cmd)
                    return
                else:
                    self._health_client.send_period_set(args[0], unack=True)
                    
            else:
                self._console_out.print_standard_message("Command {} not supported!".format(cmd))
        
        except (OverflowError, ValueError):
            self._console_out.print_error_message("Error: Invalid value!")
            return

    def process_line(self, line):
        """ Process single line

        :param  line: str, line with command and arguments.
        :return       None
        """
        if not line:
            return

        line = re.sub('\s+', " ", line).strip()
        args = line.split()

        cmd = args[0]
        args = args[1:]

        try:
            func = self._cmds[cmd]
        except KeyError as err:
            self._console_out.print_standard_message("Command {} not supported!".format(err))
            return

        func(args)

    def run(self):
        """ Run main loop.

        :return None
        """
        while True:
            self.process_line(input(self._prompt))
