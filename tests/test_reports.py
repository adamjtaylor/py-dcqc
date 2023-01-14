import pytest

from dcqc.reports import JsonReport


def test_for_error_when_creating_report_if_file_already_exists(get_data):
    existing_url = get_data("test.txt").as_posix()
    with pytest.raises(FileExistsError):
        JsonReport(existing_url)


def test_that_a_single_object_can_be_reported_on(test_files):
    test_file = test_files["good"]
    report_url = "mem://report.json"
    report = JsonReport(report_url)
    report.save(test_file)