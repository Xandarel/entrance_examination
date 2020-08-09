from geoip import geolite2

with open('logs.txt') as logs:
    none = 0
    for s in logs:
        text = s.split()

        ip = text[6]
        match = geolite2.lookup(text[6])
        if match is not None:
            country = match.country
        else:
            pass

        url = text[-1]
        url_path = url.replace('https://all_to_the_bottom.com/', '')
        url_main = url_path.split('/')

        if len(url_main) == 2:  # Только категория или сообщение об успешной оплате
            if 'success_pay' in url_main[0]:
                cart_id = int(url_main[0].replace('success_pay_', ''))
            else:
                category_name = url_main[0]
        elif len(url_main) == 3:  # Пользоватеь зашел в продукт
            category_name = url_main[0]
            product_name = url_main[1]
            print(product_name, category_name)
        elif len(url_main) == 1:  # Или он добавил в карзину, или оплачивает
            # Добавляет в карзину
            if 'cart?' in url_main[0]:
                add_cart = url_main[0].replace('cart?', '')
                add_dict = {sub.split("=")[0]: int(sub.split("=")[1]) for sub in add_cart[:-1].split('&')}
                print(add_dict)
            elif 'pay?' in url_main[0]:  # оплачивает
                pay_cart = url_main[0].replace('pay?', '')
                pay_dict = {sub.split("=")[0]: sub.split("=")[1] for sub in add_cart[:-1].split('&')}

        time = text[3]
        h, m, s = map(int, time.split(':'))
        totalSeconds = int(h) * 3600 + int(m) * 60 + int(s)
