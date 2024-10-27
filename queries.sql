INSERT INTO city (name) VALUES
('Владивосток'),
('Хабаровск'),
('Москва');

INSERT INTO store (name, city_id) VALUES
('DNS на Некрасовской', 1),
('DNS на Постышева', 1),
('DNS Даниловского', 2),
('DNS на Ленина', 2);

INSERT INTO product (name, price) VALUES
('Клавиатура проводная KEYRON Eclipse', 10),
('Проводные наушники HyperX Cloud II_2022 KHX-HSCP-GM серый', 100),
('6.56" Смартфон Tecno SPARK GO 2024 64 ГБ черный', 1000),
('27" Монитор Xiaomi G27i черный', 10000);

INSERT INTO sale (store_id) VALUES
(1),
(1),
(2),
(3),
(3);

INSERT INTO sale_products (sale_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 10),
(2, 1, 2, 10),
(2, 2, 2, 100),
(3, 3, 1, 1000),
(4, 3, 2, 1000);