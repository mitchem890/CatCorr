import pytest
import CatCorrFunc


@pytest.mark.parametrize("stringList",[(["MyFile.txt", "MyFile.exe"])])
def test_longest_substring_finder(stringList):
    assert CatCorrFunc.longest_substring_finder(stringList) == "MyFile."


@pytest.mark.parametrize("string",[("sub-150423_ses-baseline_parcellation-")])
def test_remove_empty_prefix(string):
    assert CatCorrFunc.remove_empty_prefix(string) == "sub-150423_ses-baseline"


@pytest.mark.parametrize("string",[("sub-150423_ses-baseline_parcellation-MyParcellation_output.txt")])
def test_get_parcellation(string):
    assert CatCorrFunc.get_parcellation(string) == "parcellation-MyParcellation"
    return


def test_append(filelist, outfile):

    return


def test_transpose(filename):

    return


def test_correlate(filename, outfile):

    return


def test_add_net_header(filename, num_of_parcels):

    return
