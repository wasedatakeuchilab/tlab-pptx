import os
import pathlib
import typing as t
from collections import abc

import pytest

from tests import FixtureRequest
from tlab_pptx import typing


@pytest.fixture(params=["str", "Path"])
def filepath(
    request: FixtureRequest[str], filename: str, tmpdir: str
) -> typing.FilePath:
    match request.param:
        case "str":
            return os.path.join(tmpdir, str(filename))
        case "Path":
            return pathlib.Path(tmpdir) / filename
        case _:
            raise NotImplementedError


@pytest.fixture(params=["buffer", "filepath"])
def file(
    request: FixtureRequest[str],
    filepath: str,
    open_mode: t.Literal["rb", "wb"],
) -> abc.Generator[str | t.IO[bytes], None, None]:
    match request.param:
        case "buffer":
            if "r" in open_mode:
                with open(filepath, "rb") as f:
                    yield f
            elif "w" in open_mode:
                with open(filepath, "wb") as f:
                    yield f
            else:
                raise ValueError(f"Invalid open_mode {open_mode}.")
        case "filepath":
            yield filepath
