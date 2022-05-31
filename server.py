import datetime

from flask import Flask, send_file, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
from os import listdir
from os.path import isfile, isdir, join



app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisasecret"
app.config["UPLOADED_IMAGES_DEST"] = "/home/pi/projects/LocalFileSharing/Uploads/"


images = UploadSet("images", IMAGES)
configure_uploads(app, images)


class MyForm(FlaskForm):
    image = FileField("image")




@app.route("/", methods=["GET", "POST"])
def upload():
    form = MyForm()

    if form.validate_on_submit():
        print(form.image.data)
        filename = images.save(form.image.data)
        return redirect(url_for("files"))

    return render_template("upload.html", form=form)


@app.route("/files", methods=["GET", "POST"])
def files():
    all_files = []
    for child in listdir(app.config["UPLOADED_IMAGES_DEST"]):
        if isfile(join(app.config["UPLOADED_IMAGES_DEST"], child)):
            all_files.append(child)

    print("rendering files.html template")
    print(all_files)
    print(datetime.datetime.now().strftime("%I:%M:%S %p"))
    return render_template("files.html", all_files=all_files)


@app.route("/download")
def download():
    file = request.args["file"]
    return send_file(join(app.config["UPLOADED_IMAGES_DEST"], file), as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

