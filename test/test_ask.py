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

        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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

        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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
        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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
        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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
        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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
        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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
        with mock.patch('__builtin__.input', return_value='mocked input') as mockinput:
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


    def test_prompt_msg_noask_default_fails(self):
        """
        Test that the _prompt() method fails if 'default' is provided without 'ask'

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_noask_default_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected 'default' in non-question prompt."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Hello World",
                "default": "foobar"
            }),
            self.expected
        )


    def test_prompt_msg_noask_postfix_fails(self):
        """
        Test that the _prompt() method fails if 'postfix' is provided without 'ask'

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_noask_postfix_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected 'postfix' in non-question prompt."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Hello World",
                "postfix": "foobar"
            }),
            self.expected
        )


    def test_prompt_msg_noask_trim_fails(self):
        """
        Test that the _prompt() method fails if 'trim' is provided without 'ask'

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_noask_trim_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected 'trim' in non-question prompt."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Hello World",
                "trim": False
            }),
            self.expected
        )


    def test_prompt_msg_noask_confirm_fails(self):
        """
        Test that the _prompt() method fails if 'confirm' is provided without 'ask'

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_noask_confirm_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected 'confirm' in non-question prompt."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Hello World",
                "confirm": True
            }),
            self.expected
        )


    def test_prompt_msg_confirm_defaults_fails(self):
        """
        Test that the _prompt() method fails if given both default and confirm.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_confirm_defaults_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected 'default' provided with confirmation question."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Continue",
                "ask": "result",
                "confirm": True,
                "default": "some other thing"
            }),
            self.expected
        )


    def test_prompt_msg_ask_repeats(self):
        """
        Test that the _prompt() method repeats an ask if given a blank response with no default.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_noask_postfix_fails()
        """
        global counter
        counter = 0

        def return_helper(*args, **kwargs):
            """
            Returns a different value the second time called.
            """
            global counter

            counter = counter + 1
            if counter > 1:
                return "foobar"

            return ""

        with mock.patch('__builtin__.input', side_effect=return_helper) as mockinput:
            result = self.prompt._prompt({}, {
                'ask': 'varname'
            })

            self.assertEqual(mockinput.call_count, 2)
            self.assertEquals(result['ansible_facts']['varname'], 'foobar')


    def test_prompt_msg_shows_default(self):
        """
        Test that the _prompt() method shows the default in the prompt, if provided.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_shows_default()
        """
        with mock.patch('__builtin__.input', return_value="Andrew") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "First Name",
                "ask": "first_name",
                "default": "foobar"
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("First Name [foobar]? ", args[0])
            self.assertEquals(result['ansible_facts']['first_name'], 'Andrew')



    def test_prompt_msg_defaults(self):
        """
        Test that the _prompt() method sets the fact to the default if provided and no input is given.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_defaults()
        """
        with mock.patch('__builtin__.input', return_value="") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "First Name",
                "ask": "first_name",
                "default": "foobar"
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("First Name [foobar]? ", args[0])
            self.assertEquals(result['ansible_facts']['first_name'], 'foobar')


    def test_prompt_msg_postfix_custom(self):
        """
        Test that the _prompt() method uses the provided postfix in the prompt.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_postfix_custom()
        """
        with mock.patch('__builtin__.input', return_value="") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "First Name",
                "ask": "first_name",
                "default": "foobar",
                "postfix": "!?!?"
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("First Name [foobar]!?!? ", args[0])
            self.assertEquals(result['ansible_facts']['first_name'], 'foobar')


    def test_prompt_msg_trim_default(self):
        """
        Test that the _prompt() method will trim responses by default

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_trim_default()
        """
        with mock.patch('__builtin__.input', return_value="  trim  value  ") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "First Name",
                "ask": "first_name",
            })

            self.assertEquals(result['ansible_facts']['first_name'], 'trim  value')


    def test_prompt_msg_trim_off_valid(self):
        """
        Test that the _prompt() method will not trim responses if set to False.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_trim_off_valid()
        """
        with mock.patch('__builtin__.input', return_value="  trim  value  ") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "First Name",
                "ask": "first_name",
                "trim": False
            })

            self.assertEquals(result['ansible_facts']['first_name'], '  trim  value  ')


    def test_prompt_msg_confirm_invalid_repeats(self):
        """
        Test that the _prompt() method will repeat if given an invalid response with confirm.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_confirm_invalid_repeats()
        """
        global counter
        counter = 0

        def return_helper(*args, **kwargs):
            """
            Returns a different value the second time called.
            """
            global counter

            counter = counter + 1
            if counter > 1:
                return "Y"

            return "foobar"

        with mock.patch('__builtin__.input', side_effect=return_helper) as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "Continue",
                "ask": "result",
                "confirm": False
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("Continue [yN]? ", args[0])
            self.assertEqual(mockinput.call_count, 2)
            self.assertEquals(result['ansible_facts']['result'], True)


    def test_prompt_msg_confirm_blank_default_yes(self):
        """
        Test that the _prompt() method will return appropriately with confirm as default.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_confirm_blank_default_yes()
        """
        with mock.patch('__builtin__.input', return_value="") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "Continue",
                "ask": "result",
                "confirm": True
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("Continue [Yn]? ", args[0])
            self.assertEquals(result['ansible_facts']['result'], True)


    def test_prompt_msg_confirm_blank_default_no(self):
        """
        Test that the _prompt() method will return appropriately with confirm as default.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_confirm_blank_default_no()
        """
        with mock.patch('__builtin__.input', return_value="") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "Continue",
                "ask": "result",
                "confirm": False
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("Continue [yN]? ", args[0])
            self.assertEquals(result['ansible_facts']['result'], False)


    def test_prompt_msg_confirm_capital_valid(self):
        """
        Test that the _prompt() method works with capital responses for confirms.

        .. versionadded:: 1.0.0
        .. function:: test_prompt_msg_confirm_capital_valid()
        """
        with mock.patch('__builtin__.input', return_value="Y") as mockinput:
            result = self.prompt._prompt(self.response, {
                "say": "Continue",
                "ask": "result",
                "confirm": False
            })

            args, kwargs = mockinput.call_args

            self.assertEquals("Continue [yN]? ", args[0])
            self.assertEquals(result['ansible_facts']['result'], True)
