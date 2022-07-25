import io
from typing import Iterable, TextIO, Tuple, Type

from asort import api

__all__ = ["Tuple", "Type", "TextIO", "Iterable"]


def test_cli_output(files, snapshot):
    """
    multi
    line
    string
    """
    # GIVEN
    for filepath in files:
        output_stream = io.StringIO()

        # WHEN
        changed = api.sort_file(filepath, output_stream=output_stream)

        # THEN
        assert output_stream.getvalue() == snapshot
        assert changed == snapshot
