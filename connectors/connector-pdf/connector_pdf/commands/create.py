"""Create."""
from io import BytesIO

from connector_aws.commands.uploadFile import UploadFileData
from xhtml2pdf import pisa  # type: ignore


class CreatePDF:
    """CreatePDF."""

    def __init__(self, template: str):
        """__init__."""
        self.template = template

    def execute(self, config):
        """Execute."""
        buf = BytesIO()

        pisa_status = pisa.CreatePDF(self.template, dest=buf)

        if pisa_status.err:
            return {
                "response": "ERR",
                "status": "500",
                "mimetype": "text",
            }

        return {
            "response": buf.getvalue(),
            "status": "200",
            "mimetype": "application/pdf",
        }


class CreatePDFAndUploadToS3:
    """CreatePDFAndUploadToS3."""

    def __init__(self, template: str, aws_object_name: str):
        """__init__."""
        self.template = template
        self.aws_object_name = aws_object_name

    def execute(self, config):
        """Execute."""
        aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
        aws_bucket = config["AWS_INVOICE_S3_BUCKET"]

        pdf_result = CreatePDF(self.template).execute(config)

        if pdf_result["status"] != "200":
            return {
                "response": '{ "error": "failed to create pdf" }',
                "status": "500",
                "mimetype": "application/json",
            }

        aws_result = UploadFileData(
            aws_access_key_id,
            aws_secret_access_key,
            pdf_result["response"],
            aws_bucket,
            self.aws_object_name,
        ).execute(config)

        if aws_result["status"] != "200":
            return aws_result

        return {
            "response": '{ "created": "' + self.aws_object_name + '"}',
            "status": "200",
            "mimetype": "application/json",
        }
