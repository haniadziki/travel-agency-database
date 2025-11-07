import mysql.connector
import random

conn = mysql.connector.connect(user='team10', password="te@mzaio", host="giniewicz.it", database="team10", auth_plugin="mysql_native_password")
cursor = conn.cursor()

with open('text_folder/Imiona.txt', 'r', encoding='utf-8') as file:
    first_names = [line.strip() for line in file.readlines()]

with open('text_folder/Nazwiska.txt', 'r', encoding='utf-8') as file:
    last_names = [line.strip() for line in file.readlines()]

if len(first_names) >= 6 and len(last_names) >= 6:
    # Wybieranie losowych imiona i nazwiska
    random.shuffle(first_names)
    random.shuffle(last_names)
    selected_first_names = first_names[:6]
    selected_last_names = last_names[:6]

    address_ids = list(range(286, 292))
    random.shuffle(address_ids)

    # Wstawianie danych do tabeli staff
    for i in range(6):
        staff_id = i + 1  # staff_id od 1 do 6
        first_name = selected_first_names[i]
        last_name = selected_last_names[i]
        email = f"{first_name[0].lower()}.{last_name.lower()}@work.com"
        address_id = address_ids[i]

        cursor.execute("""
            INSERT INTO staff (staff_id, first_name, last_name, email, address_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (staff_id, first_name, last_name, email, address_id))

    conn.commit()
else:
    print("Brak wystarczającej liczby imion lub nazwisk w plikach.")

cursor.close()
conn.close()
