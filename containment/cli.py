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

PROJECT_PATH = pathlib.Path(os.getcwd())
PROJECT_NAME = PROJECT_PATH.name
TAG = f"containment/{PROJECT_NAME}"
PROJECT_DIR = PROJECT_PATH.as_posix()
USER = os.environ["USER"]
SHELL = os.environ["SHELL"]
USERID = subprocess.getoutput("id -u")
HOME = os.environ["HOME"]
PERSONAL = pathlib.Path(HOME).joinpath(".containment")
PERSONAL_PROJECTS_PATH = PERSONAL.joinpath("projects")

GENERAL_PERSONAL_PACKAGES = ["vim", "tmux", "git"] # These are examples.

APT_PACKAGES = "RUN    apt-get install -y "+" ".join(GENERAL_PERSONAL_PACKAGES)
PROJ_PLUGIN = \
f"""RUN     useradd --uid 1000 --home /home/{USER} {USER}
COPY    ./entrypoint.sh entrypoint.sh
RUN     chmod +x entrypoint.sh"""
DOCKERFILE_TEMPLATE = '\n'.join([APT_PACKAGES, PROJ_PLUGIN_TEMPLATE.format()])
ENTRYPOINT = f"""#! {SHELL}
cd {PROJECT_DIR}
exec {SHELL}"""
RUNSCRIPT = \
f"""docker run -it -v {HOME}:{HOME} -v {PROJECT_DIR}:{PROJECT_DIR} \
   --entrypoint=/entrypoint.sh -u {USER} {TAG}:latest"""

def pave_profile():
    """
    Usage:
      containment pave_profile
    """
    

def pave_community():
    """
    Usage:
      containment pave_community
    """


def pave_project(project: ProjectId = None):
    """
    Usage:
      containment pave_project <project>
    """

def _assure_personal():
    if not PERSONAL.is_dir():
        PERSONAL.mkdir()
        json.dump(
            GENERAL_PERSONAL_PACKAGES,
            PERSONAL.joinpath("packages.json").open(mode='w')
        )
        PERSONAL_PROJECTS_PATH.mkdir()
    # _assure_profile even if personal already exists
    _assure_profile()

def _assure_profile():
    current_proj = PERSONAL_PROJECTS_PATH.joinpath(PROJECT_NAME)
    if not current_proj.is_dir():
        current_proj.mkdir()
        current_proj.joinpath("entrypoint.sh").write_text(ENTRYPOINT)
        current_proj.joinpath("packages.json").write_text("[]")
        _write_dockerfile()

def _write_dockerfile():
    docker_text = _assemble_dockerfile()
    current_proj.joinpath("Dockerfile").write_text(docker_text)

def _assemble_dockerfile():
    community_layer = 
        

def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    _assure_personal() 
    # These are paths that point to a dir inside home
    """personal_projs = personal.joinpath("projects")
    personal_proj = personal_projs.joinpath(PROJECT_PATH.name)
    print(personal_proj.as_posix())
    
    dclient = docker.from_env()
    proj_name = PROJECT_PATH.name
    community_base = PROJECT_PATH.joinpath('.containment').joinpath('base')
    if not community_base.is_file():
        # Create the base file since it did not exist
        pave_community(PROJECT_PATH)
    base_string = community_base.read_text()
    if not PROJECTS.is_dir():
        pave_personal(proj_name)
    personal_projdir = PROJECTS.joinpath(proj_name)
    personal_prefs = personal_projdir.joinpath("personal_layer")
    personal_string = personal_prefs.read_text()
    dockerfilestringIO = io.StringIO('\n'.join([base_string, personal_string]))
    print(dockerfilestringIO)"""
