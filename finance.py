import mysql.connector

con = mysql.connector.connect(
    host = "giniewicz.it",
    user = "team10",
    password = "te@mzaio",
    database = "team10"
)


#finance
mycursor = con.cursor()
mycursor.execute('''           
INSERT INTO finance (offer_id)
SELECT offer_id FROM offers;
               ''')

mucursor = con.cursor()
mycursor.execute('''
UPDATE finance f
JOIN offers o ON f.offer_id = o.offer_id
SET f.balance = o.overall_price - o.original_price;
                 ''')

con.commit()
mycursor.close()
con.close()
