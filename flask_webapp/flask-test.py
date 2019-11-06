from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.form:
        post_data = request.form['boodschappenlijst']
        boodschappen_lijst = []
        for element in post_data.split("\n"):
            element.replace(" ", "")
            element = element.rstrip()
            boodschappen_lijst.append(element)
        print(boodschappen_lijst)
    return render_template("index.html")

@app.route("/minor")
def minor():
    return render_template("minor.html")

@app.route("/poster")
def poster():
    return render_template("poster.html")

if __name__ == "__main__":
    app.run()