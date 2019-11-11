from flask import Flask, Response, render_template, request, url_for, jsonify
import mysql.connector as mariadb

app = Flask(__name__)

mariadb_connection = mariadb.connect(host="213.190.22.172", user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.form:
        boodschappenlijst = request.form.getlist('boodschappenlijst')


        pricelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}

        for item in boodschappenlijst:
            print(item)
            for key in pricelist.keys():
                query = "SELECT prijs FROM {table} WHERE productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                cursor.execute(query.format(table=key), ("%" + item + "%",))
                for prices in cursor.fetchall():
                    pricelist['coop'].append(prices[0])

        print(pricelist)

        total_prices = {'coop': 0, 'jumbo': 0, 'aldi': 0, 'albert_heijn': 0}

        for key in pricelist.keys():
            for price in pricelist[key]:
                total_prices[key] += float(price)

            total_prices[key] = "{:.2f}".format(total_prices[key])

        print(total_prices)

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
