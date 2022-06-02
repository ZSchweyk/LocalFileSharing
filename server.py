from flask import Flask, flash, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from os import listdir
import os
from os.path import isfile, isdir, join
import os.path


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "/home/pi/FileUploads/"
app.config['UPLOAD_EXTENSIONS'] = (".jpg", ".txt", ".png", ".pdf", ".docx", ".jpeg", ".mscz", ".xlsx", ".qdf")
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def has_valid_extension(filename):
    file_ext = os.path.splitext(filename)[1]
    if file_ext.lower() in app.config['UPLOAD_EXTENSIONS']:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)
        if has_valid_extension(filename):
            f.save(app.config['UPLOAD_FOLDER'] + filename)
        else:
            flash("File extension \"" + os.path.splitext(filename)[1] + "\" not allowed")

    all_files = []
    for child in listdir(app.config["UPLOAD_FOLDER"]):
        filename = join(app.config["UPLOAD_FOLDER"], child)
        if isfile(filename):
            if has_valid_extension(filename):
                all_files.append(File(child, round(os.path.getsize(filename) / 1000, 1)))

    return render_template('index.html', all_files=all_files)



@app.route("/download")
def download():
    file = request.args["file"]
    return send_file(join(app.config["UPLOAD_FOLDER"], file), as_attachment=True)


@app.route("/delete")
def delete():
    filename = secure_filename(request.args["filename"])
    filename = join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filename):
        os.remove(filename)

    return redirect(url_for("upload_file"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)



