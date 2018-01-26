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
Test suite for the Ansible Prompt action plugin pertaining to :func:`run`.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import mock

from test import PromptTestAbstract


class TestPromptRun(PromptTestAbstract):
    """
    Tests the :func:`run` method in the Prompt plugin.

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.4.0
       Separated into separate test class.

    .. class:: TestPromptRun
    """

    def test_Prompt_run_msg_missing_fails(self):
        """
        Test that :func:`run` will fail if missing the msg parameter.

        .. versionadded:: 0.1.0

        .. versionchanged:: 0.4.0
           Switched to use helper method.

        .. function:: test_Prompt_run_msg_missing_fails()
        """
        self._testRunFailure("Required 'msg' parameter missing.")


    def test_Prompt_run_msg_multiples_fails(self):
        """
        Test that :func:`run` will fail if there is more than one parent parameter.

        .. versionadded:: 0.1.0

        .. versionchanged:: 0.4.0
           Switched to use helper method.

        .. function:: test_Prompt_run_msg_multiples_fails()
        """
        self.prompt.setTaskArguments({
            'msg': 'Hello World',
            'foo': 'bar',
        })

        self._testRunFailure("Expected single 'msg' parameter. Multiple parameters given.")


    def test_Prompt_run_should_call_ActionBase_super_run(self):
        """
        Test that the `super` :func:`run` is called from the ActionBase.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_run_should_call_ActionModule_super_run()
        """
        with mock.patch('action_plugins.prompt.ActionBase.run', return_value=dict()) as mock_super:
            self.prompt.run()
            self.assertTrue(mock_super.called)


    def test_Prompt_run_should_call_helper_prompt_with_args(self):
        """
        Test that :func:`run` calls :func:`_prompt` on a successful setup.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_run_should_call_helper_prompt_with_args()
        """
        with mock.patch('action_plugins.Prompt._prompt', return_value="Success!") as mock_helper:
            self.prompt.setTaskArgument('msg', 'Hello World')

            self.assertEquals(
                self.prompt.run(),
                'Success!'
            )

            self.assertTrue(mock_helper.called)


    def _testRunFailure(self, msg, tmp=None, task_vars=None):
        """
        Test that the run() method fails with a particular message.

        :kwarg tmp: the temporary directory to use if creating files
        :kwarg task_vars: any variables associated with the task

        .. versionadded:: 0.4.0

        .. function:: _testRunFailure(msg)
        """
        self.expected['failed'] = True
        self.expected['msg'] = msg

        del(self.expected['changed'])

        self.assertEquals(
            self.prompt.run(
                tmp=tmp,
                task_vars=task_vars
            ),
            self.expected
        )


    # def test_Prompt_run_singlemessage_valid(self):
    #     """
    #     Test that the run() method will succeed with a single message.
    #
    #     .. versionadded:: 0.1.0
    #
    #     .. function:: test_Prompt_run_singlemessage_valid()
    #     """
    #     del(self.expected['changed'])
    #
    #     prompt = self._getPrompt()
    #
    #     prompt.setOutput(self.outstr)
    #     prompt._task.args = {
    #         "msg": "Hello World"
    #     }
    #
    #     self.assertEquals(
    #         prompt.run(),
    #         self.expected
    #     )
    #
    #     self.assertEquals(
    #         self.outstr.getvalue(),
    #         "Hello World\n"
    #     )
    #
    #
    # def test_prompt_run_multimessage_valid(self):
    #     """
    #     Test that the run() method will succeed with a multiple messages.
    #
    #     .. versionadded:: 0.1.0
    #     .. function:: test_run_multimessage_valid()
    #     """
    #     del(self.expected['changed'])
    #
    #     prompt = self._getPrompt()
    #
    #     prompt.setOutput(self.outstr)
    #     prompt._task.args = {
    #         "msg": [
    #             "Hello World",
    #             "Hi there"
    #         ]
    #     }
    #
    #     self.assertEquals(
    #         prompt.run(),
    #         self.expected
    #     )
    #
    #     self.assertEquals(
    #         self.outstr.getvalue(),
    #         "Hello World\nHi there\n"
    #     )
    #
    #
    # def test_prompt_run_saynewlinemultiple_valid(self):
    #     """
    #     Test that the run() method will succeed with a multiple messages.
    #
    #     .. versionadded:: 0.3.0
    #     .. function:: test_prompt_run_saynewlinemultiple_valid()
    #     """
    #     del(self.expected['changed'])
    #
    #     prompt = self._getPrompt()
    #
    #     prompt.setOutput(self.outstr)
    #     prompt._task.args = {
    #         "msg": [
    #             {
    #                 "say": "Hello ",
    #                 "newline": False,
    #             },
    #             {
    #                 "say": "World",
    #                 "newline": True,
    #             }
    #         ]
    #     }
    #
    #     self.assertEquals(
    #         prompt.run(),
    #         self.expected
    #     )
    #
    #     self.assertEquals(
    #         self.outstr.getvalue(),
    #         "Hello World\n"
    #     )
    #
    #
    # def test_prompt_run_align_left_valid(self):
    #     """
    #     Test that the run() method is successful with a left alignment.
    #
    #     .. versionadded:: 0.3.0
    #     .. function:: test_prompt_run_align_left_valid()
    #     """
    #     del(self.expected['changed'])
    #
    #     prompt = self._getPrompt()
    #
    #     prompt.setOutput(self.outstr)
    #     prompt._task.args = {
    #         "msg": [
    #             {
    #                 "say": "Hello World",
    #                 "align": "left",
    #             }
    #         ]
    #     }
    #
    #     self.assertEquals(
    #         prompt.run(),
    #         self.expected
    #     )
    #
    #     self.assertEquals(
    #         self.outstr.getvalue(),
    #         "Hello World\n"
    #     )
    #
    #
    # def test_prompt_run_align_center_valid(self):
    #     """
    #     Test that the run() method is successful with a center alignment.
    #
    #     .. versionadded:: 0.3.0
    #     .. function:: test_prompt_run_align_center_valid()
    #     """
    #     with mock.patch('subprocess.check_output', return_value='10 88'):
    #         del(self.expected['changed'])
    #
    #         prompt = self._getPrompt()
    #
    #         prompt.setOutput(self.outstr)
    #         prompt._task.args = {
    #             "msg": [
    #                 {
    #                     "say": "Hello World",
    #                     "align": "center",
    #                     "newline": False,
    #                 }
    #             ]
    #         }
    #
    #         self.assertEquals(
    #             prompt.run(),
    #             self.expected
    #         )
    #
    #         self.assertEquals(
    #             self.outstr.getvalue(),
    #             "Hello World".center(88)
    #         )
    #
    #
    # def test_prompt_run_align_right_valid(self):
    #     """
    #     Test that the run() method is successful with a right alignment.
    #
    #     .. versionadded:: 0.3.0
    #     .. function:: test_prompt_run_align_right_valid()
    #     """
    #     with mock.patch('subprocess.check_output', return_value='10 52'):
    #         del(self.expected['changed'])
    #
    #         prompt = self._getPrompt()
    #
    #         prompt.setOutput(self.outstr)
    #         prompt._task.args = {
    #             "msg": [
    #                 {
    #                     "say": "Hello World",
    #                     "align": "right",
    #                     "newline": False,
    #                 }
    #             ]
    #         }
    #
    #         self.assertEquals(
    #             prompt.run(),
    #             self.expected
    #         )
    #
    #         self.assertEquals(
    #             self.outstr.getvalue(),
    #             "Hello World".rjust(52)
    #         )
