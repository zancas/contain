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
BASE = COMMUNITY.joinpath("base")

# PROFILE ACQUISITION
HOME = os.environ["HOME"]
PERSONAL_PROFILE = pathlib.Path(HOME).joinpath(".containment")
PROJECTS_PATH = PERSONAL_PROFILE.joinpath("projects")

# PROJECT ACQUISITION
PROJECT_PATH = PROJECTS_PATH.joinpath(PROJECT_NAME)
TAG = f"containment/{PROJECT_NAME}"
DOCKERFILE = PROJECT_PATH.joinpath("Dockerfile")

# CONFIGURATION STRING VARIABLE VALUES
COMMUNITY_ROOTDIRNAME = COMMUNITY_ROOT_PATH.as_posix()
USER = os.environ["USER"]
SHELL = os.environ["SHELL"]
USERID = subprocess.getoutput("id -u")
GENERAL_PERSONAL_PACKAGES = ["vim", "tmux", "git"] # These are examples.

# CONFIGURATION STRINGS
APT_PACKAGES = "RUN     apt-get install -y "+" ".join(GENERAL_PERSONAL_PACKAGES)
PROJ_PLUGIN = \
f"""RUN     useradd --uid 1000 --home /home/{USER} {USER}
COPY    ./entrypoint.sh entrypoint.sh
RUN     chmod +x entrypoint.sh"""
ENTRYPOINT = f"""#! {SHELL}
cd {COMMUNITY_ROOTDIRNAME}
exec {SHELL}"""
RUNSCRIPT = \
f"""docker run -it \
               -v {HOME}:{HOME} \
               -v {COMMUNITY_ROOTDIRNAME}:{COMMUNITY_ROOTDIRNAME} \
               --entrypoint=/entrypoint.sh -u {USER} {TAG}:latest"""


EXTERNALBASIS = ("ubuntu@sha256:9ee3b83bcaa383e5e3b657f042f4034c92cdd50c03f731"
                 "66c145c9ceaea9ba7c")
BASETEXT = f"""FROM    {EXTERNALBASIS}
RUN     apt-get update && apt-get -y install sudo"""

# docker config

client = docker.from_env()
dbuildapi = client.api.build

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
    BASE.write_text(BASETEXT)


def _assure_config():
    if not COMMUNITY.is_dir():
        pave_community()
    if not PERSONAL_PROFILE.is_dir():
        pave_profile()
    if not PROJECT_PATH.is_dir():
        pave_project(PROJECT_PATH.as_posix())

def _write_dockerfile():
    docker_text = _assemble_dockerfile()
    DOCKERFILE.write_text(docker_text)

def _assemble_dockerfile():
    BASELAYER = BASE.read_text()
    DOCKERTEXT = '\n'.join([BASELAYER,
                            APT_PACKAGES,
                            PROJ_PLUGIN])
    return DOCKERTEXT
        

def _assure_build():
    build_actions = []
    for a in dbuildapi(PROJECT_PATH.as_posix()):
        build_actions.append(a)
    

def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    _assure_config() 
    _assure_build()
    
