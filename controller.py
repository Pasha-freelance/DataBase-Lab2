from psycopg2 import Error
import model
import view
import datetime
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name).upper()
        if t_name:
            if t_name == 'PRODUCT':
                self.v.print_product(self.m.print_products())
            elif t_name == 'SHOP':
                self.v.print_shop(self.m.print_shop())
            elif t_name == 'DISCOUNT':
                self.v.print_discount(self.m.print_discount())
            elif t_name == 'PRODUCT_DISCOUNT':
                self.v.print_product_discount(self.m.print_product_discount())

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name).upper()
        k_name = self.v.valid.check_pk_name(table_name, key_name).upper()
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'PRODUCT' or t_name == 'DISCOUNT':
                    if t_name == 'PRODUCT':
                        count_p = self.m.find('PRODUCT_DISCOUNT', 'product_id', value)[0]
                    if t_name == 'DISCOUNT':
                        count_p = self.m.find('PRODUCT_DISCOUNT', 'discount_id', value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'SHOP':
                    count_p = self.m.find('PRODUCT', 'shop_id', value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_product(self, key: str, shop_id: int, photo_url: str, name: str):
        if self.v.valid.check_possible_keys('Product', 'id', int(key)):
            count_p = self.m.find('Product', 'id', int(key))
            p_val = self.v.valid.check_pk(key, count_p)
        if self.v.valid.check_possible_keys('Shop', 'id', int(shop_id)):
            count_c = self.m.find('Shop', 'id', int(shop_id))
            c_val = self.v.valid.check_pk(shop_id, count_c)

        if p_val and c_val and photo_url and name:
            try:
                self.m.update_data_product(p_val, c_val, photo_url, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_shop(self, key: str, address: str, manager_name: str, manager_surname: str):
        if self.v.valid.check_possible_keys('Shop', 'id', key):
            count_s = self.m.find('Shop', 'id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)

        if s_val and address and manager_name and manager_surname:
            try:
                self.m.update_data_shop(s_val, address, manager_name, manager_surname)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_discount(self, key: str, percent: int, duration: int):
        if self.v.valid.check_possible_keys('Discount', 'id', key):
            count_s = self.m.find('Discount', 'id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)

        if s_val and percent and duration:
            try:
                self.m.update_data_discount(s_val, percent, duration)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_product_discount(self, key: str, product_id: int, discount_id: int):
        if self.v.valid.check_possible_keys('Product_discount', 'id', key):
            count_s = self.m.find('Product_discount', 'id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)
        if self.v.valid.check_possible_keys('Product', 'id', product_id):
            count_p = self.m.find('Product', 'id', int(product_id))
            p_val = self.v.valid.check_pk(product_id, count_p)
        if self.v.valid.check_possible_keys('Discount', 'id', discount_id):
            count_d = self.m.find('Discount', 'id', int(discount_id))
            d_val = self.v.valid.check_pk(discount_id, count_d)

        if s_val and p_val and d_val:
            try:
                self.m.update_data_product_discount(s_val, p_val, d_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_product(self, key: str, shop_id: int, photo_url: str, name: str):
        if self.v.valid.check_possible_keys('Product', 'id', key):
            count_p = self.m.find('Product', 'id', int(key))
            p_val = self.v.valid.check_pk(key, count_p)
        if self.v.valid.check_possible_keys('Shop', 'id', shop_id):
            count_c = self.m.find('Shop', 'id', int(shop_id))
            c_val = self.v.valid.check_pk(shop_id, count_c)

        if (not count_p or count_p == (0,)) and c_val \
                and photo_url \
                and name:
            try:
                self.m.insert_data_product(int(key), c_val, photo_url, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_discount(self, key: str, percent: int, duration: int):
        if self.v.valid.check_possible_keys('Discount', 'id', key):
            count_s = self.m.find('Discount', 'id', int(key))

        if (not count_s or count_s == (0,)) \
                and percent \
                and duration:
            try:
                self.m.insert_data_discount(int(key), percent, duration)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_product_discount(self, key: str, product_id: int, discount_id: int):
        if self.v.valid.check_possible_keys('Product_discount', 'id', key):
            count_s = self.m.find('Product_discount', 'id', int(key))
        if self.v.valid.check_possible_keys('Product_discount', 'id', product_id):
            count_p = self.m.find('Product', 'id', int(product_id))
            p_val = self.v.valid.check_pk(product_id, count_p)
        if self.v.valid.check_possible_keys('Discount', 'id', discount_id):
            count_d = self.m.find('Discount', 'id', int(discount_id))
            d_val = self.v.valid.check_pk(discount_id, count_d)

        if (not count_s or count_s == (0,)) and p_val and d_val:
            try:
                self.m.insert_data_product_discount(int(key), p_val, d_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_shop(self, key: str, address: str, manager_name: str, manager_surname: str):
        if self.v.valid.check_possible_keys('Shop', 'id', key):
            count_s = self.m.find('Shop', 'id', int(key))

        if (not count_s or count_s == (0,)) and address and manager_name and manager_surname:
            try:
                self.m.insert_data_shop(int(key), address, manager_name, manager_surname)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name).upper()
        if t_name:
            if t_name == 'PRODUCT':
                self.m.product_data_generator(n)
            elif t_name == 'SHOP':
                self.m.shop_data_generator(n)
            elif t_name == 'DISCOUNT':
                self.m.discount_data_generator(n)
            elif t_name == 'PRODUCT_DISCOUNT':
                self.m.product_discount_data_generator(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)

            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        t4_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and self.v.valid.check_key_names(t2_n, table24_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key) \
                and t4_n and self.v.valid.check_key_names(t4_n, table4_key) \
                and self.v.valid.check_key_names(t4_n, table24_key):

            start_time = time.time()
            result = self.m.search_data_all_tables(table1_name, table2_name, table3_name, table4_name,
                                                   table1_key, table2_key, table3_key, table13_key,
                                                   table4_key, table24_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)
