# -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""

import json
import os
import pathlib
import subprocess
import time

import docker

from .types import ProjectId

USER = os.environ["USER"]
SHELL = os.environ["SHELL"]
USERID = subprocess.getoutput("id -u")
personal = pathlib.Path(os.environ["HOME"]).joinpath(".containment")

GENERAL_PERSONAL_PACKAGES = ["vim", "tmux", "git"] # These are examples.
DOCKERFILE_TEMPLATE = '\n'.join([PERSONAL_APT_PACKAGES, USER_PROJECT_PLUGIN])
ENTRYPOINT_TEMPLATE = """#! {SHELL}
cd {PROJECT_DIR}
exec {SHELL}"""
RUNSCRIPT_TEMPLATE = \
"""docker run -it -v {HOME}:{HOME} -v {PROJECTDIRNAME}:{PROJECTDIRNAME} \
   --entrypoint=/entrypoint.sh -u {USER} {TAG}:latest"""

def _get_build_id():
    return build_id

def _format_entrypoint(project):
    proj_path = _get_project_path(project)
    PROJECTDIRNAME = proj_path.cwd().name
    return ENTRYPOINT_TEMPLATE.format()

def _assure_personal(project: ProjectId):
    if not personal.is_dir():
        personal.mkdir()
        json.dump(
            GENERAL_PERSONAL_PACKAGES,
            personal.joinpath("packages.json").open(mode='w')
        )
        projects = personal.joinpath("projects")
        projects.mkdir()
        print(type(project))
        print(project)
        _assure_project(projects, project)

def _assure_project(projects, project)
    current_proj = projects.joinpath(project)
    if not current_proj.is_dir():
        current_proj.mkdir()
        current_proj.joinpath("entrypoint.sh").write_text(
            _format_entrypoint(project))

def activate(project: ProjectId = None):
    """
    Usage:
      containment activate [<project>]

    Arguments:
      <project>  The name of the project to activate.
    """
    # This is derived from the clone
    _assure_personal(project) 
    # These are paths that point to a dir inside home
    """personal_projs = personal.joinpath("projects")
    personal_proj = personal_projs.joinpath(proj_path.name)
    print(personal_proj.as_posix())
    
    dclient = docker.from_env()
    proj_name = proj_path.name
    community_base = proj_path.joinpath('.containment').joinpath('base')
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
