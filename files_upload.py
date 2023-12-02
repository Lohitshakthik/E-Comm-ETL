import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

#aws_access_key = 'XXXX'
#aws_secret_key = 'XXXXXX'

bucket_names = ['0rders01', 'returns02']


def create_s3_bucket(bucket_name):
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except PartialCredentialsError:
        print("Credentials not properly configured.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"Access Denied: Check IAM user permissions for bucket '{bucket_name}'.")
        elif e.response['Error']['Code'] == 'IllegalLocationConstraintException':
            print(f"Error creating bucket '{bucket_name}': {str(e)}\nTry specifying a valid region.")
        else:
            print(f"Error creating bucket '{bucket_name}': {str(e)}")


create_s3_bucket(bucket_names[0])

create_s3_bucket(bucket_names[1])
