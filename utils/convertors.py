def price_split(base_price):
    base_price = str(base_price)
    counter = len(base_price) - 1
    counter2 = 0
    price_export = ''
    while counter >= 0:
        if counter2 < 3:
            price_export = base_price[counter] + price_export
            counter -= 1
            counter2 += 1
        else:
            price_export = base_price[counter] + ',' + price_export
            counter -= 1
            counter2 = 1
    return price_export