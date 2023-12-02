import streamlit as st
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from io import BytesIO

st.title("Welcome to ETL Page")

# AWS credentials
aws_access_key = 'XXXX'
aws_secret_key = 'XXXXXX'

# S3 bucket names
orders_bucket_name = '0rders01'
returns_bucket_name = 'returns02'

def upload_to_s3(file, bucket_name):
    print("AWS Access Key:", aws_access_key)
    print("AWS Secret Key:", aws_secret_key)
    print("Bucket Name:", bucket_name)

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    try:
        # Upload the file
        s3.upload_fileobj(file, bucket_name, file.name)
        st.success(f"{file.name} uploaded successfully to {bucket_name} bucket.")
    except NoCredentialsError:
        st.error("Credentials not available. Unable to upload to S3 bucket.")
    except Exception as e:
        st.error(f"Error uploading to S3: {str(e)}")

def main():
    with st.sidebar:
        option = st.selectbox(
            'Upload the Files',
            ('Orders', 'Returns'))
        st.write("This code will be printed to the sidebar.")

    if option == "Orders":
        st.write('You selected:', "Orders")
        file = st.file_uploader("Upload Orders file", type=["csv", "png", "jpg", "xlsx"])
        upload_button = st.button("Upload to AWS S3")

    if option == "Returns":
        st.write('You selected:', "Returns")
        file = st.file_uploader("Upload Returns file", type=["csv", "png", "jpg", "xlsx"])
        upload_button = st.button("Upload to AWS S3")

    if not file:
        st.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg", "xlsx"]))
        return

    if upload_button:
        upload_to_s3(file, orders_bucket_name if option == "Orders" else returns_bucket_name)

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

    # Create the first bucket
    create_s3_bucket(bucket_names[0])

    # Create the second bucket
    create_s3_bucket(bucket_names[1])


main()
