from flask import Flask, Response, render_template, request, url_for, jsonify
import mysql.connector as mariadb

app = Flask(__name__)

mariadb_connection = mariadb.connect(host="10.2.0.181", user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.form:
        boodschappenlijst = request.form.getlist('boodschappenlijst')
        for i in boodschappenlijst:
            print(i)
    return render_template("index.html")


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = "SELECT productnaam FROM coop WHERE productnaam LIKE '%" + str(search) + "%' LIMIT 10"
    cursor.execute(query)
    results = [mv[0] for mv in cursor.fetchall()]
    return jsonify(matching_results=results)


@app.route("/minor")
def minor():
    return render_template("minor.html")


@app.route("/poster")
def poster():
    return render_template("poster.html")


if __name__ == "__main__":
    app.run()
