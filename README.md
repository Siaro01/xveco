# xveco

Librería de economía simulada para Python.

xveco permite crear monedas, cuentas bancarias, sistemas de inflación, bancos y préstamos de forma sencilla. Está pensada para videojuegos, bots, simulaciones económicas y proyectos educativos.

---

## 💰 Características

* Monedas personalizadas
* Cuentas con saldo en céntimos
* Depósitos y retiradas
* Transferencias entre usuarios
* Conversión a euros
* Sistema de inflación
* Bancos con dinero limitado
* Préstamos con interés
* Gestión de deudas
* API simple y fácil de usar

---

## 📦 Instalación

```bash
pip install xveco
```

---

## 🚀 Ejemplo completo

```python
import xveco

# Crear moneda
coin = xveco.Currency(
    "XCoin",
    "X",
    0.5,
    "🪙"
)

# Crear cuentas
santi = xveco.Account("Santi", coin)
pepe = xveco.Account("Pepe", coin)

# Ingresar dinero
santi.deposit(100)
pepe.deposit(50)

# Transferir dinero
santi.transfer(pepe, 25)

# Mostrar saldos
santi.show_balance()
pepe.show_balance()

# Aplicar inflación
coin.apply_inflation(10)

print("Saldo de Santi en euros:", santi.balance_in_eur())
```

Salida aproximada:

```text
🪙 Santi: 75,00 X
🪙 Pepe: 75,00 X

Saldo de Santi en euros: 41.25
```

---

# 📚 Documentación

## 🪙 Currency

Representa una moneda.

### Crear una moneda

```python
coin = xveco.Currency(
    "XCoin",
    "X",
    0.5,
    "🪙"
)
```

### Parámetros

| Parámetro    | Tipo       | Descripción            |
| ------------ | ---------- | ---------------------- |
| name         | str        | Nombre de la moneda    |
| symbol       | str        | Símbolo de la moneda   |
| value_to_eur | float      | Valor respecto al euro |
| logo         | str | None | Emoji o texto opcional |

### Aplicar inflación

```python
coin.apply_inflation(10)
```

Incrementa el valor de la moneda un 10%.

---

## 👤 Account

Representa una cuenta bancaria.

### Crear una cuenta

```python
user = xveco.Account("Usuario", coin)
```

### Ingresar dinero

```python
user.deposit(100)
```

### Retirar dinero

```python
user.withdraw(50)
```

### Transferir dinero

```python
user1.transfer(user2, 25)
```

### Mostrar saldo

```python
user.show_balance()
```

Ejemplo:

```text
🪙 Usuario: 125,00 X
```

### Obtener saldo en euros

```python
print(user.balance_in_eur())
```

---

## 🏦 Bank

Representa un banco con una cantidad limitada de dinero.

### Crear banco

```python
bank = xveco.Bank(
    coin,
    10000
)
```

---

### Conceder préstamo

```python
bank.loan(
    santi,
    100,
    10
)
```

Parámetros:

| Parámetro | Descripción                   |
| --------- | ----------------------------- |
| account   | Cuenta que recibe el préstamo |
| amount    | Cantidad prestada             |
| interest  | Interés (%)                   |

---

### Calcular deuda

```python
debt = bank.calculate_debt(santi)

print(debt)
```

---

### Pagar deuda

```python
bank.pay_debt(santi)
```

---

## 💡 Ejemplo de préstamo

```python
import xveco

coin = xveco.Currency(
    "XCoin",
    "X",
    1,
    "🪙"
)

bank = xveco.Bank(
    coin,
    1000
)

santi = xveco.Account(
    "Santi",
    coin
)

bank.loan(
    santi,
    100,
    10
)

print(
    "Deuda:",
    bank.calculate_debt(santi)
)

santi.deposit(20)

bank.pay_debt(santi)

santi.show_balance()
```

---

## ⚙️ Cómo funciona internamente

Los saldos se almacenan en céntimos para evitar errores de precisión causados por números decimales.

Ejemplo:

```python
user.deposit(1.50)
```

Internamente:

```python
150
```

---

## 🎯 Casos de uso

* Bots de Discord
* Videojuegos
* RPGs
* Sistemas de comercio
* Simulaciones económicas
* Proyectos educativos
* Experimentos financieros

---

## 🛣️ Roadmap

Funciones previstas para futuras versiones:

* [ ] Persistencia en archivos
* [ ] Historial de transacciones
* [ ] Impuestos
* [ ] Mercado de recursos
* [ ] Intercambio entre monedas
* [ ] Soporte para múltiples bancos
* [ ] Intereses periódicos
* [ ] Estadísticas económicas

---

## 🤝 Contribuir

Las contribuciones, sugerencias y reportes de errores son bienvenidos.

Puedes abrir un Issue o enviar un Pull Request.

---

## 📄 Licencia

MIT License.

---

Desarrollado con Python.
