import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                dbname="store",
                user='postgres',
                password="pushokcharlik",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.{table_name}")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.{table_name} where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.{table_name}")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.{table_name}")

    def print_products(self) -> None:
        return self.get(f"SELECT * FROM public.product")

    def print_product_discount(self) -> None:
        return self.get(f"SELECT * FROM public.product_discount")

    def print_discount(self) -> None:
        return self.get(f"SELECT * FROM public.discount")

    def print_shop(self) -> None:
        return self.get(f"SELECT * FROM public.shop")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.{table_name} WHERE {key_name}={key_value};")

    def update_data_product(self, key_value: int, shop_id: int, photo_url: str, name: str) -> None:
        self.request(f"UPDATE public.product SET shop_id=\'{shop_id}\', photo_url=\'{photo_url}\', name=\'{name}\' "
                     f"WHERE id={key_value};")

    def update_data_discount(self, key_value: int, percent: int, duration: int) -> None:
        self.request(f"UPDATE public.discount SET percent=\'{percent}\', duration=\'{duration}\' "
                     f"WHERE id={key_value};")

    def update_data_product_discount(self, key_value: int, product_id: int, discount_id: int) -> None:
        self.request(f"UPDATE public.product_discount SET product_id=\'{product_id}\', discount_id=\'{discount_id}\' "
                     f"WHERE id={key_value};")

    def update_data_shop(self, key_value: int, address: str, manager_name: str, manager_surname: str) -> None:
        self.request(f"UPDATE public.shop SET address=\'{address}\', manager_name=\'{manager_name}\', "
                     f"manager_surname=\'{manager_surname}\' WHERE id={key_value};")

    def insert_data_discount(self, id_code: int, percent: int, duration: int) -> None:
        self.request(f"insert into public.discount (id, percent, duration) "
                     f"VALUES ({id_code}, \'{percent}\', \'{duration}\')")

    def insert_data_product_discount(self, id_code: int, product_id: int, discount_id: int) -> None:
        self.request(f"insert into public.product_discount (id, product_id, discount_id) "
                     f"VALUES ({id_code}, \'{product_id}\', \'{discount_id}\')")

    def insert_data_product(self, id_code: int, shop_id: int, photo_url: str, name: str) -> None:
        self.request(f"insert into public.product (id, shop_id, photo_url, name) "
                     f"VALUES ({id_code}, \'{shop_id}\', \'{photo_url}\', \'{name}\')")

    def insert_data_shop(self, id_code: int, address: str, manager_name: str, manager_surname: str) -> None:
        self.request(f"insert into public.shop (id, address, manager_name, manager_surname) "
                     f"VALUES ({id_code}, \'{address}\', \'{manager_name}\', \'{manager_surname}\')")

    def product_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.product select (SELECT MAX(id)+1 FROM public.product), "
                         "(SELECT id FROM public.shop LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.shop)-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), '');")

    def shop_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.shop select (SELECT (MAX(id)+1) FROM public.shop), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''); ")

    def discount_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.discount select (SELECT MAX(id)+1 FROM public.discount), "
                         "FLOOR(RANDOM()*(100000-1)+1),"
                         "FLOOR(RANDOM()*(100000-1)+1); ")

    def product_discount_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.product_discount select (SELECT MAX(id)+1 FROM public.product_discount), "
                         "(SELECT id FROM public.product LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.product)-1)))), "
                         "(SELECT id FROM public.discount LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.discount)-1))));")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} inner join public.{table3_name} as three "
                        f"on three.{table3_key}=one.{table13_key} "
                        f"where {search}")

    def search_data_all_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} inner join public.{table3_name} as three "
                        f"on three.{table3_key}=one.{table13_key} inner join public.{table4_name} as four "
                        f"on four.{table4_key}=two.{table24_key} "
                        f"where {search}")
