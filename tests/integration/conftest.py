import os
from pathlib import Path

import pytest

CD = Path(__file__).parent.absolute()


@pytest.fixture
def files():
    fixtures_dir = CD.joinpath("fixtures")
    fixture_files: dict[str, Path] = {}
    for root, _, file_lst in os.walk(fixtures_dir):
        r = Path(root)
        for file in file_lst:
            if file.endswith((".py", ".pyi")):
                fixture_files[file] = r.joinpath(file)
    return sorted([path for _, path in fixture_files.items()])
