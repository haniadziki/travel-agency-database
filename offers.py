import mysql.connector
import random


con = mysql.connector.connect(
    host="giniewicz.it",
    user="team10",
    password="te@mzaio",
    database="team10"
)

mycursor = con.cursor()

def generate_offers(n):
    offers = []

    mycursor.execute("SELECT city_id FROM city")
    city_ids= mycursor.fetchall()

    attractions_and_prices = {"theater": 50, "art museum": 15, "historical museum": 12,
                              "landscape park": 8, "botanic garden": 10, "aquapark": 25}
    
    hotels_and_prices = {"Grand Royal Hotel": 120, "Seaside Resort": 150, "Mountain View Lodge": 100,
                         "Golden Sands Hotel": 130, "Urban Oasis Hotel": 110, "Lakeside Retreat": 90,
                         "The Velvet Palace": 200, "Sunny Horizon Inn": 80, "Crystal Bay Resort": 140,
                         "The Emerald Stay": 170}
    
    generated_count = 0
    
    while generated_count < n:
        city_id = random.choice(city_ids)[0]

        durations = [4, 7, 10, 14]
        duration_length = random.choice(durations)

        plane_number = random.randint(1000, 5000)
        plane_price = random.randint(500, 2000)

        attractions = random.sample(list(attractions_and_prices.keys()), 3)
        attractions_prices = sum(attractions_and_prices[attraction] for attraction in attractions)

        hotel = random.choice(list(hotels_and_prices.keys()))
        hotel_price = hotels_and_prices[hotel] * duration_length

        original_price = int(plane_price) + int(attractions_prices) + int(hotel_price)
        overall_price = round(original_price * 1.5)

        mycursor.execute('''
        SELECT COUNT(*) FROM offers
        WHERE city_id = %s AND duration_length = %s 
             AND attractions = %s
        ''', (city_id, duration_length, ', '.join(attractions)))
        
        result = mycursor.fetchone()[0]
        if result == 0:
            mycursor.execute('''
            INSERT INTO offers (city_id, duration_length, plane_number, plane_price, attractions, 
                                attractions_price, hotel_name, hotel_price, original_price, overall_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (city_id, duration_length, plane_number, plane_price,
                  ', '.join(attractions), attractions_prices, hotel, hotel_price, 
                  original_price, overall_price))
            con.commit()
            generated_count += 1
    
    return offers

generate_offers(20)

mycursor.close()
con.close()
