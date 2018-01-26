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
Test suite for the Ansible Prompt action plugin pertaining to failure messages.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import unittest

from test import PromptTestAbstract


class TestPromptFail(PromptTestAbstract):
    """
    Tests the the Anisble Prompt action plugin's failure states.

    .. versionadded:: 0.4.0

    .. class:: TestPromptFail
    """

    @unittest.skip("Unimplemented")
    def test_Prompt_fail_result_bad_type_raises(self):
        """
        Test that the :func:`_fail` helper method raises a `TypeError` if `result` is anything other than a `dict`.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_fail_result_bad_type_raises()
        """
        pass


    @unittest.skip("Unimplemented")
    def test_Prompt_fail_message_bad_type_raises(self):
        """
        Test that the :func:`_fail` helper method raises a `TypeError` if `message` is anything other than a `str` or
        `unicode`.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_fail_message_bad_type_raises()
        """
        pass


    @unittest.skip("Unimplemented")
    def test_Prompt_fail_message_empty_raises(self):
        """
        Test that the :func:`_fail` helper method raises a `ValueError` if `message` is blank.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_fail_message_empty_raises()
        """
        pass


    @unittest.skip("Unimplemented")
    def test_Prompt_fail_sets_result(self):
        """
        Test that the :func:`_fail` helper method sets the failure message appropriately.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_fail_sets_result()
        """
        pass


    @unittest.skip("Unimplemented")
    def test_Prompt_fail_templates_arguments_in_result(self):
        """
        Test that the :func:`_fail` helper method adds arguments into a provided template.

        .. versionadded:: 0.4.0

        .. function:: test_Prompt_fail_templates_arguments_in_result()
        """
        pass
