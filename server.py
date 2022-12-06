# from flask import Flask

# app = Flask(__name__)


import json
import os
from detect_ocr import detect_ocr_image
from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload_file/'
DETECTED_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECTED_FOLDER'] = DETECTED_FOLDER
# @app.route('/')
# def hello_world():
#     html = "<button > Welcome </button> <h1 > The webapp is ready < /h1 >"
#     return html


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    print(request.method)
    if request.method == 'GET':
        html = f'''
        <!doctype html>
        <h1>Welcome to license detection page</h1>
        <h1> Please submit an image</h1>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        <a href="/detection">View all detected images</a>
        '''
        return html
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        form = request.form
        print(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            detect_ocr_image(app.config['UPLOAD_FOLDER'] +
                             filename, 'small', os.path.join(
                                 app.config['DETECTED_FOLDER'], 'small')+'/')
            detect_ocr_image(app.config['UPLOAD_FOLDER'] +
                             filename, 'medium', os.path.join(app.config['DETECTED_FOLDER'], 'medium')+'/')
            detect_ocr_image(app.config['UPLOAD_FOLDER'] +
                             filename, 'large', os.path.join(app.config['DETECTED_FOLDER'], 'large') + '/')
            return redirect("/small")


@ app.route('/small')
def detectionSmall():
    images = []
    for file in os.listdir(app.config['DETECTED_FOLDER'] + '/small/'):
        print(file)
        images.append('small/' + file)
        filename = app.config['DETECTED_FOLDER'] + '/small/' + file
        print(filename)
        # html += f'<img src="${filename}" alt="image" height="300px" width="500px">'
    return render_template('small.html', imagelist=images)


@ app.route('/medium')
def detectionMedium():
    images = []
    for file in os.listdir(app.config['DETECTED_FOLDER'] + '/medium/'):
        print(file)
        images.append('medium/' + file)
        filename = app.config['DETECTED_FOLDER'] + file
        print(filename)
        # html += f'<img src="${filename}" alt="image" height="300px" width="500px">'
    return render_template('medium.html', imagelist=images)


@ app.route('/large')
def detectionLarge():
    images = []
    for file in os.listdir(app.config['DETECTED_FOLDER'] + '/large'):
        print(file)
        images.append('large/' + file)
        filename = app.config['DETECTED_FOLDER'] + file
        print(filename)
        # html += f'<img src="${filename}" alt="image" height="300px" width="500px">'
    return render_template('large.html', imagelist=images)


app.run(host="0.0.0.0")
