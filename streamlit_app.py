import streamlit as st
import boto3
import botocore
import json
import io

session = boto3.Session(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_REGION"],
    )

sts_client = boto3.client('sts')

try:
    sts_client.get_caller_identity()
except botocore.exceptions.NoCredentialsError as e:
    st.error(e)

lambda_client = session.client('lambda')
s3_client = session.client('s3')

file_like_payload = io.StringIO()

# defaults for norris pta
embed_image_path = "norris_pta_000.png"
source_bucket = 'us-east-1-qr-codes'
object_key = 'norris-pta/norris_pta_001.png'

st.title('Norris Elementry PTA QR code generator')

response_body = {}

def get_save_qr_image(payload):
    response = lambda_client.invoke(
        FunctionName='npta_qr_gen',
        Payload=payload.read()
    )
    response_body = json.loads(json.loads(response['Payload'].read())['body'])

    s3_client.download_file(response_body['bucket'], response_body['key'], "qr-codes/" + response_body['file_name'])
    return "qr-codes/" + response_body['file_name']

with st.form("Enter Addresss"):
    address = st.text_input("Address here: ")
    payload = {'qr_code_text': address,'embed_image_path': embed_image_path,'source_bucket': source_bucket,'object_key': object_key}
    # Write the dictionary to the file-like object as JSON
    json.dump(payload, file_like_payload)

    # reset to beginning of file
    file_like_payload.seek(0)
    submit = st.form_submit_button('submit')

if submit:
    file_name = get_save_qr_image(file_like_payload)
    st.image(file_name)
    # save file locally
    with open(file_name, "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name=file_name,
            mime="image/png",
        )