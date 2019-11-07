from flask import Flask, Response, render_template, request, url_for
import json
from wtforms import StringField, Form
import mysql.connector as mariadb

app = Flask(__name__)

mariadb_connection = mariadb.connect(host="10.2.0.181", user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()

query = "SELECT productnaam FROM coop"
cursor.execute(query)
result = cursor.fetchall()
final_result = []
for i in result:
    final_result.append(str(i))


class SearchForm(Form):
    autocomp = StringField('Insert City', id='city_autocomplete')

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(final_result), mimetype='application/json')

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm(request.form)
    if request.form:
        post_data = request.form['boodschappenlijst']
        boodschappen_lijst = []
        for element in post_data.split("\n"):
            element.replace(" ", "")
            element = element.rstrip()
            boodschappen_lijst.append(element)
        print(boodschappen_lijst)
    return render_template("index.html", form=form)

@app.route("/minor")
def minor():
    return render_template("minor.html")

@app.route("/poster")
def poster():
    return render_template("poster.html")

if __name__ == "__main__":
    app.run()