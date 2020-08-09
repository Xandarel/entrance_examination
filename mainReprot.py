from fresh_fish_interests import fish_interests
from report import frozen_fish_time
from bestBuy import buy
from no_pay import noMoney
from come_again import newBuy

print(f'интерес пользователь к продуктам и категориям \'fresh_fish\':\n {fish_interests()}')
print(f'категорию \'frozen_fish\' чаще всего просматривают в следующее время: \n{frozen_fish_time()}')
print(f'чаще всего с товаром \'semi_manufactures\' покупают \'{buy()}\'')
print(f'всего {noMoney()} не оплаченных корзин')
print(f'{newBuy()} пользователей совершали повторные покупки')
