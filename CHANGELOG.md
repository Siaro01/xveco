# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2.0.0] - 2026-08-30

### Añadido
* **Sistema de Instancias (`ItemInstance`)**: Los objetos ahora son únicos, permitiendo guardar metadatos, rastrear durabilidad individual y calcular desgaste/pudrición con el tiempo (`get_current_decay()`).
* **Contenedores (`Container`)**: Nuevo sistema de mochilas que ocupan espacio en el inventario principal pero añaden capacidad interna (`max_container_slots`, `max_weight`).
* **Físicas de Inventario**: Añadidos límites de peso (`max_weight`) y volumen (`max_volume`) globales para las cuentas (`Account`), sumando dinámicamente el contenido de los contenedores.
* **Propiedades de Ítems (`Item`)**: Nuevos atributos para definir peso, volumen, durabilidad máxima, si se pudre (`rots`) y el tiempo de degradación (`decay_time`).
* **Sistema de Intercambio (`Trade`)**: Transacciones seguras y atómicas (items y dinero simultáneos) entre dos cuentas, validando previamente los límites de saldo, peso y espacio.

### Cambiado
* **Estructura del Inventario**: La clase `Account` ahora utiliza una lista de `ItemInstance` en lugar de un diccionario simple de cantidades, imponiendo un límite de slots (`max_inventory`).
* **Mercado Actualizado**: Las funciones `buy` y `sell` de la clase `Market` ahora generan e interactúan con instancias únicas (`ItemInstance`) al procesar compras.
* **Licencia**: Actualizada la licencia del proyecto a GNU Affero General Public License v3 (AGPLv3).