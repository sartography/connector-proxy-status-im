"""UploadFile."""
from botocore.exceptions import ClientError  # type: ignore
from connector_aws.auths.simpleAuth import SimpleAuth  # type: ignore


class UploadFileData:
    """UploadFileData."""

    def __init__(
        self,
        file_data: bytes,
        bucket: str,
        object_name: str,
    ):
        """
        :param file_data: Contents of file to be uploaded
        :param bucket: Bucket to upload to
        :param object_name: S3 object name.
        :return: Json Data structure containing a http status code (hopefully '200' for success..)
            and a response string.
        """
        self.file_data = file_data
        self.bucket = bucket
        self.object_name = object_name

    def execute(self, config, task_data):
        """Execute."""
        # Upload the file
        client = SimpleAuth("s3", config).get_resource()
        try:
            result = client.Object(self.bucket, self.object_name).put(
                Body=self.file_data
            )
            status = str(result["ResponseMetadata"]["HTTPStatusCode"])

            # TODO these can be improved
            if status == "200":
                response = '{ "result": "success" }'
            else:
                response = '{ "result": "error" }'
        except ClientError as e:
            response = f'{ "error": "AWS Excetion {e}" }'
            status = "500"

        return {"response": response, "status": status, "mimetype": "application/json"}
