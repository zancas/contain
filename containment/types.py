# -*- coding: utf-8 -*-
"""Contains types used by the containment application.

Types:
    ProjectId: A validation type for project identifiers.
"""

from typingplus.types import Length


ProjectId = Length[str, 1:]
