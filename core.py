import time

class Currency:
    def __init__(self, name, symbol, value_to_eur, logo=None):
        self.name = name
        self.symbol = symbol
        self.value_to_eur = value_to_eur
        self.logo = logo
        self.accounts = []

    def apply_inflation(self, percent):
        self.value_to_eur *= (1 + percent / 100)

    def show_accounts(self):
        return [a.name for a in self.accounts]

    def total_money(self):
        return sum(a.balance for a in self.accounts)


class Bank:
    def __init__(self, currency, supply):
        self.currency = currency
        self.supply = int(supply * 100)

    def loan(self, account, amount, interest):
        cents = int(amount * 100)
        if cents > self.supply:
            raise ValueError("el banco no tiene suficiente dinero")
        self.supply -= cents
        account.balance += cents
        account.debts.append({
            "amount": cents,
            "interest": interest
        })

    def calculate_debt(self, account):
        total = 0
        for d in account.debts:
            total += int(d["amount"] * (1 + d["interest"] / 100))
        return total

    def pay_debt(self, account):
        total = self.calculate_debt(account)
        if account.balance < total:
            raise ValueError("no puedes pagar la deuda")
        account.balance -= total
        account.debts.clear()

    def deposit_supply(self, amount):
        self.supply += int(amount * 100)

    def show_supply(self):
        return self.supply / 100


class Item:
    def __init__(self, item_id, name, base_price, weight=1.0, volume=1.0, max_durability=None, rots=False, decay_time=0):
        self.item_id = item_id
        self.name = name
        self.base_price = base_price
        self.weight = weight
        self.volume = volume
        self.max_durability = max_durability
        self.rots = rots
        self.decay_time = decay_time


class ItemInstance:
    def __init__(self, item, durability=None, metadata=None):
        self.item = item
        self.durability = durability if durability is not None else item.max_durability
        self.metadata = metadata or {}
        self.creation_time = time.time()

    def get_current_decay(self):
        if not self.item.rots or self.item.decay_time == 0:
            return 0.0
        elapsed = time.time() - self.creation_time
        return min(1.0, elapsed / self.item.decay_time)


class Container:
    def __init__(self, container_id, name, max_container_slots, max_weight=50.0):
        self.container_id = container_id
        self.name = name
        self.max_container_slots = max_container_slots
        self.max_weight = max_weight
        self.items = []

    def total_weight(self):
        return sum(i.item.weight for i in self.items)

    def add_item(self, item_instance):
        if self.total_weight() + item_instance.item.weight > self.max_weight:
            raise ValueError("la mochila excede su peso máximo")
        if len(self.items) >= self.max_container_slots:
            raise ValueError("la mochila está llena de huecos")
        self.items.append(item_instance)


class Account:
    def __init__(self, name, currency, max_inventory=32, max_weight=100.0, max_volume=100.0):
        self.name = name
        self.currency = currency
        self.balance = 0
        self.debts = []

        self.max_inventory = max_inventory
        self.max_weight = max_weight
        self.max_volume = max_volume
        
        self.inventory = []
        self.currency.accounts.append(self)

    def deposit(self, amount):
        self.balance += int(amount * 100)

    def withdraw(self, amount):
        cents = int(amount * 100)
        if cents > self.balance:
            raise ValueError("no tienes suficiente saldo")
        self.balance -= cents

    def transfer(self, other_account, amount):
        cents = int(amount * 100)
        if cents <= 0:
            raise ValueError("cantidad inválida")
        self.withdraw(amount)
        other_account.deposit(amount)

    def balance_in_eur(self):
        return self.balance / 100 * self.currency.value_to_eur

    def show_balance(self):
        euros = self.balance / 100
        logo = self.currency.logo or ""
        print(f"{logo} {self.name}: {euros:,.2f} {self.currency.symbol}"
              .replace(",", "X").replace(".", ",").replace("X", "."))

    def current_weight(self):
        weight = sum(i.item.weight for i in self.inventory)
        for i in self.inventory:
            if isinstance(i.metadata.get("container"), Container):
                weight += i.metadata["container"].total_weight()
        return weight

    def current_volume(self):
        return sum(i.item.volume for i in self.inventory)

    def inventory_used_slots(self):
        return len(self.inventory)

    def has_item_type(self, item_id, qty=1):
        count = sum(1 for i in self.inventory if i.item.item_id == item_id)
        return count >= qty

    def add_item_instance(self, item_instance):
        if self.inventory_used_slots() >= self.max_inventory:
            raise ValueError("inventario lleno (slots máximos alcanzados)")
        if self.current_weight() + item_instance.item.weight > self.max_weight:
            raise ValueError("sobrepasas el límite de peso")
        if self.current_volume() + item_instance.item.volume > self.max_volume:
            raise ValueError("sobrepasas el límite de volumen")
        self.inventory.append(item_instance)

    def remove_item_type(self, item_id, qty=1):
        removed = 0
        for i in list(self.inventory):
            if i.item.item_id == item_id:
                self.inventory.remove(i)
                removed += 1
                if removed >= qty:
                    return
        raise ValueError("no tienes suficientes ítems de ese tipo")


class Market:
    def __init__(self, currency):
        self.currency = currency
        self.items = {}
        self.price_multiplier = {}

    def register_item(self, item):
        self.items[item.item_id] = item
        self.price_multiplier[item.item_id] = 1.0

    def get_price(self, item_id):
        item = self.items[item_id]
        return item.base_price * self.price_multiplier[item_id]

    def buy(self, account, item_id, qty=1):
        price = self.get_price(item_id) * qty
        account.withdraw(price)
        for _ in range(qty):
            account.add_item_instance(ItemInstance(self.items[item_id]))
        self.price_multiplier[item_id] *= 1.01

    def sell(self, account, item_id, qty=1):
        if not account.has_item_type(item_id, qty):
            raise ValueError("no tienes ese item")
        price = self.get_price(item_id) * qty
        account.deposit(price)
        account.remove_item_type(item_id, qty)
        self.price_multiplier[item_id] *= 0.99


class Trade:
    def __init__(self, account_a, account_b):
        self.account_a = account_a
        self.account_b = account_b
        
        self.offer_a_items = []
        self.offer_a_money = 0
        self.offer_b_items = []
        self.offer_b_money = 0
        
        self.accepted_a = False
        self.accepted_b = False

    def add_offer(self, account, items=[], money=0):
        if account == self.account_a:
            self.offer_a_items = items
            self.offer_a_money = money
        elif account == self.account_b:
            self.offer_b_items = items
            self.offer_b_money = money
        else:
            raise ValueError("la cuenta no forma parte de este intercambio")

    def accept(self, account):
        if account == self.account_a:
            self.accepted_a = True
        elif account == self.account_b:
            self.accepted_b = True
        
        if self.accepted_a and self.accepted_b:
            self.execute_trade()

    def execute_trade(self):
        if self.account_a.balance < int(self.offer_a_money * 100):
            raise ValueError("Cuenta A no tiene suficiente saldo")
        if self.account_b.balance < int(self.offer_b_money * 100):
            raise ValueError("Cuenta B no tiene suficiente saldo")

        if self.offer_a_money > 0:
            self.account_a.transfer(self.account_b, self.offer_a_money)
        if self.offer_b_money > 0:
            self.account_b.transfer(self.account_a, self.offer_b_money)

        for item in self.offer_a_items:
            self.account_a.inventory.remove(item)
            self.account_b.add_item_instance(item)

        for item in self.offer_b_items:
            self.account_b.inventory.remove(item)
            self.account_a.add_item_instance(item)

        print("¡Intercambio realizado con éxito!")