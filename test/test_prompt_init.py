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
Test suite for the Ansible Prompt action plugin pertaining to object initialization.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import mock
import sys

from test import PromptTestAbstract


class TestPromptInit(PromptTestAbstract):
    """
    Tests the initialization of a Prompt object

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.4.0
       Separated into separate test class; added tests for other initialization parameters than outstr.

    .. class:: TestPromptInit
    """

    def test_Prompt_init_should_call_ActionBase_super(self):
        """
        Test that :func:`super` is called from the ActionBase.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_init_should_call_ActionBase_super()
        """
        with mock.patch('action_plugins.prompt.ActionBase.__init__') as mock_super:
            prompt = self._createPrompt()
            self.assertTrue(mock_super.called)


    def test_Prompt_init_getOutputStream_defaults_to_stdout(self):
        """
        Test that the default output stream is stdout.

        .. versionadded:: 0.2.0

        .. versionchanged:: 0.4.0
           Using getter methods instead of direct variable calls.

        .. function:: test_Prompt_init_getOutputStream_defaults_to_stdout()
        """
        self.assertEqual(
            self._createPrompt().getOutputStream(),
            sys.stdout
        )


    def test_Prompt_init_getInputStream_defaults_to_tty(self):
        """
        Test that the default input stream is /dev/tty.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_init_getInputStream_defaults_to_tty()
        """
        self.assertEqual(
            self._createPrompt().getInputStream(),
            '/dev/tty'
        )


    def test_Prompt_init_VALID_PARAMS_as_expected(self):
        """
        Test that the parameters accepted by the Action Plugin are as expected.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_init_VALID_PARAMS_as_expected()
        """
        expected_list = [
            'say', 'newline', 'align',
            'ask', 'default', 'confirm', 'postfix', 'trim',
            # 'secret', 'confirm', 'salt', 'salt_length',
        ]

        self.assertEqual(
            len(self.prompt.VALID_PARAMS),
            len(expected_list)
        )

        self.assertEqual(
            sorted(self.prompt.VALID_PARAMS),
            sorted(expected_list)
        )
