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

# COMMUNITY ACQUISITION
COMMUNITY_ROOT_PATH = pathlib.Path(os.getcwd())
PROJECT_NAME = COMMUNITY_ROOT_PATH.name
COMMUNITY = COMMUNITY_ROOT_PATH.joinpath(".containment")

# PROFILE ACQUISITION
HOME = os.environ["HOME"]
PERSONAL_PROFILE = pathlib.Path(HOME).joinpath(".containment")
PROJECTS_PATH = PERSONAL_PROFILE.joinpath("projects")

# PROJECT ACQUISITION
PROJECT_PATH = PROJECTS_PATH.joinpath(PROJECT_NAME)
TAG = f"containment/{PROJECT_NAME}"

# CONFIGURATION STRING VARIABLE VALUES
COMMUNITY_ROOTDIRNAME = COMMUNITY_ROOT_PATH.as_posix()
USER = os.environ["USER"]
SHELL = os.environ["SHELL"]
USERID = subprocess.getoutput("id -u")
GENERAL_PERSONAL_PACKAGES = ["vim", "tmux", "git"] # These are examples.

# CONFIGURATION STRINGS
APT_PACKAGES = "RUN    apt-get install -y "+" ".join(GENERAL_PERSONAL_PACKAGES)
PROJ_PLUGIN = \
f"""RUN     useradd --uid 1000 --home /home/{USER} {USER}
COPY    ./entrypoint.sh entrypoint.sh
RUN     chmod +x entrypoint.sh"""
DOCKERFILE_TEMPLATE = '\n'.join([APT_PACKAGES, PROJ_PLUGIN])
ENTRYPOINT = f"""#! {SHELL}
cd {COMMUNITY_ROOTDIRNAME}
exec {SHELL}"""
RUNSCRIPT = \
f"""docker run -it \
               -v {HOME}:{HOME} \
               -v {COMMUNITY_ROOTDIRNAME}:{COMMUNITY_ROOTDIRNAME} \
               --entrypoint=/entrypoint.sh -u {USER} {TAG}:latest"""

EXTERNALBASIS = ("ubuntu@sha256:66126c48f804cc6ea441ce48bd592d4c6535b95e752af4"
                 "d2596f5dbe66cdd209")
BASE = f"""FROM {EXTERNALBASIS}
RUN apt-get update && apt-get -y install sudo"""

def pave_profile():
    """
    Usage:
      containment pave_profile
    """
    PERSONAL_PROFILE.mkdir()
    json.dump(
        GENERAL_PERSONAL_PACKAGES,
        PERSONAL_PROFILE.joinpath("packages.json").open(mode='w')
    )
    PROJECTS_PATH.mkdir()


def pave_project(target_project_name):
    """
    Usage:
      containment pave_project <target_project_name>
    """
    print(target_project_name)
    project_path = pathlib.Path(target_project_name)
    project_path.mkdir()
    _write_dockerfile()
    project_path.joinpath("entrypoint.sh").write_text(ENTRYPOINT)
    project_path.joinpath("run_containment.sh").write_text(RUNSCRIPT)
    project_path.joinpath("packages.json").write_text("[]")


def pave_community():
    """
    Usage:
      containment pave_community
    """
    COMMUNITY.mkdir()
    basefile = COMMUNITY.joinpath("base")
    basefile.write_text(BASE)


def _assure_project():
    if not PERSONAL_PROFILE.is_dir():
        pave_profile()
    if not PROJECT_PATH.is_dir():
        pave_project(PROJECT_PATH.as_posix())
    if not COMMUNITY.is_dir():
        pave_community()

def _write_dockerfile():
    docker_text = _assemble_dockerfile()
    PROJECT_PATH.joinpath("Dockerfile").write_text(docker_text)

def _assemble_dockerfile():
    return "community_layer = "
        

def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    _assure_project() 
    # These are paths that point to a dir inside home
    """personal_projs = personal.joinpath("projects")
    personal_proj = personal_projs.joinpath(COMMUNITY_ROOT_PATH.name)
    print(personal_proj.as_posix())
    
    dclient = docker.from_env()
    proj_name = COMMUNITY_ROOT_PATH.name
    community_base = COMMUNITY_ROOT_PATH.joinpath('.containment').joinpath('base')
    if not community_base.is_file():
        # Create the base file since it did not exist
        pave_community(COMMUNITY_ROOT_PATH)
    base_string = community_base.read_text()
    if not PROJECTS.is_dir():
        pave_personal(proj_name)
    personal_projdir = PROJECTS.joinpath(proj_name)
    personal_prefs = personal_projdir.joinpath("personal_layer")
    personal_string = personal_prefs.read_text()
    dockerfilestringIO = io.StringIO('\n'.join([base_string, personal_string]))
    print(dockerfilestringIO)"""
