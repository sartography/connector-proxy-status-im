from io import BytesIO
from jinja2 import BaseLoader, Environment
from markdown2 import markdown
from xhtml2pdf import pisa

from connector_aws.commands.uploadFile import UploadFileData

class CreatePDF:
    def __init__(self, template: str):
        self.template = template

    def execute(self, config, task_data):
        buf = BytesIO()

        html_string = markdown(self.template)
        html_template = Environment(loader=BaseLoader).from_string(html_string)
        html_content = html_template.render(**task_data)

        pisa_status = pisa.CreatePDF(html_content, dest=buf)

        if pisa_status.err:
            return {
                'response': 'ERR',
                'status': '500',
                'mimetype': 'text',
            }
        
        return {
            'response': buf.getvalue(),
            'status': '200',
            'mimetype': 'application/pdf',
        }


class CreatePDFAndUploadToS3:
    def __init__(self, template: str, aws_object_name: str):
        
        self.template = template
        self.aws_object_name = aws_object_name

    def execute(self, config, task_data):
        aws_access_key_id = config['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY']
        aws_bucket = config['AWS_INVOICE_S3_BUCKET']

        pdf_result = CreatePDF(self.template).execute(config, task_data)

        if pdf_result['status'] != '200':
            return {
                'response': '{ "error": "failed to create pdf" }',
                'status': '500',
                'mimetype': 'application/json',
            }

        aws_result = UploadFileData(aws_access_key_id, 
            aws_secret_access_key, 
            pdf_result['response'],
            aws_bucket,
            self.aws_object_name).execute(config)

        if aws_result['status'] != '200':
            return aws_result

        return {
            'response': '{ "created": "' + self.aws_object_name + '"}',
            'status': '200',
            'mimetype': 'application/json',
        }

