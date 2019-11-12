from flask import Flask, render_template, request, jsonify
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
            split_item = item.split()
            print(split_item)
            for key in pricelist.keys():
                new_cursor = mariadb_connection.cursor()
                if len(split_item) == 1:
                    query = "SELECT prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key), ("%" + split_item[0] + "%",))
                elif len(split_item) == 2:
                    query = "SELECT prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key),
                                       ("%" + split_item[0] + "%", "%" + split_item[1] + "%", ))
                else:
                    query = "SELECT prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    productnaam LIKE %s AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key),
                                       ("%" + split_item[0] + "%", "%" + split_item[1] + "%", "%" + split_item[2] + "%"))
                for prices in new_cursor.fetchall():
                    pricelist[key].append(prices[0])
                new_cursor.close()

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
    search = request.args.get('q').lower()
    split_search = search.split()
    if len(split_search) == 1:
        query = "SELECT productnaam FROM coop WHERE productnaam LIKE %s LIMIT 20"
        cursor.execute(query, ("%" + str(split_search[0]) + "%",))
    elif len(split_search) == 2:
        query = "SELECT productnaam FROM coop WHERE productnaam LIKE %s AND productnaam LIKE %s LIMIT 20"
        cursor.execute(query, ("%" + str(split_search[0]) + "%", "%" + str(split_search[1]) + "%",))
    results = [mv[0].lower() for mv in cursor.fetchall()]

    print(split_search[0])

    splitter = []

    substring = ""
    for item in results:
        split_item = item.split()
        for string in split_item:
            if split_search[0] in string:
                substring = string
                splitter.append(substring)
            elif len(split_search) == 2:
                if split_search[0] in substring and split_search[1] in string:
                    substring += " " + string
                    splitter.append(substring)

    top5_search_results = list(set(splitter[:10]))
    return jsonify(matching_results=top5_search_results)


@app.route("/minor")
def minor():
    return render_template("minor.html")


@app.route("/poster")
def poster():
    return render_template("poster.html")


if __name__ == "__main__":
    app.run()


