import pandas as pd
import great_expectations as gx

def test_sample_data_with_expectations():
    # 1️⃣ Load CSV data
    df = pd.read_csv("data/sample_data.csv")

    # 2️⃣ Initialize in-memory GE context
    context = gx.get_context()

    # 3️⃣ Create a Pandas datasource + asset
    datasource = context.sources.add_pandas("my_pandas_datasource")
    asset = datasource.add_dataframe_asset(name="my_asset")

    # 4️⃣ Build a batch and get a validator
    batch_request = asset.build_batch_request(dataframe=df)
    validator = context.get_validator(batch_request=batch_request)

    # 5️⃣ Expectations (Fluent API version)
    validator.expect_table_row_count_to_be_between(min_value=1)  # replaces "greater_than"
    validator.expect_column_values_to_not_be_null("id")
    validator.expect_column_values_to_be_between("age", min_value=20, max_value=50)
    validator.expect_column_values_to_be_between("score", min_value=0, max_value=100)
    validator.expect_column_values_to_match_regex("email", r".+@.+\..+")

    # 6️⃣ Run validation
    results = validator.validate()
    assert results.success, results

    print("All expectations passed!")

