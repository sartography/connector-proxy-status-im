from connector_aws.commands.uploadFile import UploadFileData
from connector_createpdf.commands.create import CreatePDF

class CreateAndUploadToS3:
    def __init__(self, template: str, name: str, amount: str, 
        aws_bucket: str, aws_object_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        
        self.template = template
        self.name = name
        self.amount = amount
        self.aws_bucket = aws_bucket
        self.aws_object_name = aws_object_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def execute(self):
        pdf_data = self.template.format(name=self.name, amount=self.amount)
        pdf_result = CreatePDF(pdf_data).execute()

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
            self.aws_object_name).execute()

        if aws_result['status'] != '200':
            return aws_result

        return {
            'response': '{ "created": "' + self.aws_object_name + '"}',
            'status': '200',
            'mimetype': 'application/json',
        }
