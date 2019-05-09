from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app=app)


class TextString(db.Model):

    text_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)


@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            return "内容不可为空"
        textString = TextString(content=text)
        db.session.add(textString)
        db.session.commit()
        return "上传成功，序号：%s" % textString.text_id
    return render_template("index.html")


@app.route("/getText/<int:text_id>")
def getText(text_id):
    textString = TextString.query.get(text_id)
    if not textString:
        return ""
    return textString.content


if __name__ == '__main__':
    app.run()
