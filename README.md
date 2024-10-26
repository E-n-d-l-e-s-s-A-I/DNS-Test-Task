# Оглавление
- [Постановка задачи](#Постановка-задачи)
- [Установка и запуск](#Установка-и-запуск)
- [спользуемые библиотеки](#Используемые-библиотеки)
- [Модель базы данных](#Модель-базы-данных)
- [Архитектура приложения](#Архитектура-приложения)
- [Эндпоинты](#Эндпоинты)
  - [Города](#Города)
  - [Магазины](#Магазины)
  - [Товары](#Товары)
  - [Продажи](#Продажи)

# Постановка задачи:
## Создать API для управления продажами в сети магазинов бытовой техники
### Используемый стэк
- Фреймворк для разработки -  FastAPI
- База данных - Postgres

### Сущности системы
- Товар
- Магазин
- Город (в одном городе может быть несколько магазинов)
- Продажи (одна продажа может содержать несколько товаров)

### Функциональность
- CRUD-операции на сущности Товар, Магазин, Город, Продажи
- Методы api для:
	- Получения продаж в разрезе:
		- Каждого города
		- Каждого магазина
		- Каждого товара
	- Получения продаж за последние **N** суток
	- Получения продаж с суммой более (или менее) **N**  денежных единиц
	- Получения продаж с количеством товаров более (или менее) **N** штук
	- Получения конкретных продаж (по идентификатору)
	- Все перечисленные выше пункты (в контексте продаж) должны быть комбинируемы (например, иметь возможность одновременно выбирать продажи с суммой более 5000 руб. и из города Владивостока) (* задача со звездочкой - считать как доп. балл)


### Дополнительные требования, Будет плюсом но не обязательно.
- Обеспечить миграции БД
- Обернуть в docker-контейнер
- Составить docker-compose

# Установка и запуск:
# Используемые библиотеки:
- _fastapi_ - для создания самого API
- _sqlalchemy_ - для работы с базой данных через ORM
- _asyncpg_ - асинхронный движок для работы с PostgreSQL
- _alembic_ - для управления миграциями базы данных
- _pytest_ - для написания автоматических тестов

# Модель базы данных:
Исходя из предметной области была спроектирована следующая база данных:

1) **City**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный
   - **name**: VARCHAR(255), NOT NULL, UNIQUE

2) **Store**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный
   - **name**: VARCHAR(255), NOT NULL, UNIQUE
   - **city_id**: INTEGER, FOREIGN KEY, ON_DELETE=CASCADE, NOT NULL, ссылается на `id` в таблице City-

3) **Product**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный
   - **name**: VARCHAR(255), NOT NULL, UNIQUE
   - **price**: Decimal(10, 2), NOT NULL, должна быть больше 0

4) **Sale**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный
   - **created_at**: DATETIME, NOT NULL
   - **store_id**: INTEGER, NOT NULL, ссылается на `id` в таблице Store

5) **Sale_products** - связывающая **Product** и **Sale** таблица
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный
   - **sale_id**: INTEGER, FOREIGN KEY, ON_DELETE=CASCADE, NOT NULL, ссылается на `id` в таблице Sale
   - **product_id**: INTEGER, FOREIGN KEY, ON_DELETE=CASCADE, NOT NULL, ссылается на `id` в таблице Product
   - **quantity**: INTEGER, NOT NULL, количество товара в продаже, должно быть больше 0
   - **unit_price**:  Decimal(10, 2), NOT NULL, цена товара на момент продажи, должна быть больше 0


![модель базы данных](readme_images/database_model.jpg)

# Архитектура приложения

# Эндпоинты
1. ## Города
- **GET /cities**
  - Описание: Получение списка всех городов
  - Ответ: Возвращает массив городов с их ID и названиями
	```
	[
      {
        "id": 1,
        "name": "Название города",
      },
      ...
	]
	```

- **POST /cities**
  - Описание: Добавление нового города
  - Тело запроса: 
  ```
  {
    "name": "Название города"
  }
  ```
  - Ответ: Возвращает ID добавленного города
  ```
  {
    "id": 3
  }
  ```
  - Ошибки:
    - 409 Conflict: При нарушении целостности бд. Например, если город с таким `name` уже существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `name` города это число

- **Get /cities/{city_id}**
  - Описание: Получение города по ID
  - Ответ: Возвращает название и ID города
  ```
  {
    "id": 1,
    "name": "Название города"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если город с таким`city_id` не найден

- **Patch /cities/{city_id}**
  - Описание: Частичное обновление информации о городе
  - Тело запроса: 
  ```
  {
    "name": "Новое название города"
  }
  ```
  - Ответ: Возвращает название и ID города
  ```
  {
    "id": 1,
    "name": "Новое название города"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если город с таким`city_id` не найден
    - 409 Conflict: При нарушении целостности бд. Например, если город с таким `name` уже существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `name` города это число

- **Delete /cities/{city_id}**
  - Описание: Удаление города по ID
  - Ответ: Возвращает название и ID города
  ```
  {
    "id": 1,
    "name": "Название города"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если город с таким`city_id` не найден

2. ## Магазины
- **GET /stores**
  - Описание: Получение списка всех магазинов
  - Ответ: Возвращает массив магазинов с их ID, названиями и ID города
	```
    [
      {
        "id": 1
        "name": "Название магазина",
        "city_id": 1
      },
      ...
    ]
	```

- **POST /stores**
  - Описание: Добавление нового магазина
  - Тело запроса: 
  ```
  {
    "name": "Название магазина",
    "city_id": 1
  }
  ```
  - Ответ: Возвращает ID добавленного магазина
  ```
  {
    "id": 1
  }
  ```
  - Ошибки:
    - 409 Conflict: При нарушении целостности бд. Например, если города с таким `city_id` не существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `name` магазина это число
  
- **Get /stores/{store_id}**
  - Описание: Получение магазина по ID
  - Ответ: Возвращает название магазина, ID магазина и ID города
  ```
  {
    "id": 1,
    "name": "Название магазина",
    "city_id": 1
  }
  ```
  - Ошибки:
    - 404 Not Found: Если магазин с таким`store_id` не найден

- **Patch /stores/{store_id}**
  - Описание: Частичное обновление информации о магазине
  - Тело запроса: 
  ```
  {
    "name": "Новое название магазина",
    "city_id": 1
  }
  ```
  - Ответ: Возвращает название магазина, ID магазина и ID города
  ```
  {
    "id": 1,
    "name": "Новое название магазина",
    "city_id": 1
  }
  ```
  - Ошибки:
    - 404 Not Found: Если магазин с таким`store_id` не найден
    - 409 Conflict: При нарушении целостности бд. Например, если города с таким `city_id` не существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `name` магазина это число

- **Delete /stores/{store_id}**
  - Описание: Удаление магазина по ID
  - Ответ: Возвращает название магазина, ID магазина и ID города
  ```
  {
    "id": 1,
    "name": "Название магазина",
    "city_id": 1
  }
  ```
  - Ошибки:
    - 404 Not Found: Если магазин с таким`store_id` не найден

3. ## Товары

- **GET /products**
  - Описание: Получение списка всех товаров
  - Ответ: Возвращает массив товаров с их ID, названиями и ценой
	```
    [
      {
        "id": 1,
        "name": "Название товара",
        "price": "11.11"
      },
      ...
     ]
	```

- **POST /products**
  - Описание: Добавление нового товара
  - Тело запроса: 
  ```
  {
    "name": "Название товара",
    "price": 11.11
  }
  ```
  \*`price` - должно быть числом > 0 и с количеством знаков после запятой <= 2
  - Ответ: Возвращает ID добавленного товара
  ```
  {
    "id": 1
  }
  ```
  - Ошибки:
    - 409 Conflict: При нарушении целостности бд. Например, если товар с таким `name` уже существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `price` задан с неправильным количеством знаков после запятой

- **Get /products/{product_id}**
  - Описание: Получение товара по ID
  - Ответ: Возвращает название товара, ID товара и его цену
  ```
  {
    "id": 3,
    "name": "Название товара",
    "price": "11.00",
    
  }
  ```
  - Ошибки:
    - 404 Not Found: Если товар с таким`product_id` не найден

- **Patch /products/{product_id}**
  - Описание: Частичное обновление информации о товаре
  - Тело запроса: 
  ```
  {
    "name": "Новое название товара",
    "price": "11.11"
  }
  ```
  \*`price` - должно быть числом > 0 и с количеством знаков после запятой <= 2
  - Ответ: Возвращает название товара, ID товара и его цену
  ```
  {
    "id": 1,
    "name": "Новое название товара",
    "price": "11.11"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если товар с таким`product_id` не найден
    - 409 Conflict: При нарушении целостности бд. Например, если товар с таким `name` уже существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `price` задан с неправильным количеством знаков после 

- **Delete /products/{product_id}**
  - Описание: Удаление товара по ID
  - Ответ: Возвращает название товара, ID товара и его цену
  ```
  {
    "id": 1,
    "name": "Название товара",
    "price": "11.11"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если товар с таким`product_id` не найден

4. ## Продажи
    
При запросах к эндпоинтам продаж следует учитывать, что для товаров всегда возвращается цена на момент создания продажи.

- **POST /sales**
  - Описание: Добавление новой продажи
  - Тело запроса: 
  ```
  {
    "store_id": 1,
    "products": [
      {
        "quantity": 1,
        "product_id": 1
      },
      ...
    ]
  }
  ```
  \*`quantity` - должно быть целым числом > 0
  - Ответ: Возвращает ID добавленной продажи
  ```
  {
    "id": 1
  }
  ```
  - Ошибки:
    - 409 Conflict: При нарушении целостности бд. Например, если магазин с `store_id` не существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `quantity` меньше 1

- **Get /sales/{sale_id}**
  - Описание: Получение продажи по ID
  - Ответ: Возвращает ID продажи, ID магазина, и массив товаров продажи
  ```
  {
    "id": 1,
    "store_id": 1,
    "products": [
      {
        "quantity": 1,
        "product_id": 1,
        "unit_price": "12.11"
      },
      ...
    ]
  }
  ```
  - Ошибки:
    - 404 Not Found: Если продажа с таким`sale_id` не найдена

- **Patch /sales/{sale_id}**
  - Описание: Частичное обновление информации о самой продаже, но не о товарах продажи. Взаимодействие с товарами продажи происходит по эндпоинтам *`/sales/{sale_id}/products/...`*
  - Тело запроса: 
  ```
  {
    "store_id": 2
  }
  ```
  - Ответ: Возвращает ID продажи, ID магазина, и массив товаров продажи
  ```
  {
    "id": 1,
    "store_id": 2,
    "products": [
      {
        "quantity": 1,
        "product_id": 1,
        "unit_price": "12.11"
      },
      ...
    ]
  }
  ```
  - Ошибки:
    - 404 Not Found: Если продажа с таким`sale_id` не найдена
    - 409 Conflict: При нарушении целостности бд. Например, если магазин с таким `store_id` не существует в бд
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `store_id` не число

- **Delete /sales/{sale_id}**
  - Описание: Удаление продажи по ID
  - Ответ: Возвращает ID продажи, ID магазина, и массив товаров продажи
  ```
  {
    "id": 1,
    "store_id": 2,
    "products": [
      {
        "quantity": 1,
        "product_id": 1,
        "unit_price": "12.11"
      },
      ...
    ]
  }
  ```
  - Ошибки:
    - 404 Not Found: Если продажа с таким`sale_id` не найдена

- **Get /sales/{sale_id}/products**
  - Описание: Получение списка товаров продажи по ее ID. В отличие от **`Get /sales/{sale_id}`** возвращает детальную информации о каждом товаре, включая его название.
  - Ответ: Возвращает Массив товаров продажи
  ```
  [
    {
      "id": 1,
      "name": "Название товара",
      "quantity": 1,
      "unit_price": "11.11"
    },
    ...
  ]
  ```
  - Ошибки:
    - 404 Not Found: Если продажа с таким`sale_id` не найдена

- **POST /sales/{sale_id}/products**
  - Описание: Добавление нового товара в продажу. Добавляет именно еще не присутствующий в продаже товар. Если товар уже присутствует в продаже вернет 409. Для взаимодействия с ним стоим обращаться к эндпоинту **`/sales/{sale_id}/products/{product_id}`**
  - Тело запроса: 
  ```
  {
    "quantity": 1,
    "product_id": 1
  }
  ```
  \*`quantity` - должно быть целым числом > 0
  - Ответ: Возвращает ID продажи, ID магазина, и обновленный массив товаров продажи
  ```
  {
    "id": 1,
    "store_id": 1,
    "products": [
      {
        "product_id": 1,
        "quantity": 1,
        "unit_price": "11.11"
      },
      ...
    ]
  }
  ```
  - Ошибки:
    - 404 Not Found: Если продажа с таким`sale_id` или товар с `product_id` не найдены
    - 409 Conflict: При нарушении целостности бд. Например, если товар с `product_id` уже присутствует в продаже
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `quantity` меньше 1

- **Patch /sales/{sale_id}/products/{product_id}**
  - Описание: Частичное обновление информации о товаре продажи
  - Тело запроса: 
  ```
  {
    "quantity": 2
  }
  ```
  - Ответ: Возвращает ID товара, количество товара, и его цену на момент заказа
  ```
  {
    "product_id": 1,
    "quantity": 2
    "unit_price": "11.11"
  }
  ```
  - Ошибки:
    - 404 Not Found: Если товар с `product_id` в продаже с `sale_id` не найден
    - 422 Unprocessable Entity: При некорректном теле запроса. Например, если `quantity` меньше 1

- **Delete /sales/{sale_id}/products/{product_id}**
  - Описание: Удаление товара из продажи
  - Ответ: Возвращает ID товара, количество товара, и его цену на момент заказа
  ```
    {
      "product_id": 1,
      "quantity": 1,
      "unit_price": "11.11"
    }
  ```
  - Ошибки:
    - 404 Not Found: Если товар с `product_id` в продаже с `sale_id` не найден