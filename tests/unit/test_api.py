import io
from unittest import mock

import pytest

from asort import api
from asort.api import ASort, process_dund_tokens


@mock.patch("asort.api.process_path")
def test_asort_process_path(mock_process_path):
    # GIVEN
    asort = ASort
    path = "path"

    # WHEN
    asort.process_path(path)

    # THEN
    mock_process_path.assert_called_with(path)


@mock.patch("asort.api.sort_file")
@mock.patch("asort.api.os")
@mock.patch("asort.api.Path")
@pytest.mark.parametrize(
    ["is_file", "file_changed"],
    [
        (True, True),
        (True, False),
        (False, False),
    ],
    ids=[
        "is file and file changed",
        "is file and file hasn't changed",
        "not a file and file hasn't changed",
    ],
)
def test_process_path(
    mock_path, mock_os, mock_sort_file, is_file, file_changed, capsys, snapshot
):
    # GIVEN
    mock_return = mock.MagicMock()
    mock_return.is_file.return_value = is_file
    mock_return.__str__ = lambda _: "file1.py"  # type: ignore
    mock_return.joinpath = lambda x: x
    mock_path.return_value = mock_return
    mock_sort_file.return_value = file_changed
    mock_os.walk.return_value = [("root", None, ["file2.py", "file3.pyi", "file4.txt"])]
    path = "path"

    # WHEN
    api.process_path(path)

    # THEN
    out, _ = capsys.readouterr()
    assert out == snapshot


@mock.patch("asort.api.open", mock.mock_open(read_data="foo\nbar\nbaz\n"))
@mock.patch("asort.api.write_stream")
@mock.patch("asort.api.Tokenizer")
def test_sort_file_no_output_stream(mock_tokenizer, mock_write_stream):
    # GIVEN
    mock_path = mock.MagicMock()
    mock_tokenizer.return_value.change_occured = True

    # WHEN
    change = api.sort_file(mock_path)

    # THEN
    mock_write_stream.assert_called_once()
    assert change == True


def test_process_dund_tokens_no_tokens():
    # WHEN + THEN
    assert [] == process_dund_tokens([])
