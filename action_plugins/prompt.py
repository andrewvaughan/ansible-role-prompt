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


__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
  """
  Prompts user with one-or-more messages and optionally waits for input for each.
  """

  TRANSFERS_FILES = False
  VALID_ARGS = frozenset(('say', 'ask', 'multi'))


  def run(self, tmp=None, task_vars=None):
    """
    Runs the plugin.
    """

    if task_vars is None:
        task_vars = dict()

    result = super(ActionModule, self).run(tmp, task_vars)
    args = self._task.args

    # Check for any invalid arguments
    for arg in args:
      if arg not in self.VALID_ARGS:
        return self._fail("'%s' is not a valid argument for prompt", arg)

    # We are running multiple prompts
    if 'multi' in args:

      # If any other arguments exist, throw an exception
      if len(args) != 1:
        return self._fail("'multi' cannot be combined with additional arguments.")

      if not isinstance(args['multi'], list):
        return self._fail("'multi' must be a list of individual messages.")

      for subargs in args['multi']:
        self._prompt(subargs)

    # Otherwise, run a single prompt
    else:
      self._prompt(args)

    return result




  def _prompt(self, args):
    """
    Prompts the user with a message and optionally asks for a response.

      @param args : the arguments for the prompt
    """

    # Support a list of lines for the 'say' command
    if isinstance(args['say'], list):
      for line in args['say']:
        print line

    else:
      print args['say']



  def _fail(self, message, *args):
    """
    Raises an Ansible exception with a given message.

      @param message : the message to pass to the Ansible exception
      @param args    : an arbitrary number of arguments to replace in the message's formatting

      @return an object containing a failure exception for Ansible to be returned
    """

    return {
      "failed" : True,
      "msg"    : message % (args)
    }
