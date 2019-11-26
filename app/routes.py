from app import app, session
import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory, Response
from werkzeug.utils import secure_filename
from tf_idf.NLP_helpers import word_frequencies, idf, tf_idf
from tf_idf.read_xlf import get_words
from tf_idf.exporting_funcs import export_CSV, export_TBX, export_MultiTerm

ALLOWED_EXTENSIONS = set(['xliff', 'xlf', 'xlz', 'sdlxliff', 'xml'])


@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    # return render_template('base.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])
    return render_template('base.html')


@app.route('/get_glossary')
def get_glossary():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    words = get_words(files)
    tfs = word_frequencies(words)
    idfs = idf(tfs.keys())
    tf_idf_gen = tf_idf(tfs, idfs)
    session.clean_session()
    session.init_gen(tf_idf_gen)
    terms = session.get_top_n(10)

    return render_template('glossary.html', terms=terms)


@app.route('/export', methods=['POST'])
def export():

    if request.method == 'POST':

        PATH = app.config['DOWNLOAD_FOLDER']
        terms = session.get_top()

        if request.form['filetype'] == 'CSV':
            export_CSV(PATH, terms)
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'export.csv', as_attachment=True,
                                       mimetype="text/csv", attachment_filename=('export.csv'))
        elif request.form['filetype'] == 'TBX':
            export_TBX(PATH, terms)
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'TBX_export.xml', as_attachment=True,
                                       mimetype="text/xml", attachment_filename=('TBX_export.xml'))
        elif request.form['filetype'] == 'MultiTerm':
            export_MultiTerm(PATH, terms)
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'MultiTerm_export.xml', as_attachment=True,
                                       mimetype="text/xml", attachment_filename=('MultiTerm_export.xml'))

    # return render_template('export.html')


# @app.route('/download')
# def download():
#     return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'export.csv', as_attachment=True, mimetype="text/csv", attachment_filename=('export.csv'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('upload.html')
