# DataBase-Lab2
Лабораторна робота 2 Створення додатку бази даних, орієнтованого на взаємодію з СУБД PostgreSQL

Обрана предметна галузь передбачає зберігання товарів в кожному окремому філіалу мережі магазинів. Згідно цієї області для побудови бази даних було виділено наступні сутності:

1.	Сутність “Shop” містить такі атрибути як ID, адреса магазину та контакти управляючого філіалом. Слугує для зберігання інформації про філіал
2.	Сутність “Discount” містить такі атрибути як ID, відсоток знижки та термін її дії. Слугує зберігання інформації про знижку.
3.	Сутність  “Product_discount” містить такі атрибути як ID, ідентифікатор продукту та ідентифікатор знижки. Слугує для зв’язування знижки та продукту.
4.	Сутність “Product” містить такі атрибути як ID, ідентифікатор відділу, до якого належить продукт та назву продукту. Слугує для зберігання інформації про конкретний продукт.
