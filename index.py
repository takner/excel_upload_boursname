from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import jdatetime
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # First grab the file
        filename = secure_filename(file.filename)
        date_str = jdatetime.date.today().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H-%M-%S")
        new_filename = f"{date_str}_{time_str}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
        return "File " f"{new_filename}" " has been uploaded"
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
