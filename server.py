from flask import Flask, send_file, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet


app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisasecret"
app.config["UPLOADED_IMAGES_DEST"] = "/home/pi/projects/LocalFileSharing/Uploads"


images = UploadSet("images", IMAGES)
configure_uploads(app, images)


class MyForm(FlaskForm):
    image = FileField("image")


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()

    if form.validate_on_submit():
        print(form.image.data)
        filename = images.save(form.image.data)
        return "Filename: " + filename

    return render_template("index.html", form=form)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

