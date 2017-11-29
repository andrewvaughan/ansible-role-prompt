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
Test suite for the Ansible prompt action plugin.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import ansible
import mock
import StringIO
import sys
import unittest

from action_plugins import Prompt

from ansible.playbook.task import Task as AnsibleTask
from ansible.playbook.play_context import PlayContext as AnsiblePlayContext


class TestAsk(unittest.TestCase):
    """
    Tests the messaging portion of the Ansible prompt action plugin.

    .. class:: TestAsk
    .. versionadded:: 0.2.0
    """

    def setUp(self):
        """
        Sets up a prompt object before each test.

        .. versionadded:: 0.2.0
        .. function:: setUp()
        """
        self.prompt = self._getPrompt()

        self.outstr = StringIO.StringIO()
        self.prompt.setOutput(self.outstr)

        self.response = {
            "changed": False
        }

        self.expected = self.response.copy()


    def _getPrompt(self):
        """
        Return a generic Prompt object.

        :returns: generic Prompt object

        .. versionadded:: 0.2.0
        .. function:: _getPrompt()
        """
        return Prompt(
            task=AnsibleTask(),
            connection=None,
            play_context=AnsiblePlayContext(),
            loader=None,
            templar=None,
            shared_loader_obj=None
        )




    # __init__(task, connection, play_context, loader, templar, shared_loader_obj)

    def test_prompt_init_default_instr_valid(self):
        """
        Test that the default input stream is '/dev/tty'.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_init_default_instr_valid()
        """
        self.assertEqual(self._getPrompt()._instr, '/dev/tty')




    # setIntput(instr)

    def test_prompt_setInput_default_valid(self):
        """
        Test that the default setting for a prompt is '/dev/tty'.

        .. versionadded:: 0.2.0
        .. function:: test_setInput_default_valid()
        """
        self.prompt.setInput()

        self.assertEquals(
            self.prompt._instr,
            '/dev/tty'
        )

        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': 'varname'
            })

            self.assertEquals(result['ansible_facts']['varname'], 'mocked input')


    def test_prompt_setInput_stringio_valid(self):
        """
        Test that an updated setting for setInput() sticks.

        .. versionadded:: 0.2.0
        .. function:: test_setInput_stringio_valid()
        """
        instr = StringIO.StringIO()
        self.prompt.setInput(instr)

        self.assertEquals(instr, self.prompt._instr)
        self.assertEquals(instr.getvalue(), "")

        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': 'varname'
            })

            self.assertEquals(result['ansible_facts']['varname'], 'mocked input')



    # _prompt(result, msg)

    def test_prompt_ask_var_empty_invalid(self):
        """
        Test that the _prompt() function returns an error if given an empty variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_empty_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Parameter 'ask' must provide variable name.  Empty received."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": None
            }),
            self.expected
        )


    def test_prompt_ask_var_spaces_invalid(self):
        """
        Test that the _prompt() function returns an error if given spaces in a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_spaces_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Parameter 'ask' must provide variable name.  Empty received."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "   "
            }),
            self.expected
        )


    def test_prompt_ask_var_space_invalid(self):
        """
        Test that the _prompt() function returns an error if given a space in a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_space_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Invalid character in 'ask' parameter 'hello world'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "hello world"
            }),
            self.expected
        )


    def test_prompt_ask_var_dash_invalid(self):
        """
        Test that the _prompt() function returns an error if given a dash in a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_dash_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Invalid character in 'ask' parameter 'hello-world'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "hello-world"
            }),
            self.expected
        )


    def test_prompt_ask_var_bracket_invalid(self):
        """
        Test that the _prompt() function returns an error if given a bracket in a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_bracket_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Invalid character in 'ask' parameter 'hello(world'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "hello(world"
            }),
            self.expected
        )


    def test_prompt_ask_var_period_invalid(self):
        """
        Test that the _prompt() function returns an error if given a period in a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_period_invalid()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Invalid character in 'ask' parameter 'hello.world'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "hello.world"
            }),
            self.expected
        )


    def test_prompt_ask_var_simple_valid(self):
        """
        Test that the _prompt() function properly sets input given a simple variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_simple_valid()
        """
        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': 'varname'
            })

            self.assertEquals(result['ansible_facts']['varname'], 'mocked input')


    def test_prompt_ask_var_numbers_valid(self):
        """
        Test that the _prompt() function properly sets input given numbers as a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_numbers_valid()
        """
        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': '12345'
            })

            self.assertEquals(result['ansible_facts']['12345'], 'mocked input')


    def test_prompt_ask_var_unicode_valid(self):
        """
        Test that the _prompt() function properly sets input given unicode as a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_unicode_valid()
        """
        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': u'varname'
            })

            self.assertEquals(result['ansible_facts']['varname'], 'mocked input')


    def test_prompt_ask_var_underscore_valid(self):
        """
        Test that the _prompt() function properly sets input given an underscore string as a variable.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_var_underscore_valid()
        """
        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'say': 'test',
                'ask': 'var_name'
            })

            self.assertEquals(result['ansible_facts']['var_name'], 'mocked input')


    def test_prompt_ask_say_missing_valid(self):
        """
        Test that the _prompt() function works properly without a 'say' parameter.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_ask_say_missing_valid()
        """
        with mock.patch('__builtin__.raw_input', return_value='mocked input') as mockinput:
            result = self.prompt._prompt({}, {
                'ask': 'varname'
            })

            self.assertEquals(result['ansible_facts']['varname'], 'mocked input')


    def test_prompt_msg_newline_withask_fails(self):
        """
        Test that the _prompt() method fails if both `ask` and `newline` are set.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_msg_newline_withask_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Option 'newline' is not compatible with option 'ask'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "test_var",
                "newline": False
            }),
            self.expected
        )


    def test_prompt_msg_align_withask_fails(self):
        """
        Test that the _prompt() method fails if both `ask` and `align` are set.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_msg_align_withask_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Option 'align' is not compatible with option 'ask'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "ask": "test_var",
                "align": "center"
            }),
            self.expected
        )
