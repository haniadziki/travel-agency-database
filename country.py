import mysql.connector

con = mysql.connector.connect(
 host = "giniewicz.it",
 user = "team10",
 password = "te@mzaio",
 database = "team10"
)

mycursor = con.cursor()

mycursor.execute('''INSERT INTO country (country_id, country) 
            VALUES 
(NULL, 'Polska'),
(NULL, 'Anglia'),
(NULL, 'Hiszpania'),
(NULL, 'Włochy'),
(NULL, 'Niemcy'),
(NULL, 'Grecja')''')

con.commit()
mycursor.close()
con.close()