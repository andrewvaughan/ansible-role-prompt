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
Test suite for the Ansible Prompt action plugin pertaining to getters and setters.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import StringIO
import sys

from test import PromptTestAbstract


class TestPromptGettersAndSetters(PromptTestAbstract):
    """
    Tests the various getters and setters for the Prompt class.

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.4.0
       Separated into separate test class.

    .. class:: TestPromptGettersAndSetters
    """

    def test_Prompt_setOutput_defaults_to_stdout(self):
        """
        Test that the setOutput function defaults to sys.stdout if not set.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setOutput_defaults_to_stdout()
        """
        self.prompt.setOutput()

        self.assertEqual(
            self.prompt.getOutputStream(),
            sys.stdout
        )


    def test_Prompt_setOutput_and_getOutput_match(self):
        """
        Test that the getter changes once modified by the setter for the Output variable.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setOutput_and_getOutput_match()
        """
        self.prompt.setOutput()

        new_output = StringIO.StringIO()

        self.assertEqual(
            self.prompt.getOutputStream(),
            sys.stdout
        )

        self.prompt.setOutput(new_output)

        self.assertEqual(
            self.prompt.getOutputStream(),
            new_output
        )

    def test_Prompt_setInput_defaults_to_tty(self):
        """
        Test that the setInput function defaults to '/dev/tty' if not set.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setInput_defaults_to_tty()
        """
        self.prompt.setInput()

        self.assertEqual(
            self.prompt.getInputStream(),
            '/dev/tty'
        )


    def test_Prompt_setInput_and_getInput_match(self):
        """
        Test that the getter changes once modified by the setter for the Input variable.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setInput_and_getInput_match()
        """
        self.prompt.setInput()

        new_input = '/dev/foobar'

        self.assertEqual(
            self.prompt.getInputStream(),
            '/dev/tty'
        )

        self.prompt.setInput(new_input)

        self.assertEqual(
            self.prompt.getInputStream(),
            new_input
        )


    def test_Prompt_setTaskArguments_and_getTaskArguments_match(self):
        """
        Test that the getter changes one modified by the setter for the TaskArguments variable.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setTaskArguments_and_getTaskArguments_match()
        """
        new_args = {
            'foo': 'bar',
            'num': 12345
        }

        self.prompt.setTaskArguments(new_args)

        self.assertEqual(
            len(self.prompt.getTaskArguments()),
            2
        )

        self.assertEqual(
            self.prompt.getTaskArguments(),
            new_args
        )


    def test_Prompt_setTaskArgument_and_getTaskArgument_match(self):
        """
        Test that the getter changes one modified by the setter for a single TaskArguments variable.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setTaskArgument_and_getTaskArgument_match()
        """
        prompt = self._createPrompt()

        prompt.setTaskArgument('foo', 'bar')
        prompt.setTaskArgument('num', 12345)

        self.assertEqual(
            prompt.getTaskArgument('foo'),
            'bar'
        )

        self.assertEqual(
            prompt.getTaskArgument('num'),
            12345
        )


    def test_Prompt_setTaskArgument_and_getTaskArguments_match(self):
        """
        Test that the getter for all TaskArguments changes one modified by the setter for a single TaskArguments
        variable.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setTaskArgument_and_getTaskArguments_match()
        """
        self.prompt.setTaskArgument('foo', 'bar')
        self.prompt.setTaskArgument('num', 12345)

        self.assertEqual(
            sorted(self.prompt.getTaskArguments()),
            [
                'foo',
                'num'
            ]
        )

        self.assertEqual(
            self.prompt.getTaskArguments()['foo'],
            'bar'
        )

        self.assertEqual(
            self.prompt.getTaskArguments()['num'],
            12345
        )


    def test_Prompt_setTaskArguments_and_getTaskArgument_match(self):
        """
        Test that the getter for a single TaskArgument changes one modified by the setter for all TaskArguments.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_setTaskArguments_and_getTaskArgument_match()
        """
        self.prompt.setTaskArguments({
            'foo': 'bar',
            'num': 12345
        })

        self.assertEqual(
            self.prompt.getTaskArgument('foo'),
            'bar'
        )

        self.assertEqual(
            self.prompt.getTaskArgument('num'),
            12345
        )
