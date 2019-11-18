from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import os
import base64
import mysql.connector as mariadb

app = Flask(__name__)
Session(app)

mariadb_connection = mariadb.connect(host="213.190.22.172", port=3306, user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()


@app.route("/", methods=['GET', 'POST'])
def home():
    # Wanneer de form gesubmit wordt en er dus producten gestuurd worden naar de back-end
    # worden deze in de boodschappenlijst variabele gestopt.
    if request.form:
        boodschappenlijst = request.form.getlist('boodschappenlijst')

        pricelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}
        namelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}

        # Wanneer het productveld niet leeg is wordt dit product in elk van de vier supermarkt database tables
        # gezocht om daarna het goedkoopste product per supermarkt als sessie variabele op te slaan.
        # Dit prouct wordt dan bij naam en prijs opgeslagen en weergegeven op /results pagina.
        for item in boodschappenlijst:
            if item is not "":
                split_item = item.split()
                for key in pricelist.keys():
                    like_list = []
                    extra_param = ""
                    new_cursor = mariadb_connection.cursor()
                    for i in range(len(split_item)):
                        if i > 0:
                            extra_param += " AND productnaam LIKE %s"
                        else:
                            extra_param = ""
                        like_list.append("%" + split_item[i] + "%")

                    # In de dynamische query hieronder wordt telkens een extra parameter (AND productnaam LIKE %s)
                    # toegevoegd wanneer er een extra invoerveld aangemaakt wordt op de frontend.
                    query = "SELECT productnaam, prijs FROM {table} WHERE productnaam LIKE %s" + extra_param + " AND NOT prijs = 0.0 \
                                            ORDER BY prijs ASC LIMIT 1"

                    new_cursor.execute(query.format(table=key), like_list)

                    for product in new_cursor.fetchall():
                        namelist[key].append(product[0])
                        pricelist[key].append(product[1])
                    new_cursor.close()

        session['names_list_coop'] = namelist['coop']
        session['names_list_jumbo'] = namelist['jumbo']
        session['names_list_aldi'] = namelist['aldi']
        session['names_list_ah'] = namelist['albert_heijn']

        total_prices = {'coop': 0, 'jumbo': 0, 'aldi': 0, 'albert_heijn': 0}

        # Als laatste wordt de totale prijs per supermarkt hieronder berekend.
        # Daarna wordt deze ook als sessie variabele aangemaakt.
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
    like_list = []
    extra_param = ""

    # Net zoals in de home functie wordt hieronder een dynamische query opgesteld.
    for i in range(len(split_search)):
        if i > 0:
            extra_param += " AND productnaam LIKE %s"
        else:
            extra_param = ""
        like_list.append("%" + split_search[i] + "%")

    query = "SELECT productnaam FROM jumbo WHERE productnaam LIKE %s" + extra_param + " LIMIT 20"
    cursor.execute(query, like_list)

    # Hieronder wordt gekeken naar de eerste twee trefwoorden, door spatie gescheiden, waarop gezocht wordt.
    # Deze worden vergeleken met bestaande producten die uit de query gehaald worden en kan er zo een autocomplete
    # ontstaan, waarbij de eerste twee zoektermen automatisch aangevuld kunnen worden.
    query_results = [item[0].lower() for item in cursor.fetchall()]
    similar_products = []
    full_string = ""
    for item in query_results:
        split_item = item.split()
        for string in split_item:
            if split_search[0] in string:
                full_string = string
                similar_products.append(full_string)
            elif len(split_search) == 2:
                if split_search[0] in full_string and split_search[1] in string:
                    full_string += " " + string
                    similar_products.append(full_string)

    top10_search_results = list(set(similar_products[:10]))
    return jsonify(matching_results=top10_search_results)


@app.route("/results")
def results():
    # Deze functie is vooral bedoeld om de sessie variabele door te geven aan de /results pagina om
    # aan de gebruiker te tonen.
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
    # Er wordt een random sessie_id gegenereerd voor de website.
    session_id_bytes = os.urandom(64)
    session_id = base64.b64encode(session_id_bytes)

    app.secret_key = session_id
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run()
