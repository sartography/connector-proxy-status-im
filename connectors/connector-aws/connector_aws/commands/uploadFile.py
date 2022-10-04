import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from connector_aws.auths.simpleAuth import SimpleAuth


class UploadFile:
    """ AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY need to be set in the environment for
    BOTO3 to make the correct call. """

    def __init__(self, access_key: str, secret_key: str,
                 file_name: str, file_data:bytes, bucket: str, object_name: str):
        """
        :param access_key: AWS Access Key
        :param secret_key: AWS Secret Key
        :param file_name: File to upload
        :param file_data: Contents of file to be uploaded
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: Json Data structure containing a http status code (hopefully '200' for success..)
            and a response string.
        """
        self.client = SimpleAuth('kinesis', access_key, secret_key).get_resource()
        self.file_name = file_name
        self.file_data = file_data
        self.bucket = bucket
        self.object_name = object_name

    def execute(self):

        # If S3 object_name was not specified, use file_name
        if self.object_name is None:
            self.object_name = self.file_name

        # Upload the file
        try:
            response = self.client.upload_file(self.file_name, self.bucket, self.object_name)
        except ClientError as e:
            response = f'{ "error": "AWS Excetion {e}" }'
        return {
            'response': 'success',
            'status': response.status_code,
            'mimetype': 'application/json'
        }
