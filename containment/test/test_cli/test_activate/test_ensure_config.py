# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import pytest
from unittest import mock

from ....builder import CommandLineInterface
from ....cli.activate import activate as actfun
from ....cli import activate


def test_fixturization(ensureconfig_mockcli):
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=ensureconfig_mockcli) as CLIO,\
         mock.patch('containment.builder.context') as mcontext,\
         mock.patch('containment.builder.config') as mconfig:
        print(CLIO.ensure_config)
        print(CLIO.write_dockerfile)
        mconfig.project_config.path.is_dir.return_value = \
            False
        c = CLIO()
        #print(dir(c))
        c.ensure_config()
        print((mcontext.method_calls))
        print((mconfig.method_calls))
        #print(dir(mcontext))
