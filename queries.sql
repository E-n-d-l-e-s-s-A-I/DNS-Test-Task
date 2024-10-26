INSERT INTO city (name) VALUES
('Владивосток'),
('Хабаровск');

INSERT INTO store (name, city_id) VALUES
('DNS на Некрасовской', 1),
('DNS на Постышева', 1);


INSERT INTO product (name, price) VALUES
('Клавиатура проводная KEYRON Eclipse', 999),
('27" Монитор Xiaomi G27i черный', 14999),
('6.56" Смартфон Tecno SPARK GO 2024 64 ГБ черный', 6999.50);

INSERT INTO sale (store_id) VALUES
(1),
(1);

INSERT INTO sale_products (sale_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 3),
(2, 2, 3);