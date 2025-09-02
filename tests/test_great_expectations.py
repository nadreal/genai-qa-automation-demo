# tests/test_great_expectations.py
import great_expectations as ge
import pandas as pd

def test_sample_data_with_expectations():
    # Load dataset
    df = pd.read_csv("data/sample_data.csv")
    gdf = ge.from_pandas(df)

    # Expectations
    gdf.expect_column_to_exist("id")
    gdf.expect_column_to_exist("score")
    gdf.expect_column_values_to_not_be_null("id")
    gdf.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")

    # Run validations
    results = gdf.validate()
    assert results.success, results
