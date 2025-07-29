CREATE OR REPLACE STORAGE INTEGRATION s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::764678967028:role/dummy-role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://cold-chain=monitoring/');

DESC INTEGRATION s3_int;

ALTER STORAGE INTEGRATION s3_int
SET STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::764678967028:role/SnowflakeS3Access';

DESC INTEGRATION s3_int;
ALTER STORAGE INTEGRATION s3_int
SET STORAGE_ALLOWED_LOCATIONS = ('s3://cold-chain-monitoring/');

DESC INTEGRATION s3_int;

CREATE OR REPLACE STAGE coldchain_stage
  STORAGE_INTEGRATION = s3_int
  URL = 's3://cold-chain-monitoring/';

LIST @coldchain_stage;

COPY INTO cold_chain_data
FROM @coldchain_stage/cold_chain_data.csv
FILE_FORMAT = (
  TYPE = 'CSV',
  FIELD_OPTIONALLY_ENCLOSED_BY = '"',
  SKIP_HEADER = 1
);
SELECT * FROM cold_chain_data LIMIT 10;

