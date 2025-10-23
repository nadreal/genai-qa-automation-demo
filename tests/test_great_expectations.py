import pandas as pd
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

# def test_sample_data_with_expectations():
#     df = pd.read_csv("data/sample_data.csv")

#     context = gx.get_context(mode="fluent")  # returns EphemeralDataContext in Docker

#     # Create a pandas datasource using fluent API
#     from great_expectations.datasource.fluent import PandasDatasource

#     datasource = context.sources.add_pandas(name="my_pandas_datasource")
#     asset = datasource.add_dataframe_asset(name="my_asset")
    
#     batch_request = asset.build_batch_request(dataframe=df)
#     validator = context.get_validator(batch_request=batch_request)

#     result = validator.expect_column_values_to_not_be_null("id")
#     assert result.success

#     print("All expectations passed!")
