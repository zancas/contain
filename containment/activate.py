# -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""

import os
import pathlib
import subprocess

from .pave import PROJECTS
from .pave import pave_community
from .pave import pave_personal
from .types import ProjectId


def activate(project: ProjectId = None):
    """
    Usage:
      containment activate [<project>]

    Arguments:
      <project>  The name of the project to activate.
    """
    print(_get_project_path(project))
    proj_path = _get_project_path(project)
    proj_name = proj_path.name
    print(proj_name)
    proj_base = proj_path.joinpath('.containment').joinpath('base')
    if not proj_base.is_file():
        # Create the base file since it did not exist
        pave_community(proj_path)
    base_string = proj_base.read_text()
    if not PROJECTS.is_dir():
        pave_personal(proj_name)

    personal_string = PROJECTS\
                      .joinpath(proj_name)\
                      .joinpath("personal").read_text()
    dockerfiletext = '\n'.join([base_string, personal_string])
    print(dockerfiletext)
    

def _get_project_path(project: ProjectId):
    """Find the path of the project based on the project name."""
    if not project:
        return pathlib.Path(os.getcwd())
    project_path = next(
        (p for p in projects_path.iterdir() if p == project),
        None
        )
    if not project_path:
        raise ValueError('Unknown project "{}"'.format(project))
    return pathlib.Path(project_path)
