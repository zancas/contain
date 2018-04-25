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
import sys
import time

import docker

from .types import ProjectId

# COMMUNITY ACQUISITION
COMMUNITY_ROOT_PATH = pathlib.Path(os.getcwd())
PROJECT_NAME = COMMUNITY_ROOT_PATH.name
COMMUNITY = COMMUNITY_ROOT_PATH.joinpath(".containment")
BASE = COMMUNITY.joinpath("base")
COMMUNITY_PACKAGES = COMMUNITY.joinpath("packages.json")

# PROFILE ACQUISITION
HOME = os.environ["HOME"]
PROFILE = pathlib.Path(HOME).joinpath(".containment")
PROJECTS_PATH = PROFILE.joinpath("projects")

# PROJECT ACQUISITION
PROJECT = PROJECTS_PATH.joinpath(PROJECT_NAME)
TAG = f"containment/{PROJECT_NAME}"
DOCKERFILE = PROJECT.joinpath("Dockerfile")
RUNFILE = PROJECT.joinpath("run_containment.sh")
ENTRYPOINTFILE = PROJECT.joinpath("entrypoint.sh")
PROJECTPACKAGES = PROJECT.joinpath("packages.json")
#PROJPACKAGES = json.load(PACKAGESFILE.open())

# CONFIGURATION STRING VARIABLE VALUES
COMMUNITY_ROOTDIRNAME = COMMUNITY_ROOT_PATH.absolute().as_posix()
USER = os.environ["USER"]
SHELL = os.environ["SHELL"]
USERID = subprocess.getoutput("id -u")
DOCKERGID = subprocess.getoutput("grep docker /etc/group").split(':')[2]
GENERAL_PERSONAL_PACKAGES = ["vim", "tmux", "git"] # These are examples.

# CONFIGURATION STRINGS
PROJ_PLUGIN = \
f"""RUN     useradd -G docker --uid 1000 --home /home/{USER} {USER}
RUN     echo {USER} ALL=\(ALL\) NOPASSWD: ALL >> /etc/sudoers
COPY    ./entrypoint.sh entrypoint.sh
RUN     chmod +x entrypoint.sh"""
ENTRYPOINT = f"""#! {SHELL}
cd {COMMUNITY_ROOTDIRNAME}
exec {SHELL}"""
RUNSCRIPT = \
f"""docker run -it \
               -v /var/run/docker.sock:/var/run/docker.sock \
               -v {HOME}:{HOME} \
               -v {COMMUNITY_ROOTDIRNAME}:{COMMUNITY_ROOTDIRNAME} \
               --entrypoint=/entrypoint.sh -u {USER}:{DOCKERGID} {TAG}:latest"""


EXTERNALBASIS = ("ubuntu@sha256:9ee3b83bcaa383e5e3b657f042f4034c92cdd50c03f731"
                 "66c145c9ceaea9ba7c")
BASETEXT = f"""FROM    {EXTERNALBASIS}
RUN     apt-get update && apt-get install -y sudo docker.io"""

# docker config

client = docker.from_env()
dbuildapi = client.api.build

PKG_INSTALL_CMDS = {"debian": "apt-get install -y",
                    "ubuntu": "apt-get install -y"}


def _generate_RUN_install_commands(package_file):
    """
    take in a dict return a string of docker build RUN directives
    one RUN per package type
    one package type per JSON key
    """
    packages = ' '.join(json.load(package_file.open()))
    if packages:
        for packager in PKG_INSTALL_CMDS:
            if packager in EXTERNALBASIS:
                installer = PKG_INSTALL_CMDS[packager]
        return f'RUN    {installer} {packages}'
    else:
        return ''


def pave_profile():
    """
    Usage:
      containment pave_profile
    """
    PROFILE.mkdir()
    json.dump(
        GENERAL_PERSONAL_PACKAGES,
        PROFILE.joinpath("packages.json").open(mode='w')
    )
    PROJECTS_PATH.mkdir()


def pave_project(target_project_name):
    """
    Usage:
      containment pave_project <target_project_name>
    """
    print("Inside pave_project")
    project_path = pathlib.Path(target_project_name)
    project_path.mkdir()
    ENTRYPOINTFILE.write_text(ENTRYPOINT)
    RUNFILE.write_text(RUNSCRIPT)
    print("about to write to ", PROJECTPACKAGES.absolute().as_posix())
    PROJECTPACKAGES.write_text("[]")
    write_dockerfile()


def pave_community():
    """
    Usage:
      containment pave_community
    """
    print("pave_community is executing!!")
    COMMUNITY.mkdir()
    BASE.write_text(BASETEXT)
    COMMUNITY_PACKAGES.write_text("[]")


def _assure_config():
    if not COMMUNITY.is_dir():
        pave_community()
    if not PROFILE.is_dir():
        pave_profile()
    if not PROJECT.is_dir():
        pave_project(PROJECT.absolute().as_posix())


def write_dockerfile():
    """
    Usage:
      containment write_dockerfile  
    """
    docker_text = _assemble_dockerfile()
    DOCKERFILE.write_text(docker_text)


def _assemble_dockerfile():
    BASE_LAYER = BASE.read_text()
    COMMUNITY_LAYER = \
        _generate_RUN_install_commands(COMMUNITY.joinpath("packages.json")) 
    PROFILE_LAYER = \
        _generate_RUN_install_commands(PROFILE.joinpath("packages.json")) 
    PROJECT_LAYER = \
        _generate_RUN_install_commands(PROJECT.joinpath("packages.json")) 
    DOCKERTEXT = '\n'.join([BASE_LAYER,
                            COMMUNITY_LAYER,
                            PROFILE_LAYER,
                            PROJECT_LAYER,
                            PROJ_PLUGIN])
    return DOCKERTEXT
        

def rebuild():
    """
    Usage:
      containment rebuild
    """
    write_dockerfile()
    build()


def build():
    """
    Usage:
      containment build
    """
    build_actions = []
    for a in dbuildapi(PROJECT.absolute().as_posix(), tag=TAG):
        print(a)
        build_actions.append(a)


def run():
    """
    Usage:
      containment run
    """
    run_string = RUNFILE.read_text()
    run_command = run_string.split()
    chmod_string = "chmod +x " + RUNFILE.absolute().as_posix()
    chmod_run = subprocess.run(chmod_string.split())
    run_subprocess = subprocess.run(run_command,
                                    stdin=sys.stdin,
                                    stdout=sys.stdout,
                                    stderr=sys.stderr)
    

def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    _assure_config() 
    build()
    run()
