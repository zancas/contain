# -*- coding: utf-8 -*-
"""Contains the init command and helper methods.

Functions:
    init: Initialize the current directory as a project and create the
    contain metasource.
"""

import os
from pathlib import Path
import uuid

from rcli.display import run_tasks
from .types import Project

from .exceptions import ProjectAlreadyInitialized

ENTRYPOINT = """#! /bin/bash
useradd $USER -u $USER_ID -G sudo,docker,staff &&\
echo $USER' ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers &&\
exec su - $USER"""

class Project:
    def __init__(self, pathstring):
        self.path = Path(pathstring or '.').absolute()

class Init:
    """
    Usage:
      contain init [<project>]
      contain init (-h | --help)

    Arguments:
      <project>   The name of the project to initialize, this should be a path
                  relative to the current working directory. If no path is
                  supplied the current working directory is used by default.
                  [default: .]

    Options:
      -h, --help  Display this message.
    """
    def __call__(self, project: Project):
        # XXX query the list of projects to see if it includes project
        self.project = project
        return run_tasks(
            'Creating Initial Container for Project {}.'.format(project),
            [self._make_task(f) for f in [
                self.assert_project_not_already_initialized,
                self.write_container_config]])

    def _make_task(self, method):
        """create a run_tasks compliant task"""
        return (method.__doc__, method)

    def assert_project_not_already_initialized(self):
        """determine whether a target project exists"""
        if self.project.path.joinpath('.contain').is_file():
            raise ProjectAlreadyInitialized(self.project.path.absolute())

    def write_container_config(self):
        """Construct a set of container config rules."""
        self.rendered = self._render_config()
        with self.project.path.joinpath('.contain').open(mode='w') as cfh:
            cfh.write(self.rendered)

    def _render_config(self):
        """In the future this might render based on project scan results."""
        pathname = os.path.abspath(os.path.join(os.curdir, str(uuid.uuid4())))
        self.entrypoint = Path(pathname)
        self.entrypoint.write_text(ENTRYPOINT)
        return 'FROM    ubuntu:latest\nENTRYPOINT ["{}"]'.format(pathname)
