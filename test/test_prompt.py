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
import unittest
import StringIO
import sys

from action_plugins import Prompt

from ansible.playbook.task import Task as AnsibleTask
from ansible.playbook.play_context import PlayContext as AnsiblePlayContext


class TestPrompt(unittest.TestCase):
  """
  Tests the Ansible prompt action plugin.
  """

  def setUp(self):
    """
    Sets up a prompt object before each test.
    """
    self.prompt = self._getPrompt()
    self.output = StringIO.StringIO()

    self.prompt.setOutput(self.output)

    self.response = {
      "changed" : False
    }

    self.expected = self.response.copy()


  def _getPrompt(self):
    """
    Return a generic Prompt object.

      :returns: generic Prompt object
    """
    return Prompt(
      task = AnsibleTask(),
      connection = None,
      play_context = AnsiblePlayContext(),
      loader = None,
      templar = None,
      shared_loader_obj = None
    )




  ### setOutput(output)

  def test_setOutput_default_valid(self):
    """
    Test that the default setting for a prompt is stdout.
    """
    prompt = self._getPrompt()
    prompt.setOutput()

    self.assertEquals(
      prompt.output,
      sys.stdout
    )


  def test_setOutput_stringio_valid(self):
    """
    Test that an updated setting for setOutput() sticks.
    """
    prompt = self._getPrompt()
    output = StringIO.StringIO()

    prompt.setOutput(output)

    self.assertEquals(output, prompt.output)
    self.assertEquals(output.getvalue(), "")

    prompt._prompt({}, "test")

    self.assertEquals(output.getvalue(), "test\n")




  ### _fail(result, msg, args*)

  def test_fail_params_missing_exception(self):
    """
    Test that the _fail() method throws an exception if all parameters are missing.
    """
    with self.assertRaises(TypeError):
      self.prompt._fail()


  def test_fail_response_missing_exception(self):
    """
    Test that the _fail() method throws an exception if the response is missing.
    """
    with self.assertRaises(TypeError):
      self.prompt._fail(None, "Failure Message")


  def test_fail_response_invalid_exception(self):
    """
    Test that the _fail() method throws an exception if the response is not a dict.
    """
    with self.assertRaises(TypeError):
      self.prompt._fail("Bad Result", "Failure Message")


  def test_fail_message_missing_exception(self):
    """
    Test that the _fail() method throws an exception if no message is provided.
    """
    with self.assertRaises(TypeError):
      self.prompt._fail(self.response)


  def test_fail_message_empty_exception(self):
    """
    Test that the _fail() method throws an exception if an empty message is provided.
    """
    with self.assertRaises(ValueError):
      self.prompt._fail(self.response, "")


  def test_fail_message_nonstring_exception(self):
    """
    Test that the _fail() method throws an exception if a non-string message is provided.
    """
    with self.assertRaises(TypeError):
      self.prompt._fail(self.response, 45)
      self.prompt._fail(self.response, {"hello" : "bar"})
      self.prompt._fail(self.response, ["a", "b"])


  def test_fail_message_valid_success(self):
    """
    Tests that the _fail() method returns an expected response.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Failure Message"

    self.assertEquals(
      self.prompt._fail(self.response, "Failure Message"),
      self.expected
    )


  def test_fail_message_valid_success(self):
    """
    Test that the _fail() method returns an expected response with multiple variables.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Failure Message A 3.14 Cats"

    self.assertEquals(
      self.prompt._fail(self.response, "Failure Message %s %.2f %s", "A", 3.14159, "Cats"),
      self.expected
    )




  ### _prompt(result, msg)

  def test_prompt_param_invalid_fails(self):
    """
    Test that the _prompt() method returns a failure if given a bad, top-level parameter name.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Unexpected parameter 'foo'"

    self.assertEquals(
      self.prompt._prompt(self.response, {
        "foo" : "bar"
      }),
      self.expected
    )


  def test_prompt_msg_emptystring_fails(self):
    """
    Test that the _prompt() method returns a failure if an empty string is provided for the message.
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
    """
    msg = "Hello World"

    self.assertTrue(isinstance(msg, str))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % msg)


  def test_prompt_msg_int_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple integer.
    """
    msg = 1

    self.assertTrue(isinstance(msg, int))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_long_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple long.
    """
    msg = sys.maxint + 1

    self.assertTrue(isinstance(msg, long))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_float_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple float.
    """
    msg = 1.1

    self.assertTrue(isinstance(msg, float))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_complex_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple complex.
    """
    msg = complex(1, 5)

    self.assertTrue(isinstance(msg, complex))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_tuple_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple tuple.
    """
    msg = (1, 5)

    self.assertTrue(isinstance(msg, tuple))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_set_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple set.
    """
    msg = set([1, 5, 50, "alpha"])

    self.assertTrue(isinstance(msg, set))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_frozenset_succeeds(self):
    """
    Test that the _prompt() method is successful if given a simple frozenset.
    """
    msg = frozenset([-5, 5, 5.0, "beta"])

    self.assertTrue(isinstance(msg, frozenset))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % str(msg))


  def test_prompt_msg_listparam_invalid_fails(self):
    """
    Test that the _prompt() method fails if given a list with an invalid parameter in it.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Unexpected parameter 'foo'"

    self.assertEquals(
      self.prompt._prompt(self.response, [
        { "say" : "valid" },
        { "foo" : "bar" }
      ]),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "valid\n")


  def test_prompt_msg_list_empty_fails(self):
    """
    Test that the _prompt() method fails if given an empty list.
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

    self.assertEquals(self.output.getvalue(), "%s\n" % ("\n".join([str(m) for m in msg])))


  def test_prompt_msg_listsay_succeeds(self):
    """
    Test that the _prompt() method is successful if given multiple, simple strings.
    """
    msg = [
      { "say" : "a" },
      { "say" : "B" },
      { "say" : -20 },
      { "say" : 5.5 },
    ]

    self.assertTrue(isinstance(msg, list))

    self.assertEquals(
      self.prompt._prompt(self.response, msg),
      self.expected
    )

    self.assertEquals(self.output.getvalue(), "%s\n" % ("\n".join([str(m['say']) for m in msg])))




  # run(tmp=None, task_vars=None)

  def test_run_msg_missing_fails(self):
    """
    Test that the run() method will fail if missing the msg parameter.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Required 'msg' parameter missing."

    del(self.expected['changed'])

    prompt = self._getPrompt()

    prompt.setOutput(self.output)

    self.assertEquals(
      prompt.run(),
      self.expected
    )


  def test_run_multiple_params_fails(self):
    """
    Test that the run() method will fail if there are too many parameters.
    """
    self.expected['failed'] = True
    self.expected['msg'] = "Expected single 'msg' parameter. Multiple parameters given."

    del(self.expected['changed'])

    prompt = self._getPrompt()

    prompt.setOutput(self.output)
    prompt._task.args = {
      "msg" : "Hello World",
      "foo" : "bar"
    }

    self.assertEquals(
      prompt.run(),
      self.expected
    )


  def test_run_singlemessage_valid(self):
    """
    Test that the run() method will fail if there are too many parameters.
    """
    del(self.expected['changed'])

    prompt = self._getPrompt()

    prompt.setOutput(self.output)
    prompt._task.args = {
      "msg" : "Hello World"
    }

    self.assertEquals(
      prompt.run(),
      self.expected
    )

    self.assertEquals(
      self.output.getvalue(),
      "Hello World\n"
    )


  def test_run_multimessage_valid(self):
    """
    Test that the run() method will fail if there are too many parameters.
    """
    del(self.expected['changed'])

    prompt = self._getPrompt()

    prompt.setOutput(self.output)
    prompt._task.args = {
      "msg" : [
        "Hello World",
        "Hi there"
      ]
    }

    self.assertEquals(
      prompt.run(),
      self.expected
    )

    self.assertEquals(
      self.output.getvalue(),
      "Hello World\nHi there\n"
    )
