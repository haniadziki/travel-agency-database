import mysql.connector
import random
from datetime import datetime, timedelta


con = mysql.connector.connect(
    host="giniewicz.it",
    user="team10",
    password="te@mzaio",
    database="team10"
)

mycursor = con.cursor()

def generate_orders(n):
    mycursor.execute("SELECT offer_id, duration_length FROM offers")
    offers = mycursor.fetchall()

    mycursor.execute("SELECT customer_id FROM customers")
    customers_ids = mycursor.fetchall()

    mycursor.execute("SELECT staff_id FROM staff")
    staff_ids = mycursor.fetchall()

    start_date = datetime.strptime("01.01.2023", "%d.%m.%Y")
    end_date = datetime.strptime("31.12.2024", "%d.%m.%Y")
    days_range = (end_date - start_date).days

    all_dates = []
    for day_offset in range(days_range + 1):
        current_date = start_date + timedelta(days=day_offset)
        month = current_date.month
        if month in [7, 8]:
            weight = 10
        elif month in [6, 9]:
            weight = 5
        elif month in [4, 5]:
            weight = 3
        else:
            weight = 1
        all_dates.extend([current_date] * weight)

    order_dates = random.choices(all_dates, k=n)

    for order_date in order_dates:
        offer = random.choice(offers)
        offer_id, duration_length = offer

        customer_id = random.choice(customers_ids)[0]
        staff_id = random.choice(staff_ids)[0]

        random_days_after_order = random.randint(0, days_range)
        trip_start = order_date + timedelta(days=random_days_after_order)
        trip_end = trip_start + timedelta(days=duration_length - 1)

        mycursor.execute('''
            INSERT INTO orders (offer_id, customer_id, staff_id, order_date, trip_start, trip_end)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (offer_id, customer_id, staff_id, order_date, trip_start, trip_end))

    con.commit()

generate_orders(1000)

mycursor.close()
con.close()
