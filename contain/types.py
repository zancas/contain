# -*- coding: utf-8 -*-
"""Contains types used by the contain application.

Types:
    ProjectId: A validation type for project identifiers.
"""

from typingplus.types import Length


Project = Length[str, 1:]
