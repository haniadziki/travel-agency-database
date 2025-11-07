import mysql.connector

con = mysql.connector.connect(
 host = "giniewicz.it",
 user = "team10",
 password = "te@mzaio",
 database = "team10"
)

mycursor = con.cursor()

mycursor.execute('''INSERT INTO city (city_id, city, country_id)
                 VALUES
(NULL, 'Warszawa', 1),
(NULL, 'Kraków', 1),
(NULL, 'Londyn', 2),
(NULL, 'Manchester', 2),
(NULL, 'Madryt', 3),
(NULL, 'Alicante', 3),
(NULL, 'Mediolan', 4),
(NULL, 'Wenecja', 4),
(NULL, 'Berlin', 5),
(NULL, 'Hamburg', 5),
(NULL, 'Ateny', 6),
(NULL, 'Sparta', 6);

''')

con.commit()
mycursor.close()
con.close()