# -*- coding: utf-8 -*-
"""The pave command-function, which is usually called internally by activate.

Functions:
    pave:  Create and populate a new ~/.containment directory

INVARIANT:  After pave runs the contents of the .containment directory are not
modified by the containment pave or activate commands.
"""

# If the wardrobe is assembled then the EXTERNALBASIS is
import os
import pathlib

WARDROBE = pathlib.Path(os.environ["HOME"]).joinpath(".containment")
DEFAULTS = WARDROBE.joinpath("defaults")
BASIS = DEFAULTS.joinpath("basis.json")
EQUIPMENT = DEFAULTS.joinpath("equipment.json")
STAGE = pathlib.Path(os.environ["PWD"]).joinpath(".containment")
EXTERNALBASIS = ("ubuntu@sha256:d3fdf5b1f8e8a155c17d5786280af1f5a04c10e9514"
                 "5a515279cf17abdf0191f")
EQUIPMENT_MANIFEST = '["vim", "ipython", "pytest"]'
USER = os.environ["USER"]
DOCKERFILE_TEMPLATE = f"""FROM {EXTERNALBASIS}
RUN apt update
RUN apt install sudo"""


#RUN adduser --uid `id -u`  {USER}"""  


def _assemble_default_wardrobe():
    DEFAULTS.mkdir(parents=True)
    BASIS.write_text( '"' + EXTERNALBASIS + '"' )
    EQUIPMENT.write_text( EQUIPMENT_MANIFEST )


def _write_entrypoint():
    # Write the defaalt entrypoint into the personal directory.
    pass


def _compose_Dockerfile():
    # Generate the basic dockerfile:
    pass

def pave():
    """
    Usage:
      containment pave
    """
    if not STAGE.is_dir():
        STAGE.mkdir(parents=True, exist_ok=False)
        COMMUNITY_BASE = STAGE.joinpath("base")
        COMMUNITY_BASE.write_text(DOCKERFILE_TEMPLATE)
    
    #else:
        # BASIS is default pump that into the community stage.
    #    print
    if WARDROBE.is_dir():
        print(WARDROBE.name)
        return
    else:  # This is the first use by this User!!
        _assemble_default_wardrobe()
        print(os.environ["HOME"])



        #  if STAGE == WARDROBE:  # User is home, there is no project. 
