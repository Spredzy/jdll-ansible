# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import datetime

from ansible.plugins.callback import CallbackBase


_LOGFILE = '/tmp/log.txt'

class CallbackModule(CallbackBase):
    """
    This callback module tells you how long your plays ran for.
    """

    def __init__(self):

        super(CallbackModule, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        """Event executed after each command when it succeed. Get the output
        of the command and create a file associated to the current
        jobstate.
        """

        super(CallbackModule, self).v2_runner_on_ok(result, **kwargs)
        open(_LOGFILE, 'a').write('%s: Task ok\n' % datetime.now())

    def v2_runner_on_failed(self, result, ignore_errors=False):
        """Event executed after each command when it fails. Get the output
        of the command and create a failure jobstate and a file associated.
        """

        super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)
        open(_LOGFILE, 'a').write('%s: Task has failed\n' % datetime.now())

    def v2_playbook_on_play_start(self, play):
        """Event executed before each play. Create a new jobstate and save
        the current jobstate id.
        """

        super(CallbackModule, self).v2_playbook_on_play_start(play)
        open(_LOGFILE, 'a').write('%s: Run has started\n' % datetime.now())
