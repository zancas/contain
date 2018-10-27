# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import pytest
from unittest import mock

from ..builder import CommandLineInterface
from ..cli.activate import activate as actfun
from ..cli import activate

mockattributes = ("ensure_config", "write_dockerfile", "build", "run")


def set_of_cli_operations(mockattributes):
    print("The number of steps is: ", steps)
    def actual_decorator(cli_cls):
        print("Did this get evaluated?")
        return cli_cls

    return actual_decorator

@set_number_of_cli_operations(15)
class CommandLineInterfaceWrapper:
    pass


def test_unitest_patch():
    
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    auto_spec=True) as CLIO:   
        c = CLIO()
        print(c)
        print(c.ensure_config())

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
