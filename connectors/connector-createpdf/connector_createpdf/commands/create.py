from io import BytesIO
from xhtml2pdf import pisa

class CreatePDF:
    def __init__(self, template: str):
        self.template = template

    def execute(self, config):
        buf = BytesIO()

        pisa_status = pisa.CreatePDF(self.template, dest=buf)

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
