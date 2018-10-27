# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import pytest
from unittest import mock

from ..builder import CommandLineInterface
from ..cli.activate import activate as actfun
from ..cli import activate

mockattributes = ("ensure_config", "write_dockerfile", "build", "run")


def apply_operations(stop_index):
    def actual_decorator(cli_cls):
        raw_klass = cli_cls.__bases__[0]
        print("stop_index is: ", stop_index)
        for stub in mockattributes[stop_index:]:
            print(stub)
            setattr(raw_klass, stub, mock.MagicMock(name=stub))
        print(type(raw_klass.run))
        print(type(raw_klass.ensure_config))
        print()
        return cli_cls

    return actual_decorator

@apply_operations(1)
class EnsureConfigOnly(CommandLineInterface): pass

@apply_operations(2)
class FirstTwo(CommandLineInterface): pass

@apply_operations(3)
class FirstThree(CommandLineInterface): pass

def test_unitest_patch():
    
    print(EnsureConfigOnly)
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=EnsureConfigOnly) as CLIO:   
        print(EnsureConfigOnly)
        c = CLIO()
        print(c)
        print(c.ensure_config)
        print(c.write_dockerfile)
        print(c.build)
        print(c.run)

@pytest.fixture
def initialoperations():
    def takesteps(number_steps):
        """"""
        newcli = CommandLineInterface()
        for ordered_op in operations[number_steps:]:
            print(ordered_op)
            newcli.__setattr__(ordered_op, mock.sentinel) 
        #print(dir(newcli))
        print(type(newcli.run))
        print(type(newcli.build))
        return newcli

    return takesteps


def test_construction(initialoperations, monkeypatch):
    """Test activation under ideal conditions."""
    with monkeypatch.context() as c:
        monkeypatch.setattr("..builder.CommandLineInterface",
                            initialoperations(3))
        actfun()


def test_ensure_config(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.write_dockerfile = lambda: print("write_dockerfile")
        newcli.build = lambda: print("build")
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_write_dockerfile(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.build = lambda: print("build")
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_build(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_run(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()
