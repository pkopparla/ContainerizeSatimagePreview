from src.process import getpreview
import pytest


def test_filenotfound():
    "pass in some random directory where no valid files exist"
    with pytest.raises(FileNotFoundError):
        getpreview("tests")
