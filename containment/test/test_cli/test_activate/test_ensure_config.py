# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import os
from pathlib import Path
import pytest
from unittest import mock

from ....builder import CommandLineInterface
from ....cli.activate import activate as actfun
from ....cli import activate
from ....config import config


def test_pave_project(ensureconfig_mockcli, tmpdir):
    print(dir(config.project_config))
    print(config.project_config.path)
    config.project_config.path = Path(os.path.join(tmpdir, ".containment"))
    print(config.project_config.path)
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=ensureconfig_mockcli) as CLIO,\
         mock.patch('containment.builder.config', new=config) as mconfig:
        # The following line causes the code to enter pave_project.
        CLIO().ensure_config()
    
