import io

from asort import api


def test_cli_output(files, snapshot):
    # GIVEN
    for filepath in files:
        output_stream = io.StringIO()

        # WHEN
        changed = api.sort_file(filepath, output_stream=output_stream)

        # THEN
        assert output_stream.getvalue() == snapshot
        assert changed == snapshot
