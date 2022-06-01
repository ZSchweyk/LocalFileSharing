from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, isdir, join
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "/home/pi/FileUploads/"
app.config['UPLOAD_EXTENSIONS'] = (".jpg", ".txt", ".png")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

    all_files = []
    for child in listdir(app.config["UPLOAD_FOLDER"]):
        filename = join(app.config["UPLOAD_FOLDER"], child)
        if isfile(filename):
            file_ext = os.path.splitext(filename)[1]
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                all_files.append(child)

    return render_template('index.html', all_files=all_files)



@app.route("/download")
def download():
    file = request.args["file"]
    return send_file(join(app.config["UPLOAD_FOLDER"], file), as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)



