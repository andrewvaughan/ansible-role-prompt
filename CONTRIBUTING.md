# Contributing

The Ansible Prompt plugin would not exist without its contributors, and we welcome you to join us in our endeavor.
This guide is intended for anyone who wants to contribute to [Ansible Prompt Plugin][project-url]. Please read this
document carefully before contributing, as it answers many of the questions that new contributors have when first
working with our projects.

## Agreement

By submitting any work to this project, you agree to our [project license][license-url] as well as to the following
principal guidelines:

1. Any work contributed is original work, or you otherwise have the right to submit the work;
1. You grant this project and its members a non-exclusive, irrevocable license to use your submitted work in any way; and,
1. You are capable of granting these rights for the contribution.

## Ways to Contribute

There are many ways to contribute to this project:

* **Report a Bug** - if you find a bug, please [file a detailed issue](#bug-reports)
* **Request a Feature** - if you want to request a feature, please [submit a request](#feature-requests)
* **Work on an Issue** - if you wish to contribute directly, please feel free to work on [any open issue](#working-on-issues)

### Bug Reports

Perfect code is rare, and this project is no exception.  If you find a bug, or feel something is acting strangely,
please [file an issue][issues-url] so that it can be addressed.  When filing an issue, please provide the following
information:

* What version of the project you were using
* What you did
* What you expected to happen
* What actually happened

### Feature Requests

We love ideas of any form.  Even if you can't add a feature on your own, we welcome all suggestions.  When making
a feature request, please [file an issue][issues-url] and provide the following information:

* The feature you want to add or problem you want to solve
* Your take on the correct approach to building the new functionality

## Working on Issues

All bugs and features are stored in our [GitHub Issues][issues-url] section. It is here that we determine which issues
will be road-mapped for various releases, and plan our [milestones][milestones-url] accordingly.  All issues that are
received will be reviewed by the core development staff and assigned a milestone for release.

If you intend to work on a specific issue, please add a comment to the issue saying so and indicate when you think
you will complete it.  This will help us to avoid duplication of effort.  If you find that you cannot finish the
work, simply add a comment letting people know so someone else can pick it up.

### Pull Requests

All contributions to this project must go through a [GitHub Pull Request][pulls-url].  In addition, all Pull Requests
must be directly related to an open issue.  All pull requests should follow a very specific process:

**1. Open or choose an issue to work on**

Before working, please identify or create an issue for what you are looking to contribute.  **Note** that only
accepted issues will be merged, and if your issue is not slated for a milestone it may not be accepted.  You may
request that the issue be identified for release before you begin working.

**2. Announce that you will be working on that issue**

Let us know when you plan to start on the issue and how long you think it will take you.  This will help us be ready
to support you when it comes time to review.

**3. Fork the project repository**

Every contributor, including core staff, is required to work within a fork of their own repository.  All branches on
the main repository are meant for production purposes only.

**4. Add the project upstream remote**

In order to keep your code up to date with master, you need to add the project's main repository as your upstream:

```bash
git remote add upstream https://github.com/andrewvaughan/ansible-prompt module
```

**5. Ensure that your master branch is up to date with the upstream**

```bash
git checkout master
git pull upstream master
```

**6. Create a new branch**

Create a branch on your local repository that has a descriptive name of what you are fixing, such as:

```bash
git checkout -b fix-broken-config
git push -u origin fix-broken-config
```

**7. Make your changes**

Make your changes, commit, and add tests!  All features must be tested to completion before they will be accepted.
This project makes use of automated testing tools to provide thorough testing and code-style rules to ensure
consistency across the project.

Please refer to our [code standards](#code-style-requirements) to save yourself time when testing!

**8. Rebase onto upstream**

Before you send a pull request, be sure to rebase onto the upstream source.  This ensures your code is running on
the latest available code.

```bash
git fetch upstream
git rebase upstream/master
```

**9. Ensure all tests pass**

After rebasing, be sure to run the test suite to make sure nothing is broken.

**10. Squash your commits**

Commits on the production environment are used as a change log for releases.  As such, commits must be
[squashed][squash-support] to a single commit before being accepted.

On the last step of your rebase, all commit messages must follow a specific standard to be accepted:

```
Tag: Message (fixes #issueno)
```

In this case, `Tag` is one of the following:

* `Fix` - for a bug fix
* `Update` - for any update to existing functionality
* `New` - for any new functionality
* `Docs` - for documentation updates
* `Build` - for changes to build or automation
* `Upgrade` - for dependency upgrades

Generally, you can find this tag as one of the labels on the issue you are fixing.  The `Message` should be a
one-sentence description of the change.  Finally, the issue number the Pull Request represents should be mentioned at
the end.  If the commit does not completely resolve the issue, please use `(refs #1234)` instead of `(fixes #1234)`.

Here are some good examples:

```
Build: Added new Python version to Travis-CI config (fixes #19)
Fix: Resolved bug due to extra semicolon (fixes #220)
Upgrade: Upgraded (some pip module) from 1.0.0 to 1.1.0 (fixes #999)
```

**11. Submit a Pull Request**

You're ready to submit your pull request!  Refer to the [GitHub documentation][pull-support] on how best to send a
pull request from your fork.

**12. Watch for status**

All Pull Requests must pass comprehensive testing.  If the build passes or fails, it will show up on the Pull
Request.  We cannot accept any Pull Requests that fail our criteria for a build, so if that happens, please fix and
re-squash your commits, and then update the Pull Request to trigger another build.

## Code Style Requirements

All code provided to this project must follow a strict set of code standards to prevent unnecessary commit logs from
being introduced due to formatting.  The project codebase is checked against linting rules before running unit
tests.

Before submitting a Pull Request, all tests must be run, provide full coverage of functionality, and successfully
pass before a request will be reviewed.

### Standards Subject to Change

With every Pull Request, the core team has the opportunity to better refine our style and acceptance guidelines.  As
such, you may be requested to pull an updated set of code style guidelines due to an unforeseen inconsistency in
submitted code, and to resubmit your request according to the new guidelines.


[project-url]:    https://github.com/andrewvaughan/ansible-prompt
[license-url]:    https://github.com/andrewvaughan/ansible-prompt/blob/master/LICENSE
[issues-url]:     https://github.com/andrewvaughan/ansible-prompt/issues
[milestones-url]: https://github.com/andrewvaughan/ansible-prompt/milestones
[pulls-url]:      https://github.com/andrewvaughan/ansible-prompt/pulls

[squash-support]: http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html
[pull-support]:   https://help.github.com/articles/creating-a-pull-request
