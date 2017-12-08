containment
===========

|PyPI| |Python Versions| |Build Status| |Coverage Status| |Code Quality|

*Automate the creation and management of development containers.*

``containment`` makes it easy to create and share reusable container images
that provide a consistent and transparent development environment.

``containment`` was inspired by Python's virtualenv_ package. Like
``virtualenv``, ``containment`` separates project dependencies from packages
installed on the development machine but additionally separates your project's
operating system dependencies to guarantee that all developers are using a
consistent set of dependencies.

Unlike with traditional container-based approaches, ``containment`` creates an
additional layer to make the use of the development container more seamless.
``containment`` tries to be as invisible to the user as possible, by using the
same shell, development tools, and configuration already defined by the user.


Installation
------------

Currently, the easiest method is to install it using pip:

.. code-block:: bash

    $ pip3 install containment


In the future, there will be operating system packages to simplify the
installation of ``containment``.


Basic Usage
-----------

.. code-block:: bash

    $ cd path/to/project
    $ containment


.. _virtualenv: https://github.com/pypa/virtualenv


.. |Build Status| image:: https://travis-ci.org/contains-io/contain.svg?branch=development
   :target: https://travis-ci.org/contains-io/contain
.. |Coverage Status| image:: https://coveralls.io/repos/github/contains-io/contain/badge.svg?branch=development
   :target: https://coveralls.io/github/contains-io/contain?branch=development
.. |PyPI| image:: https://img.shields.io/pypi/v/contain.svg
   :target: https://pypi.python.org/pypi/contain/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/contain.svg
   :target: https://pypi.python.org/pypi/contain/
.. |Code Quality| image:: https://api.codacy.com/project/badge/Grade/f6306cdc0276428fbbbed44386aeb1b6
   :target: https://www.codacy.com/app/contains-io/contain?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=contains-io/contain&amp;utm_campaign=Badge_Grade
