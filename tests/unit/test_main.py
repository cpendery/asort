from unittest import mock

from asort import main


@mock.patch("asort.main.argparse")
def test_cli(mock_argparse, snapshot):
    # GIVEN + WHEN
    main.cli()

    # THEN
    assert (
        mock_argparse.ArgumentParser.return_value.add_argument.call_args_list
        == snapshot
    )


@mock.patch("asort.main.api")
@mock.patch("asort.main.cli")
def test_main(mock_cli, mock_asort):
    # GIVEN
    paths = ["path1", "path2"]
    mock_cli.return_value.paths = paths

    # WHEN
    main.main()

    # THEN
    call_lists = mock_asort.ASort.return_value.process_path.call_args_list
    call_paths = [call_arg[0][0] for call_arg in call_lists]
    assert paths == call_paths
