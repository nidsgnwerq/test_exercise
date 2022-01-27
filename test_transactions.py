import pytest
import os

testdata = ["transactions", "transactions_1", "transactions_2", "transactions_3"]


@pytest.mark.parametrize("file_name", testdata)
def test_input_with_output(file_name):
    result_file_name = str(file_name + "_result.csv")
    expected_file_name = os.path.join("expected_outputs", str(file_name + "_expected.csv"))

    with open(result_file_name) as file:
        result_lines = file.readlines()

    with open(expected_file_name) as file:
        expected_lines = file.readlines()

    assert result_lines == expected_lines