# -*- coding: utf-8 -*-
"""Contains the init command and helper methods.

Functions:
    init: Initialize the current directory as a project and create the
    contain metasource.
"""

from pathlib import Path

from rcli.display import run_tasks
from .types import Project

def init(project: Project = '.'):
    """
    Usage:
      contain init [<project>]
      contain init (-h | --help)

    Arguments:
      <project>   The name of the project to initialize, this should be a path
                  relative to the current working directory. If no path is
                  supplied the current working directory is used by default.

    Options:
      -h, --help  Display this message.
    """
    # XXX query the list of projects to see if it includes project
    project_path = Path(project)
    return run_tasks(
        'Creating Initial Container for Project {}.'.format(project),
        [('{}'.format(project), lambda: '{}'.format(project))])
