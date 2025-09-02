import pytest
from pytest_html import extras
import os


@pytest.fixture(scope="session")
def data_path():
    root_dir = os.path.dirname(os.path.abspath(__file__))  # if conftest is in tests/
    root_dir = os.path.dirname(root_dir)  # go up to project root
    return os.path.join(root_dir, "data")

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call":
#         extra = getattr(report, "extra", [])
#         # Always add log, even if test PASSED
#         extra.append(extras.text(f"Finished {item.name} with outcome: {report.outcome}"))
#         # extra.append(extras.text(f"[{report.outcome.upper()}] Test {item.name} completed"))
#         report.extra = extra

