# -*- coding: utf-8 -*-
"""The pave command-function, which is usually called internally by activate.

Functions:
    pave:  Create and populate a new ~/.containment directory
"""

# If the wardrobe is assembled then the EXTERNALBASIS is
import os
import pathlib

WARDROBE = pathlib.Path(os.environ["HOME"]).joinpath(".containment")
DEFAULTS = WARDROBE.joinpath("defaults")
BASIS = DEFAULTS.joinpath("basis.json")
STAGE = pathlib.Path(os.environ["PWD"]).joinpath(".containment")
EXTERNALBASIS = ("ubuntu@sha256:d3fdf5b1f8e8a155c17d5786280af1f5a04c10e9514"
                 "5a515279cf17abdf0191f")


def _assemble_default_wardrobe():
    DEFAULTS.mkdir(parents=True)
    BASIS.write_text( '"' + EXTERNALBASIS + '"' )


def pave():
    """
    Usage:
      containment pave
    """
    if WARDROBE.is_dir():
        return
    else:  # This is the first use by this User!!
        _assemble_default_wardrobe()
        print(os.environ["HOME"])



        #  if STAGE == WARDROBE:  # User is home, there is no project. 
