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
    mock_proj_root = os.path.join(tmpdir, "test_project_root")
    mock_home = os.path.join(tmpdir, "test_user_home")
    mock_shell = "/bin/bash"
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=ensureconfig_mockcli) as CLIO,\
         mock.patch('containment.config._PROJECT_ROOT',
                    new=mock_proj_root) as mprojroot,\
         mock.patch('containment.config._HOME',
                    new=mock_home) as mhome,\
         mock.patch('containment.config._SHELL',
                    new=mock_shell) as mshell:
        # The following line causes the code to enter pave_project.
        #CLIO().ensure_config()
        print("pass")
    
