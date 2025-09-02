import polars as pl
import great_expectations as ge
import pytest
from pytest_html import extras 
import logging
import os

def test_csv_with_polars(data_path):
    # Load CSV
    csv_file = os.path.join(data_path, "sample_data.csv")
    df = pl.read_csv(csv_file)

    # 1. Column existence
    for col in ["id", "name", "age", "score", "email"]:
        assert col in df.columns, f"Column {col} is missing"

    # 2. Column uniqueness
    assert df["id"].n_unique() == df.height, "Column 'id' has duplicate values"

    # 3. No nulls
    for col in ["id", "name", "age", "score", "email"]:
        assert df[col].null_count() == 0, f"Column {col} has null values"

    # 4. Column value ranges
    assert df["age"].min() >= 0 and df["age"].max() <= 120, "Age column out of bounds"
    assert df["score"].min() >= 0 and df["score"].max() <= 100, "Score column out of bounds"

    # 5. Regex validation for email
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    invalid_emails = df.filter(~df["email"].str.contains(email_regex, literal=False))
    assert invalid_emails.height == 0, f"Invalid emails found: {invalid_emails['email'].to_list()}"
    

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        extra = getattr(report, "extra", [])
        # collect properties attached in tests
        for name, value in getattr(item, "user_properties", []):
            extra.append(extras.text(str(value), name=name))
        report.extra = extra
        
@pytest.fixture
def unique_id_result(data_path):
    csv_file = os.path.join(data_path, "sample_data.csv")
    df = pl.read_csv(csv_file)
    if df["user_id"].is_unique:
        return "All user_id values are unique"
    else:
        return "Duplicates found in user_id column"
    
def test_pass_with_logs(request):
    # Some simulated work
    logs = []
    logging.info("Step 1: Connected to DB")
    logging.info("Step 2: Fetched 100 rows")
    logging.info("Step 3: Validation passed ✅")

    # Attach structured result
    request.node.user_properties.append(("Validation Result", {"rows": 100, "status": "ok"}))

    # Attach log even if test passes
    request.node.debug_log = "\n".join(logs)

    assert True  # test passes
    
import logging

def test_pass():
    logging.info("This is an INFO log inside a passing test")   
    assert 1 == 1

def test_fail():
    logging.info("This is an INFO log inside a failing test")    
    assert 1 == 2
