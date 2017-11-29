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


class TestSay(unittest.TestCase):
    """
    Tests the messaging portion of the Ansible prompt action plugin.

    .. class:: TestSay
    .. versionadded:: 0.1.0
    """

    def setUp(self):
        """
        Sets up a prompt object before each test.

        .. versionadded:: 0.1.0
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

        .. versionadded:: 0.1.0
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

    def test_prompt_init_default_outstr_valid(self):
        """
        Test that the default output stream is stdout.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_init_default_outstr_valid()
        """
        self.assertEqual(self._getPrompt()._outstr, sys.stdout)




    # setOutput(outstr)

    def test_prompt_setOutput_default_valid(self):
        """
        Test that the default setting for a prompt is stdout.

        .. versionadded:: 0.1.0
        .. function:: test_setOutput_default_valid()
        """
        prompt = self._getPrompt()
        prompt.setOutput()

        self.assertEquals(
            prompt._outstr,
            sys.stdout
        )


    def test_prompt_setOutput_stringio_valid(self):
        """
        Test that an updated setting for setOutput() sticks.

        .. versionadded:: 0.1.0
        .. function:: test_setOutput_stringio_valid()
        """
        prompt = self._getPrompt()
        outstr = StringIO.StringIO()

        prompt.setOutput(outstr)

        self.assertEquals(outstr, prompt._outstr)
        self.assertEquals(outstr.getvalue(), "")

        prompt._prompt({}, "test")

        self.assertEquals(outstr.getvalue(), "test\n")




    # _fail(result, msg, args*)

    def test_prompt_fail_params_missing_exception(self):
        """
        Test that the _fail() method throws an exception if all parameters are missing.

        .. versionadded:: 0.1.0
        .. function:: test_fail_params_missing_exception()
        """
        with self.assertRaises(TypeError):
            self.prompt._fail()


    def test_prompt_fail_response_missing_exception(self):
        """
        Test that the _fail() method throws an exception if the response is missing.

        .. versionadded:: 0.1.0
        .. function:: test_fail_response_missing_exception()
        """
        with self.assertRaises(TypeError):
            self.prompt._fail(None, "Failure Message")


    def test_prompt_fail_response_invalid_exception(self):
        """
        Test that the _fail() method throws an exception if the response is not a dict.

        .. versionadded:: 0.1.0
        .. function:: test_fail_response_invalid_exception()
        """
        with self.assertRaises(TypeError):
            self.prompt._fail("Bad Result", "Failure Message")


    def test_prompt_fail_message_missing_exception(self):
        """
        Test that the _fail() method throws an exception if no message is provided.

        .. versionadded:: 0.1.0
        .. function:: test_fail_message_missing_exception()
        """
        with self.assertRaises(TypeError):
            self.prompt._fail(self.response)


    def test_prompt_fail_message_empty_exception(self):
        """
        Test that the _fail() method throws an exception if an empty message is provided.

        .. versionadded:: 0.1.0
        .. function:: test_fail_message_empty_exception()
        """
        with self.assertRaises(ValueError):
            self.prompt._fail(self.response, "")


    def test_prompt_fail_message_nonstring_exception(self):
        """
        Test that the _fail() method throws an exception if a non-string message is provided.

        .. versionadded:: 0.1.0
        .. function:: test_fail_message_nonstring_exception()
        """
        with self.assertRaises(TypeError):
            self.prompt._fail(self.response, 45)
            self.prompt._fail(self.response, {"hello": "bar"})
            self.prompt._fail(self.response, ["a", "b"])


    def test_prompt_fail_message_valid_success(self):
        """
        Tests that the _fail() method returns an expected response.

        .. versionadded:: 0.1.0
        .. function:: test_fail_message_valid_success()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Failure Message"

        self.assertEquals(
            self.prompt._fail(self.response, "Failure Message"),
            self.expected
        )


    def test_prompt_fail_message_valid_success(self):
        """
        Test that the _fail() method returns an expected response with multiple variables.

        .. versionadded:: 0.1.0
        .. function:: test_fail_message_valid_success()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Failure Message A 3.14 Cats"

        self.assertEquals(
            self.prompt._fail(self.response, "Failure Message %s %.2f %s", "A", 3.14159, "Cats"),
            self.expected
        )




    # _prompt(result, msg)

    def test_prompt_param_invalid_fails(self):
        """
        Test that the _prompt() method returns a failure if given a bad, top-level parameter name.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_param_invalid_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected parameter 'foo'"

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "foo": "bar"
            }),
            self.expected
        )


    def test_prompt_msg_emptystring_fails(self):
        """
        Test that the _prompt() method returns a failure if an empty string is provided for the message.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_emptystring_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "No message provided"

        self.assertEquals(
            self.prompt._prompt(self.response, ""),
            self.expected
        )


    def test_prompt_msg_emptylist_fails(self):
        """
        Test that the _prompt() method returns a failure if an empty list is provided for the message.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_emptylist_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "No message provided"

        self.assertEquals(
            self.prompt._prompt(self.response, []),
            self.expected
        )


    def test_prompt_msg_emptyobject_fails(self):
        """
        Test that the _prompt() method returns a failure if an empty object is provided for the message.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_emptyobject_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "No message provided"

        self.assertEquals(
            self.prompt._prompt(self.response, {}),
            self.expected
        )


    def test_prompt_msg_none_fails(self):
        """
        Test that the _prompt() method returns a failure if no message is provided.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_none_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "No message provided"

        self.assertEquals(
            self.prompt._prompt(self.response, None),
            self.expected
        )


    def test_prompt_msg_string_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple string.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_string_succeeds()
        """
        msg = "Hello World"

        self.assertTrue(isinstance(msg, str))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % msg)


    def test_prompt_msg_unicode_succeeds(self):
        """
        Test that the _prompt() method is successful if given a unicode string.

        .. versionadded:: 0.2.0
        .. function:: test_prompt_msg_unicode_succeeds()
        """
        msg = u"Hello World"

        self.assertTrue(isinstance(msg, unicode))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % msg)


    def test_prompt_msg_int_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple integer.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_int_succeeds()
        """
        msg = 1

        self.assertTrue(isinstance(msg, int))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_long_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple long.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_long_succeeds()
        """
        msg = sys.maxint + 1

        self.assertTrue(isinstance(msg, long))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_float_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple float.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_float_succeeds()
        """
        msg = 1.1

        self.assertTrue(isinstance(msg, float))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_complex_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple complex.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_complex_succeeds()
        """
        msg = complex(1, 5)

        self.assertTrue(isinstance(msg, complex))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_tuple_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple tuple.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_tuple_succeeds()
        """
        msg = (1, 5)

        self.assertTrue(isinstance(msg, tuple))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_set_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple set.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_set_succeeds()
        """
        msg = set([1, 5, 50, "alpha"])

        self.assertTrue(isinstance(msg, set))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_frozenset_succeeds(self):
        """
        Test that the _prompt() method is successful if given a simple frozenset.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_frozenset_succeeds()
        """
        msg = frozenset([-5, 5, 5.0, "beta"])

        self.assertTrue(isinstance(msg, frozenset))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % str(msg))


    def test_prompt_msg_listparam_invalid_fails(self):
        """
        Test that the _prompt() method fails if given a list with an invalid parameter in it.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_listparam_invalid_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Unexpected parameter 'foo'"

        self.assertEquals(
            self.prompt._prompt(self.response, [
                {"say": "valid"},
                {"foo": "bar"}
            ]),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "valid\n")


    def test_prompt_msg_list_empty_fails(self):
        """
        Test that the _prompt() method fails if given an empty list.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_list_empty_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "No message provided"

        self.assertEquals(
            self.prompt._prompt(self.response, []),
            self.expected
        )


    def test_prompt_msg_list_succeeds(self):
        """
        Test that the _prompt() method is successful if given multiple, simple strings.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_list_succeeds()
        """
        msg = [
            "alpha",
            "bravo",
            -7,
            1.5
        ]

        self.assertTrue(isinstance(msg, list))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % ("\n".join([str(m) for m in msg])))


    def test_prompt_msg_listsay_succeeds(self):
        """
        Test that the _prompt() method is successful if given multiple, simple strings.

        .. versionadded:: 0.1.0
        .. function:: test_prompt_msg_listsay_succeeds()
        """
        msg = [
            {"say": "a"},
            {"say": "B"},
            {"say": -20},
            {"say": 5.5},
        ]

        self.assertTrue(isinstance(msg, list))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "%s\n" % ("\n".join([str(m['say']) for m in msg])))


    def test_prompt_msg_saynewline_succeeds(self):
        """
        Test that the _prompt() method is successful if given a string that has no trailing newline.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_msg_saynewline_succeeds()
        """
        msg = [
            {"say": "Hello World", "newline": False},
        ]

        self.assertTrue(isinstance(msg, list))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "Hello World")


    def test_prompt_msg_saynewlinemultiple_succeeds(self):
        """
        Test that the _prompt() method is successful if given multiple strings that have no trailing newline.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_msg_saynewlinemultiple_succeeds()
        """
        msg = [
            {"say": "Hello ", "newline": False},
            {"say": "World", "newline": False},
            {"say": ", How are we?", "newline": True},
        ]

        self.assertTrue(isinstance(msg, list))

        self.assertEquals(
            self.prompt._prompt(self.response, msg),
            self.expected
        )

        self.assertEquals(self.outstr.getvalue(), "Hello World, How are we?\n")


    def test_prompt_msg_align_invalid_fails(self):
        """
        Test that the _prompt() method is fails if given an invalid align option.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_msg_align_invalid_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Align 'foobar' invalid.  Expected 'left', 'center', or 'right'."

        self.assertEquals(
            self.prompt._prompt(self.response, {
                "say": "Hello World",
                "align": "foobar"
            }),
            self.expected
        )


    def test_prompt_param_align_left_valid(self):
        """
        Test that the param() method is successful with a left alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_param_align_left_valid()
        """
        with mock.patch('subprocess.check_output', return_value='10 50'):
            msg = [
                {"say": "Hello World", "align": "left"},
            ]

            self.assertTrue(isinstance(msg, list))

            self.assertEquals(
                self.prompt._prompt(self.response, msg),
                self.expected
            )

            self.assertEquals(self.outstr.getvalue(), "Hello World\n")


    def test_prompt_param_align_center_valid(self):
        """
        Test that the param() method is successful with a center alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_param_align_center_valid()
        """
        with mock.patch('subprocess.check_output', return_value='10 75'):
            msg = [
                {"say": "Hello World", "align": "center"},
            ]

            self.assertTrue(isinstance(msg, list))

            self.assertEquals(
                self.prompt._prompt(self.response, msg),
                self.expected
            )

            self.assertEquals(self.outstr.getvalue(), "%s%s" % ("Hello World".center(74), "\n"))


    def test_prompt_param_align_right_valid(self):
        """
        Test that the param() method is successful with a right alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_param_align_right_valid()
        """
        with mock.patch('subprocess.check_output', return_value='10 88'):
            msg = [
                {"say": "Hello World", "align": "right"},
            ]

            self.assertTrue(isinstance(msg, list))

            self.assertEquals(
                self.prompt._prompt(self.response, msg),
                self.expected
            )

            self.assertEquals(self.outstr.getvalue(), "%s%s" % ("Hello World".rjust(87), "\n"))




    # run(tmp=None, task_vars=None)

    def test_prompt_run_msg_missing_fails(self):
        """
        Test that the run() method will fail if missing the msg parameter.

        .. versionadded:: 0.1.0
        .. function:: test_run_msg_missing_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Required 'msg' parameter missing."

        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)

        self.assertEquals(
            prompt.run(),
            self.expected
        )


    def test_prompt_run_multiple_params_fails(self):
        """
        Test that the run() method will fail if there are too many parameters.

        .. versionadded:: 0.1.0
        .. function:: test_run_multiple_params_fails()
        """
        self.expected['failed'] = True
        self.expected['msg'] = "Expected single 'msg' parameter. Multiple parameters given."

        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)
        prompt._task.args = {
            "msg": "Hello World",
            "foo": "bar"
        }

        self.assertEquals(
            prompt.run(),
            self.expected
        )


    def test_prompt_run_singlemessage_valid(self):
        """
        Test that the run() method will succeed with a single message.

        .. versionadded:: 0.1.0
        .. function:: test_run_singlemessage_valid()
        """
        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)
        prompt._task.args = {
            "msg": "Hello World"
        }

        self.assertEquals(
            prompt.run(),
            self.expected
        )

        self.assertEquals(
            self.outstr.getvalue(),
            "Hello World\n"
        )


    def test_prompt_run_multimessage_valid(self):
        """
        Test that the run() method will succeed with a multiple messages.

        .. versionadded:: 0.1.0
        .. function:: test_run_multimessage_valid()
        """
        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)
        prompt._task.args = {
            "msg": [
                "Hello World",
                "Hi there"
            ]
        }

        self.assertEquals(
            prompt.run(),
            self.expected
        )

        self.assertEquals(
            self.outstr.getvalue(),
            "Hello World\nHi there\n"
        )


    def test_prompt_run_saynewlinemultiple_valid(self):
        """
        Test that the run() method will succeed with a multiple messages.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_run_saynewlinemultiple_valid()
        """
        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)
        prompt._task.args = {
            "msg": [
                {
                    "say": "Hello ",
                    "newline": False,
                },
                {
                    "say": "World",
                    "newline": True,
                }
            ]
        }

        self.assertEquals(
            prompt.run(),
            self.expected
        )

        self.assertEquals(
            self.outstr.getvalue(),
            "Hello World\n"
        )


    def test_prompt_run_align_left_valid(self):
        """
        Test that the run() method is successful with a left alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_run_align_left_valid()
        """
        del(self.expected['changed'])

        prompt = self._getPrompt()

        prompt.setOutput(self.outstr)
        prompt._task.args = {
            "msg": [
                {
                    "say": "Hello World",
                    "align": "left",
                }
            ]
        }

        self.assertEquals(
            prompt.run(),
            self.expected
        )

        self.assertEquals(
            self.outstr.getvalue(),
            "Hello World\n"
        )


    def test_prompt_run_align_center_valid(self):
        """
        Test that the run() method is successful with a center alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_run_align_center_valid()
        """
        with mock.patch('subprocess.check_output', return_value='10 88'):
            del(self.expected['changed'])

            prompt = self._getPrompt()

            prompt.setOutput(self.outstr)
            prompt._task.args = {
                "msg": [
                    {
                        "say": "Hello World",
                        "align": "center",
                        "newline": False,
                    }
                ]
            }

            self.assertEquals(
                prompt.run(),
                self.expected
            )

            self.assertEquals(
                self.outstr.getvalue(),
                "Hello World".center(88)
            )


    def test_prompt_run_align_right_valid(self):
        """
        Test that the run() method is successful with a right alignment.

        .. versionadded:: 0.3.0
        .. function:: test_prompt_run_align_right_valid()
        """
        with mock.patch('subprocess.check_output', return_value='10 52'):
            del(self.expected['changed'])

            prompt = self._getPrompt()

            prompt.setOutput(self.outstr)
            prompt._task.args = {
                "msg": [
                    {
                        "say": "Hello World",
                        "align": "right",
                        "newline": False,
                    }
                ]
            }

            self.assertEquals(
                prompt.run(),
                self.expected
            )

            self.assertEquals(
                self.outstr.getvalue(),
                "Hello World".rjust(52)
            )
