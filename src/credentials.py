import json
import base64
import boto3
import botocore.exceptions


def get_sumo_auth():
    secret_name = "sumologic_api"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            format_secret = json.loads(secret)
            sumo_id = format_secret['id']
            sumo_token = format_secret['token']
            decoded_secret = sumo_id + ':' + sumo_token
            encoded_bytes = base64.b64encode(decoded_secret.encode("utf-8"))
            encoded_secret = str(encoded_bytes, "utf-8")
            return encoded_secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret
    except botocore.exceptions.ClientError as e:
        raise e
