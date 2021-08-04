import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request
from utils import allowed_file, convert_doc_to_pdf,find_the_email
import glob

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    """ Renders Index.html """
    try:
        return render_template('index.html')
    except Exception as e:
        print("Exception Occurred", e)
        return jsonify({"status": "failed", "message": "Something Went Wrong !!"})


@app.route('/uploads', methods=['POST'])
def file_converter():
    """
    Function Processing Steps:
    Step-1 : Check uploaded file extension ,if accepted format process further
    Step-2 : Save the files into uploads folder
    Step-3 : Convert the html,doc and docx files into pdf file and stores into converted_files folder
    Note :  If file is already in pdf format than file will directly save in converted_files
            folder without other action.
    """
    if request.method == "POST":
        try:
            files = request.files.getlist('file')
            print("files", files)
            if len(files) > 0:
                for data in files:
                    if allowed_file(data.filename):
                        filename = secure_filename(data.filename)
                        extension = filename.split('.')
                        file_path = os.path.join('static/uploads', filename)
                        if extension[-1] == 'pdf':
                            pdf_file_path = os.path.join('static/converted_files', filename)
                            data.save(pdf_file_path)
                        else:
                            data.save(file_path)
                        if extension[-1] == "docx" or extension[-1] == "doc":
                            if convert_doc_to_pdf(file_path,data.filename):
                                print("File Converted to PDF Successfully !!")
                            else:
                                raise Exception('Something Went Wrong with file convert !')
                        return jsonify({"status": "success", "message": "File Uploaded Successfully !!"})
                    else:
                        return jsonify({"status": "failed", "message": "Format Not Allowed !!"})
            else:
                return jsonify({"status": "failed"})
        except Exception as e:
            print("Exception Occurred", e)
            return jsonify({"status": "exception", "message": "Something Went Wrong post!!"})
    else:
        return jsonify({"status": "failed", "message": "Method Not Allowed !"})




@app.route('/result', methods=['GET'])
def result():
    """ Renders Something """
    try:
        file_path = os.path.join('static/converted_files')
        AllFiles = glob.glob(file_path+"/*.pdf")
        l = []
        for OneFile in AllFiles:
            print(OneFile)
            l.append(find_the_email(OneFile))
        return jsonify(l)        
    except Exception as e:
        print("Exception Occurred", e)
        return jsonify({"status": "failed", "message": "Something Went Wrong !!"})


@app.route('/remove', methods=['GET'])
def remove():
    for f in os.listdir('static/converted_files'):
        try:
            os.remove(os.path.join('static/converted_files', f))
        except:
            return jsonify({"status": "failed", "message": "something Went wrong"})
    return jsonify({"status": "success", "message": "All Files Removed Successfully !"})














# run the project
if __name__ == '__main__':
    app.run(port=9000,debug=True)