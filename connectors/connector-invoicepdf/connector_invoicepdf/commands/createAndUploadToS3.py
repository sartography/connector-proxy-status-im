from connector_aws.commands.uploadFile import UploadFileData
from connector_createpdf.commands.create import CreatePDF

class CreateAndUploadToS3:
    def __init__(self, template: str, name: str, amount: str, 
            aws_bucket: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.template = template
        self.name = name
        self.amount = amount
        self.aws_bucket = aws_bucket
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def execute(self):
        pdf_result = CreatePDF(self.template).execute()

        if pdf_result['status'] != '200':
            return {
                'response': '{ "error": "failed to create pdf" }',
                'status': '500',
                'mimetype': 'application/json',
            }

        aws_result = UploadFileData(self.aws_access_key_id, 
            self.aws_secret_access_key, 
            pdf_result['response'],
            self.aws_bucket,
            'invoice.pdf').execute()

        return aws_result
