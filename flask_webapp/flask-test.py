from flask import Flask, render_template, request, jsonify, session, redirect, url_for, json
from flask_session import Session
import mysql.connector as mariadb

app = Flask(__name__)
Session(app)

mariadb_connection = mariadb.connect(host="213.190.22.172", user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()

prices_global_list = []

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.form:
        boodschappenlijst = request.form.getlist('boodschappenlijst')

        pricelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}
        namelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}

        for item in boodschappenlijst:
            split_item = item.split()
            print(split_item)
            for key in pricelist.keys():
                new_cursor = mariadb_connection.cursor()
                if len(split_item) == 1:
                    query = "SELECT productnaam, prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key), ("%" + split_item[0] + "%",))
                elif len(split_item) == 2:
                    query = "SELECT productnaam, prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key),
                                       ("%" + split_item[0] + "%", "%" + split_item[1] + "%", ))
                else:
                    query = "SELECT productnaam, prijs FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                    productnaam LIKE %s AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                    new_cursor.execute(query.format(table=key),
                                       ("%" + split_item[0] + "%", "%" + split_item[1] + "%", "%" + split_item[2] + "%"))
                for object in new_cursor.fetchall():
                    pricelist[key].append(object[1])
                    namelist[key].append(object[0])

                new_cursor.close()

        #session['prices_list_coop'] = pricelist['coop']
        #session['prices_list_jumbo'] = pricelist['jumbo']
        #session['prices_list_aldi'] = pricelist['aldi']
        #session['prices_list_ah'] = pricelist['albert_heijn']

        session['names_list_coop'] = namelist['coop']
        session['names_list_jumbo'] = namelist['jumbo']
        session['names_list_aldi'] = namelist['aldi']
        session['names_list_ah'] = namelist['albert_heijn']

        total_prices = {'coop': 0, 'jumbo': 0, 'aldi': 0, 'albert_heijn': 0}

        for key in pricelist.keys():
            for price in pricelist[key]:
                total_prices[key] += float(price)

            total_prices[key] = "{:.2f}".format(total_prices[key])

        session['total_prices_coop'] = total_prices['coop']
        session['total_prices_jumbo'] = total_prices['jumbo']
        session['total_prices_aldi'] = total_prices['aldi']
        session['total_prices_ah'] = total_prices['albert_heijn']

        return redirect(url_for('results'))
    return render_template("index.html")


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q').lower()
    split_search = search.split()
    if len(split_search) == 1:
        query = "SELECT productnaam FROM jumbo WHERE productnaam LIKE %s LIMIT 20"
        cursor.execute(query, ("%" + str(split_search[0]) + "%",))
    elif len(split_search) == 2:
        query = "SELECT productnaam FROM jumbo WHERE productnaam LIKE %s AND productnaam LIKE %s LIMIT 20"
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


@app.route("/results")
def results():
    coop_names = session.get('names_list_coop', None)
    jumbo_names = session.get('names_list_jumbo', None)
    aldi_names = session.get('names_list_aldi', None)
    ah_names = session.get('names_list_ah', None)
    coop_price = session.get('total_prices_coop', None)
    jumbo_price = session.get('total_prices_jumbo', None)
    aldi_price = session.get('total_prices_aldi', None)
    ah_price = session.get('total_prices_ah', None)
    return render_template("results.html", coop_names=coop_names, jumbo_names=jumbo_names, aldi_names=aldi_names,
                           ah_names=ah_names, coop_price=coop_price, jumbo_price=jumbo_price, aldi_price=aldi_price,
                           ah_price=ah_price)


@app.route("/minor")
def minor():
    return render_template("minor.html")


@app.route("/poster")
def poster():
    return render_template("poster.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run()


