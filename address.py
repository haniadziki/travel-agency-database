import mysql.connector
import random

def load_addresses(file_name):
    """
    Ładuje listę adresów z pliku tekstowego.
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def fill_address_table(n):
    conn = mysql.connector.connect(
        user='team10',
        password="te@mzaio",
        host="giniewicz.it",
        database="team10",
        auth_plugin="mysql_native_password"
    )
    cursor = conn.cursor()

    # Ładowanie adresów z plików
    addresses_polska = load_addresses("text_folder/UlicaP.txt")  
    addresses_anglia = load_addresses("text_folder/UlicaA.txt")  
    addresses_hiszpania = load_addresses("text_folder/UlicaH.txt")  
    addresses_wlochy = load_addresses("text_folder/UlicaW.txt")
    addresses_niemcy = load_addresses("text_folder/UlicaN.txt") 
    addresses_grecja = load_addresses("text_folder/UlicaG.txt") 

    addresses_by_city = {
        1: addresses_polska, 2: addresses_polska,
        3: addresses_anglia, 4: addresses_anglia,
        5: addresses_hiszpania, 6: addresses_hiszpania,
        7: addresses_wlochy, 8: addresses_wlochy,
        9: addresses_niemcy, 10: addresses_niemcy,
        11: addresses_grecja, 12: addresses_grecja,
    }

    generated_count = 0

    while generated_count < n:
        city_id = random.randint(1, 12)
        
        address_list = addresses_by_city.get(city_id, [])
        if not address_list:
            file_name_map = {
                (1, 2): "text_folder/UlicaP.txt",
                (3, 4): "text_folder/UlicaA.txt",
                (5, 6): "text_folder/UlicaH.txt",
                (7, 8): "text_folder/UlicaW.txt",
                (9, 10): "text_folder/UlicaN.txt",
                (11, 12):"text_folder/UlicaG.txt",
            }
            for ids, file_name in file_name_map.items():
                if city_id in ids:
                    address_list.extend(load_addresses(file_name))
                    break

        address = address_list.pop(0)

        postal_code = f"{random.randint(10, 99)}-{random.randint(100, 999)}"
        phone_number = f"+{random.randint(1, 99)} {random.randint(100, 999)}-{random.randint(1000, 9999)}"

        cursor.execute("""
            INSERT INTO address (city_id, address, postal_code, phone)
            VALUES (%s, %s, %s, %s)
        """, (city_id, address, postal_code, phone_number))

        generated_count += 1

    conn.commit()

    cursor.close()
    conn.close()

fill_address_table(291)