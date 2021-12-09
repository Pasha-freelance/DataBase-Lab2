import datetime


class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg.upper() in ['PRODUCT', 'SHOP', 'DISCOUNT', 'PRODUCT_DISCOUNT']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        table_name = table_name.upper()
        if table_name == 'PRODUCT' and key_name == 'id' \
                or table_name == 'SHOP' and key_name == 'id' \
                or table_name == 'DISCOUNT' and key_name == 'id' \
                or table_name == 'PRODUCT_DISCOUNT' and key_name == 'id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val, count):
        try:
            value = int(val)
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if count and not count == (0,):
                return value
            else:
                return 0

    def check_key_names(self, table_name: str, key: str):
        table_name = table_name.upper()
        if table_name == 'PRODUCT' and key in ['id', 'shop_id', 'photo_url', 'name']:
            return True
        elif table_name == 'SHOP' and key in ['id', 'address', 'manager_name', 'manager_surname']:
            return True
        elif table_name == 'DISCOUNT' and key in ['id', 'percent', 'duration']:
            return True
        elif table_name == 'PRODUCT_DISCOUNT' and key in ['id', 'product_id', 'discount_id']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        table_name = table_name.upper()
        if table_name == 'PRODUCT':
            if key in ['id', 'shop_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['photo_url', 'name']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for product table'
                print(self.error)
                return False
        elif table_name == 'PRODUCT_DISCOUNT':
            if key in ['id', 'product_id', 'discount_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for product table'
                print(self.error)
                return False
        elif table_name == 'SHOP':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['address', 'manager_name', 'manager_surname']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for shop table'
                print(self.error)
                return False
        elif table_name == 'DISCOUNT':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif table_name in ['percent', 'duration']:
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct {table_name} value'
                    print(self.error)
                    return False
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for discount table'
                print(self.error)
                return False
        elif table_name == 'SHOP':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['manager_name', 'manager_surname', 'address']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for shop table'
                print(self.error)
                return False
