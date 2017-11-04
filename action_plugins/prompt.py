#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Andrew Vaughan <hello@andrewvaughan.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
ActionModule definition for the Ansible prompt action plugin.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

__metaclass__ = type

import sys

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    """
    Prompts user with one-or-more messages and optionally waits for input for each.

    .. class:: ActionModule
    .. versionadded:: 0.1.0
    """

    TRANSFERS_FILES = False
    VALID_PARAMS = ["say"]


    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        """
        Initializes the prompt Ansible plugin.

        .. versionadded:: 0.1.0
        .. function:: __init__(task, connection, play_context, loader, templar, shared_loader_obj)
        """
        super(ActionModule, self).__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self.setOutput(sys.stdout)


    def run(self, tmp=None, task_vars=None):
        """
        Performs the plugin task, prompting the user one or more times.

        :kwarg tmp: the temporary directory to use if creating files
        :kwarg task_vars: any variables associated with the task

        :returns: a dictionary of results from the module

        .. versionadded:: 0.1.0
        .. function:: run([tmp=None, task_vars=None])
        """
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        args = self._task.args

        # Expect only the messages parameter
        if 'msg' not in args:
            return self._fail(result, "Required 'msg' parameter missing.")

        if len(args) != 1:
            return self._fail(result, "Expected single 'msg' parameter. Multiple parameters given.")

        return self._prompt(result, args['msg'])


    def setOutput(self, output=None):
        """
        Sets the output stream to write to.

        :kwarg output: an output stream to write to

        .. versionadded:: 0.1.0
        .. function:: setOutput([output=None])
        """
        if output is None:
            self.output = sys.stdout

        else:
            self.output = output


    def _prompt(self, result, msg):
        """
        Prompts the user with a message and optionally asks for a response.

        :kwarg result: the base result dict to build on
        :kwarg msg: the message provided to parse (string, object, or list)

        :returns: an updated dict response with success or failure

        .. versionadded:: 0.1.0
        .. function:: _prompt(result, msg)
        """
        if not isinstance(msg, list):
            msg = [msg]

        if len(msg) == 0:
            return self._fail(result, "No message provided")

        # Parse each item on the list
        for m in msg:

            if m is not None and not isinstance(m, (str, dict)):
                m = str(m)

            # If no message is provided, fail
            if m is None or len(m) == 0:
                return self._fail(result, "No message provided")

            # If a simple scalar value is provided, simply display it
            if not isinstance(m, dict):
                self.output.write("%s\n" % m)
                continue

            # If this is a set of key/value pairs, parse it
            for arg in m:
                if arg not in self.VALID_PARAMS:
                    return self._fail(result, "Unexpected parameter '%s'" % arg)

            if 'say' in m:
                self.output.write("%s\n" % m['say'])

        return result


    def _fail(self, result, message, *args):
        """
        Raises an Ansible exception with a given message.

        :kwarg result: the base result object to build on
        :kwarg message: the message to pass to the Ansible exception
        :kwarg args: an arbitrary number of arguments to replace in the message's formatting

        :returns: an updated dict response with the provided failure condition

        .. versionadded:: 0.1.0
        .. function:: _fail(result, message, *args)
        """
        if not isinstance(result, dict):
            raise TypeError("Invalid result provided. Expected dict, received %s." % type(result))

        if not isinstance(message, str):
            raise TypeError("Invalid message provided. Expected string, received '%s'." % message)

        if message == "":
            raise ValueError("Empty message provided. Requires failure message.")

        result['failed'] = True
        result['msg'] = message % (args)

        return result
