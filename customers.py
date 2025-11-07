import mysql.connector
import random

conn = mysql.connector.connect(user='team10', password="te@mzaio", host="giniewicz.it", database="team10", auth_plugin="mysql_native_password")
cursor = conn.cursor()

with open('text_folder/Imiona.txt', 'r', encoding='utf-8') as file:
    imiona = [line.strip() for line in file.readlines()]

with open('text_folder/Nazwiska.txt', 'r', encoding='utf-8') as file:
    nazwiska = [line.strip() for line in file.readlines()]

if len(imiona) > 0 and len(nazwiska) > 0:
    total_customers = 285
    
    imiona_repeated = imiona * (total_customers // len(imiona)) + imiona[:total_customers % len(imiona)]
    nazwiska_repeated = nazwiska * (total_customers // len(nazwiska)) + nazwiska[:total_customers % len(nazwiska)]
    random.shuffle(imiona_repeated)
    random.shuffle(nazwiska_repeated)

    # Generowanie unikalnych address_id
    address_ids = list(range(1, total_customers + 1))
    random.shuffle(address_ids)

    # Domeny do generowania emaili
    domains = ['@poczta.com'] * 150 + ['@mail.com'] * 135
    random.shuffle(domains)

    # Wstawianie danych do tabeli customers
    for i in range(total_customers):
        customer_id = i + 1
        first_name = imiona_repeated[i]
        last_name = nazwiska_repeated[i]
        email = f"{first_name[0].lower()}.{last_name.lower()}{domains[i]}"
        address_id = address_ids[i]
        
        cursor.execute("""
            INSERT INTO customers (customer_id, first_name, last_name, email, address_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, first_name, last_name, email, address_id))

    conn.commit()
else:
    print("Brak wystarczającej liczby imion lub nazwisk w plikach.")

cursor.close()
conn.close()
