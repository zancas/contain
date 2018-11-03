# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import pytest
from unittest import mock

from ....builder import CommandLineInterface
from ....cli.activate import activate as actfun
from ....cli import activate

mockattributes = ("ensure_config", "write_dockerfile", "build", "run")


def apply_operations(stop_index):
    def actual_decorator(cli_cls):
        raw_klass = cli_cls.__bases__[0]
        print(id(raw_klass))
        for stub in mockattributes[stop_index:]:
            setattr(raw_klass, stub, mock.MagicMock(name=stub))
        return raw_klass

    return actual_decorator

@apply_operations(1)
class EnsureConfigOnly(CommandLineInterface): pass

def test_ensure_config(tmpdir):
    print(tmpdir)
    print(EnsureConfigOnly)
    
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=EnsureConfigOnly) as CLIO:
        with mock.patch('containment.builder.context') as mcon:
            print(EnsureConfigOnly)
            c = CLIO()
            print(dir(c))
