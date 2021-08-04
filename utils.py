from uuid import uuid4
from docx2pdf import convert
from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
import re
import os


ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convert_doc_to_pdf(file_path,file_name):
    print('FILE PATH IS',file_path)
    try:
        convert(file_path,'static/converted_files/'+file_name+'.pdf')
    except Exception as e:
        print("Exception Occurred", e)
        return False
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except IOError:
        print('Error deleting file')
    return True



def find_the_email(pdf_path):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(pdf_path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = match.group(0)
    return email