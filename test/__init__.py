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
Test suite for the Ansible Prompt action plugin.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import ansible
import mock
import StringIO
import unittest

from action_plugins import Prompt

from ansible.playbook.task import Task as AnsibleTask
from ansible.playbook.play_context import PlayContext as AnsiblePlayContext


__all__ = [
    'PromptTestAbstract',
]


class PromptTestAbstract(unittest.TestCase):
    """
    Provide common functionality for tests within the Prompt module.

    .. versionadded:: 0.4.0

    .. class:: PromptTestAbstract
    """

    def setUp(self):
        """
        Set up a Prompt object before each test.

        .. versionadded:: 0.1.0

        .. versionchanged:: 0.4.0
           Switched newly-deprecated methods to their new names.

        .. function:: setUp()
        """
        self.mockTask = mock.Mock(
            spec=AnsibleTask,
            async=False,
            args={}
        )

        self.mockPlayContext = mock.Mock(spec=AnsiblePlayContext)

        self.prompt = self._createPrompt()

        self.outstr = StringIO.StringIO()
        self.prompt.setOutputStream(self.outstr)

        self.response = {
            "changed": False
        }

        self.expected = self.response.copy()


    def tearDown(self):
        """
        Tear down the Prompt object created after test is complete.

        .. versionadded:: 0.4.0

        .. function:: tearDown()
        """
        self.mockTask.reset_mock()
        self.mockPlayContext.reset_mock()


    def _getPrompt(self):
        """
        Return a new, generic Prompt object.

        .. deprecated:: 0.4.0
           Use :func:`_createPrompt` instead; will be removed in 1.0.0

        .. versionadded:: 0.1.0

        .. versionchanged:: 0.4.0
           Deprecated and renamed to :func:`_createPrompt`

        .. function:: _getPrompt()
        """
        return self._createPrompt()


    def _createPrompt(self):
        """
        Return a new, generic Prompt object.

        :returns: a generic Prompt object

        .. versionadded:: 0.4.0

        .. function:: _createPrompt()
        """
        return Prompt(
            task=self.mockTask,
            connection=None,
            play_context=self.mockPlayContext,
            loader=None,
            templar=None,
            shared_loader_obj=None
        )
