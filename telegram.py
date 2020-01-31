from telegram.ext import Updater, CommandHandler
import mysql.connector as mariadb
mariadb_connection = mariadb.connect(host="192.168.192.2", user="s4dpython", password="s4dpython", database="producten")
cursor = mariadb_connection.cursor()

def groceries(update, context):
    products = update.message.text.split(" ",1)[1].split(",")

    pricelist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}
    itemlist = {'coop': [], 'jumbo': [], 'aldi': [], 'albert_heijn': []}
    for item in products:
        split_item = item.split()
        print(split_item)
        for key in pricelist.keys():
            new_cursor = mariadb_connection.cursor()
            if len(split_item) == 1:
                query = "SELECT prijs,productnaam FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                ORDER BY prijs ASC LIMIT 1"
                new_cursor.execute(query.format(table=key), ("%" + split_item[0] + "%",))
            elif len(split_item) == 2:
                query = "SELECT prijs,productnaam FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                new_cursor.execute(query.format(table=key),
                                   ("%" + split_item[0] + "%", "%" + split_item[1] + "%",))
            else:
                query = "SELECT prijs,productnaam FROM {table} WHERE productnaam LIKE %s AND NOT prijs = 0.0 \
                productnaam LIKE %s AND productnaam LIKE %s ORDER BY prijs ASC LIMIT 1"
                new_cursor.execute(query.format(table=key),
                                   ("%" + split_item[0] + "%", "%" + split_item[1] + "%", "%" + split_item[2] + "%"))
            for prices in new_cursor.fetchall():
                pricelist[key].append(prices[0])
                itemlist[key].append(prices[1])
            new_cursor.close()
    total_prices = {'coop': 0, 'jumbo': 0, 'aldi': 0, 'albert_heijn': 0}

    cheapest_name = ""
    cheapest_price = 99999

    for key in pricelist.keys():
        for price in pricelist[key]:
            total_prices[key] += float(price)

        if total_prices[key] < cheapest_price:
            cheapest_name = key
            cheapest_price = total_prices[key]

        total_prices[key] = "{:.2f}".format(total_prices[key])

    print(total_prices)
    update.message.reply_text("""Coop: €{coop} 
    Jumbo: €{jumbo}
    Aldi: €{aldi}
    Albert Heijn: €{albert_heijn}
    """"".format(**total_prices))

    update.message.reply_text("De goedkoopste winkel is {0}".format(cheapest_name))
    update.message.reply_text("\n".join(itemlist[cheapest_name]))

updater = Updater('*************************', use_context=True)
updater.dispatcher.add_handler(CommandHandler('boodschappen', groceries))

updater.start_polling()
updater.idle()
