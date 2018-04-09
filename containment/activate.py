# -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""

import os
import pathlib
import subprocess
import time

import docker

from .types import ProjectId

USER = os.environ["USER"]
USERID = subprocess.getoutput("id -u")
ENTRYPOINT = f"""#! /bin/bash
mkdir /home/{USER}
useradd --uid {USERID} --home /home/{USER} {USER}
exec su - {USER} $@"""  
personal = pathlib.Path(os.environ["HOME"]).joinpath(".containment")

def _get_build_id():
    return build_id

def _assure_personal():
    if not personal.is_dir():
        personal.mkdir()
        personal.joinpath("projects").mkdir()
        personal.joinpath("entrypoint.sh").write_text(ENTRYPOINT)

def activate(project: ProjectId = None):
    """
    Usage:
      containment activate [<project>]

    Arguments:
      <project>  The name of the project to activate.
    """
    _assure_personal() 
    # This is derived from the clone
    proj_path = _get_project_path(project)
    # These are paths that point to a dir inside home
    personal_projs = personal.joinpath("projects")
    personal_proj = personal_projs.joinpath(proj_path.name)
    print(personal_proj.as_posix())
    
    dclient = docker.from_env()
    proj_name = proj_path.name
    print(proj_name)
    """community_base = proj_path.joinpath('.containment').joinpath('base')
    if not community_base.is_file():
        # Create the base file since it did not exist
        pave_community(proj_path)
    base_string = community_base.read_text()
    if not PROJECTS.is_dir():
        pave_personal(proj_name)
    personal_projdir = PROJECTS.joinpath(proj_name)
    personal_prefs = personal_projdir.joinpath("personal_layer")
    personal_string = personal_prefs.read_text()
    dockerfilestringIO = io.StringIO('\n'.join([base_string, personal_string]))
    print(dockerfilestringIO)"""
                                

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
