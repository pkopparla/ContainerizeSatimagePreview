from src.process import getpreview
import warnings
import boto3
import subprocess
import pytest


def test_gdal_exists():
    """test if gdal cli is installed"""
    response_code = subprocess.call("gdalinfo --version", shell=True)
    assert response_code == 0


def test_awscreds_exist():
    """check if AWS creds exist, give warning if they don't"""
    if boto3.session.Session().get_credentials() is None:
        warnings.warn(
            "AWS credentials not found, code can only run locally", UserWarning
        )
    else:
        assert True


@pytest.mark.parametrize(
    "test_input",
    [
        # case where input is only 2 strings
        ["test1", "test2"],
        # case where input is not list but string
        ["randomstring"],
    ],
)
def test_improper_bandcount(test_input):
    """pass in incorrect number of band files"""
    with pytest.raises(ValueError):
        getpreview(test_input)  # should be list of exactly 3 strings


def test_download_failed():
    """pass in non-existent remote files to check error handling"""
    with pytest.raises(FileNotFoundError):
        getpreview(["a", "b", "c"])  # gdal_translate should fail to write to local file
