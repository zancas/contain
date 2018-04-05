# -*- coding: utf-8 -*-
"""The pave command-function, which is usually called internally by activate.

Functions:
    pave:  Create and populate a new ~/.containment directory

INVARIANT:  After pave runs a ~/.containment/projects/{PROJECT} directory
INVARIANT:  
"""

# If the wardrobe is assembled then the EXTERNALBASIS is
import os
import pathlib

from .activate import personal
from .exceptions import ContainmentException
from .types import ProjectId


PROJECTS = personal.joinpath("projects")
EXTERNALBASIS = ("ubuntu@sha256:d3fdf5b1f8e8a155c17d5786280af1f5a04c10e9514"
                 "5a515279cf17abdf0191f")
USER = os.environ["USER"]
BASE_TEMPLATE = f"""FROM {EXTERNALBASIS}
RUN apt update
RUN apt install sudo"""


DEFAULT = """RUN apt remove --purge nano && apt install -y vim"""
ENTRYPOINT = """adduser --uid `id -u` {USER}"""  


def _write_entrypoint():
    # Write the defaalt entrypoint into the personal directory.
    pass


def _compose_Dockerfile():
    # Generate the basic dockerfile:
    pass


def pave(project: ProjectId = None):
    """
    Usage:
      containment pave
    """

    if not project:
        project = pathlib.Path(os.environ['PWD'])
    
    if not project.joinpath('.containment').is_dir():
        pave_community(project)


def pave_community(project):
    community_dir = project.joinpath(".containment")
    community_dir.mkdir(parents=True, exist_ok=False)
    community_dir.joinpath("base").write_text(BASE_TEMPLATE)


def pave_personal(project: ProjectId = None):
    personal_projdir = PROJECTS.joinpath(project)
    if not personal_projdir.is_dir():
        # THIS IS THE FIRST USE OF CONTAINMENT WITH THTS PROJECT!
        personal_projdir.mkdir()
    personal_proj_layer = personal_projdir.joinpath("personal_layer")
    personal_proj_dockerfiles = personal_projdir.joinpath("dockerfiles")
    if not personal_proj_dockerfiles.is_dir():
        personal_proj_dockerfiles.mkdir()
        
    if not personal_proj_layer.is_file():
        personal_proj_layer.parent.mkdir(parents=True, exist_ok=True)
        personal_proj_layer.write_text(f"{DEFAULT}")
    
