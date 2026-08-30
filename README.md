# xveco

Librería avanzada de economía, bancos, mercados e inventarios en Python, con soporte de peso, volumen, durabilidad, podrición y contenedores.

**Versión:** 2.1.5
**Licencia:** AGPLv3 o posterior
**Python:** >=3.8

## Instalación

```bash
pip install xveconomy
```

## Características

- Monedas con conversión a EUR e inflación
- Bancos con préstamos, deudas e intereses
- Cuentas con saldo, inventario, peso y volumen máximos
- Ítems con durabilidad y podrición basada en tiempo
- Contenedores (mochilas) con límites propios de peso y huecos
- Mercado con precios dinámicos según oferta/demanda
- Sistema de intercambios (trades) entre cuentas

## Uso básico

### Moneda y cuenta

```python
from xveco import Currency, Account

euro = Currency("Euro", "€", 1.0, logo="💶")
cuenta = Account("Jugador1", euro)

cuenta.deposit(100)
cuenta.show_balance()
```

### Banco

```python
from xveco import Bank

banco = Bank(euro, supply=10000)

banco.loan(cuenta, 500, interest=5)
print(banco.calculate_debt(cuenta))

banco.pay_debt(cuenta)
```

### Ítems e inventario

```python
from xveco import Item, ItemInstance

manzana = Item("manzana", "Manzana", base_price=2, weight=0.2, volume=0.1, rots=True, decay_time=60)
instancia = ItemInstance(manzana)

cuenta.add_item_instance(instancia)
print(instancia.get_current_decay())
```

### Contenedores

```python
from xveco import Container

mochila = Container("mochila1", "Mochila básica", max_container_slots=10, max_weight=20)
mochila.add_item(instancia)
```

### Mercado

```python
from xveco import Market

mercado = Market(euro)
mercado.register_item(manzana)

mercado.buy(cuenta, "manzana", qty=3)
mercado.sell(cuenta, "manzana", qty=1)
```

### Intercambios (Trade)

```python
from xveco import Trade

cuenta2 = Account("Jugador2", euro)
trade = Trade(cuenta, cuenta2)

trade.add_offer(cuenta, items=[], money=50)
trade.add_offer(cuenta2, items=[instancia], money=0)

trade.accept(cuenta)
trade.accept(cuenta2)
```

## Clases principales

| Clase | Descripción |
|---|---|
| `Currency` | Moneda con valor a EUR e inflación |
| `Bank` | Préstamos, deudas y suministro de dinero |
| `Item` | Definición de un ítem (plantilla) |
| `ItemInstance` | Instancia concreta de un ítem, con durabilidad/podrición |
| `Container` | Contenedor con límites de peso y huecos |
| `Account` | Cuenta de usuario con saldo e inventario |
| `Market` | Mercado con precios dinámicos |
| `Trade` | Intercambio entre dos cuentas |

## Licencia

Este proyecto está licenciado bajo la GNU Affero General Public License v3 o posterior (AGPLv3).

## Enlaces

- Repositorio: [https://github.com/Siaro01/xveco](https://github.com/Siaro01/xveco)