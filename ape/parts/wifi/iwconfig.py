
# The MIT License (MIT)
# 
# Copyright (c) 2013 Russell Nakamura
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# this package
from ape import BaseClass, ApeError
from ape.commoncode.eventtimer import EventTimer


class IwconfigQuery(BaseClass):
    """
    Queries ``iwconfig`` for information
    """
    def __init__(self, connection, interface='wlan0', interval=1):
        """
        IwconfigQuery constructor

        :param:

         - `interface`: name of the interface to query
         - `connection`: connection to the device to query
         - `interval`: seconds to wait before refreshing output
        """
        super(IwconfigQuery, self).__init__()
        self.interface = interface
        self.connection = connection
        self.interval = interval
        self._command = None
        self._event_timer = None
        return

    @property
    def event_timer(self):
        """
        An EventTimer to track intervals between calling iwconfig
        """
        if self._event_timer is None:
            self._event_timer = EventTimer(seconds=self.interval)
        return self._event_timer        

    @property
    def output(self):
        """
        Output of the iwconfig command, refreshed at self.interval second intervals
        """
        if self.event_timer.is_set():
            self._output = self()
            self.event_timer.start()
        return self._output

    @property
    def command(self):
        """
        :return: command to send to connection to query iwconfig
        """
        if self._command is None:
            self._command = 'iwconfig {0}'.format(self.interface)
        return self._command

    def __call__(self):
        """
        Calls the iwconfig command and returns the output
        """
        stdin, stdout, stderr = self.connection.iwconfig(self.interface)
        self.check_errors(stderr)
        return stdout.readlines()

    def check_errors(self, stderr):
        """
        Checks for known errors

        :param:

         - `stderr`: file-like object for standard error
        :raise: ApeError if an error is found
        """
        for line in stderr:
            if 'No such device' in line:
                self.logger.error(line)
                raise ApeError("'{0}' is not a recognized interface".format(self.interface))
            if 'no wireless extensions' in line:
                self.logger.error(line)
                raise ApeError("'{0}' is not a wireless interface".format(self.interface))
            if 'command not found' in line:
                self.logger.error(line)
                raise ApeError("'iwconfig' doesn't seem to be installed on the path.".format(self.interface))
        return

    def close(self):
        """
        Closes the event timer
        """
        self.event_timer.close()
        return
# end class IwconfigQuery    
